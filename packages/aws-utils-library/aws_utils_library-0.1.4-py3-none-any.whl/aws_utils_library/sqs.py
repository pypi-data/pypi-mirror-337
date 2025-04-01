# aws_voucher/sqs.py
import logging
from botocore.exceptions import ClientError
from .core import get_boto3_client, handle_aws_error
import json

logger = logging.getLogger(__name__)

class SQSManager:
    def __init__(self):
        self.client = get_boto3_client('sqs')

    @handle_aws_error
    def get_queue_url(self, queue_name):
        """Get URL for an existing queue"""
        try:
            response = self.client.get_queue_url(QueueName=queue_name)
            return response['QueueUrl']
        except self.client.exceptions.QueueDoesNotExist:
            return None
        except ClientError as e:
            logger.error(f"Error getting queue URL: {e}")
            raise

    @handle_aws_error
    def create_queue(self, queue_name, attributes=None):
        """Create a new SQS queue"""
        default_attrs = {
            'DelaySeconds': '0',
            'MessageRetentionPeriod': '86400',  # 1 day
            'VisibilityTimeout': '30'
        }
        if attributes:
            default_attrs.update(attributes)
            
        try:
            response = self.client.create_queue(
                QueueName=queue_name,
                Attributes=default_attrs
            )
            logger.info(f"Created queue: {queue_name}")
            return response['QueueUrl']
        except ClientError as e:
            logger.error(f"Error creating queue: {e}")
            raise

    @handle_aws_error
    def setup_queue(self, queue_name, attributes=None):
        """Ensure queue exists, create if it doesn't"""
        url = self.get_queue_url(queue_name)
        if url:
            return url
        return self.create_queue(queue_name, attributes)

    @handle_aws_error
    def subscribe_to_sns(self, queue_url, topic_arn):
        """Subscribe SQS queue to SNS topic"""
        try:
            # Get queue ARN
            attributes = self.client.get_queue_attributes(
                QueueUrl=queue_url,
                AttributeNames=['QueueArn']
            )
            queue_arn = attributes['Attributes']['QueueArn']
            
            # Set policy to allow SNS to send messages
            policy = {
                "Version": "2012-10-17",
                "Statement": [{
                    "Effect": "Allow",
                    "Principal": {"Service": "sns.amazonaws.com"},
                    "Action": "sqs:SendMessage",
                    "Resource": queue_arn,
                    "Condition": {
                        "ArnEquals": {"aws:SourceArn": topic_arn}
                    }
                }]
            }
            
            self.client.set_queue_attributes(
                QueueUrl=queue_url,
                Attributes={'Policy': json.dumps(policy)}
            )
            
            # Subscribe to SNS
            sns = get_boto3_client('sns')
            response = sns.subscribe(
                TopicArn=topic_arn,
                Protocol='sqs',
                Endpoint=queue_arn
            )
            logger.info(f"Subscribed queue to SNS topic")
            return response['SubscriptionArn']
        except ClientError as e:
            logger.error(f"Error subscribing queue to SNS: {e}")
            raise