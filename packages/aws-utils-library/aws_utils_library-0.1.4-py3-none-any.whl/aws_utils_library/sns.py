# aws_voucher/sns.py
import logging
from botocore.exceptions import ClientError
from .core import get_boto3_client, handle_aws_error

logger = logging.getLogger(__name__)

class SNSManager:
    def __init__(self):
        self.client = get_boto3_client('sns')

    @handle_aws_error
    def get_topic_arn(self, topic_name):
        """Get ARN for an existing topic"""
        try:
            topics = self.client.list_topics()
            for topic in topics['Topics']:
                if topic_name in topic['TopicArn']:
                    return topic['TopicArn']
            return None
        except ClientError as e:
            logger.error(f"Error listing topics: {e}")
            raise

    @handle_aws_error
    def create_topic(self, topic_name):
        """Create a new SNS topic"""
        try:
            response = self.client.create_topic(Name=topic_name)
            arn = response['TopicArn']
            logger.info(f"Created topic: {arn}")
            return arn
        except ClientError as e:
            logger.error(f"Error creating topic: {e}")
            raise

    @handle_aws_error
    def setup_topic(self, topic_name):
        """Ensure topic exists, create if it doesn't"""
        arn = self.get_topic_arn(topic_name)
        if arn:
            return arn
        return self.create_topic(topic_name)

    @handle_aws_error
    def subscribe_email(self, topic_arn, email):
        """Subscribe email to topic"""
        try:
            response = self.client.subscribe(
                TopicArn=topic_arn,
                Protocol='email',
                Endpoint=email
            )
            logger.info(f"Subscribed {email} to topic")
            return response['SubscriptionArn']
        except ClientError as e:
            logger.error(f"Error subscribing email: {e}")
            raise

    @handle_aws_error
    def publish_message(self, topic_arn, message):
        """Publish message to topic"""
        try:
            response = self.client.publish(
                TopicArn=topic_arn,
                Message=message
            )
            logger.info(f"Published message: {response['MessageId']}")
            return response['MessageId']
        except ClientError as e:
            logger.error(f"Error publishing message: {e}")
            raise