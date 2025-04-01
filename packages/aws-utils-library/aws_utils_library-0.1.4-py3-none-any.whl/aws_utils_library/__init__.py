# aws_voucher/__init__.py
from .core import AWSConfig, get_aws_config, get_boto3_client, handle_aws_error
from .s3 import S3Manager
from .dynamodb import DynamoDBManager, VoucherDBManager
from .cognito import CognitoManager
from .sns import SNSManager
from .sqs import SQSManager
from .stripe_helper import StripeManager

# Initialize default instances for convenience
aws_config = AWSConfig()
s3_manager = S3Manager()
dynamodb_manager = DynamoDBManager()
voucher_db_manager = VoucherDBManager()
cognito_manager = CognitoManager()
sns_manager = SNSManager()
sqs_manager = SQSManager()
stripe_manager = StripeManager()

__all__ = [
    'AWSConfig',
    'get_aws_config',
    'get_boto3_client',
    'handle_aws_error',
    'S3Manager',
    'DynamoDBManager',
    'VoucherDBManager',
    'CognitoManager',
    'SNSManager',
    'SQSManager',
    'StripeManager',
    # Default instances
    'aws_config',
    's3_manager',
    'dynamodb_manager',
    'voucher_db_manager',
    'cognito_manager',
    'sns_manager',
    'sqs_manager',
    'stripe_manager'
]