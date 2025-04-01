# aws_voucher/dynamodb.py
import uuid
import logging
from datetime import datetime
from botocore.exceptions import ClientError
from .core import get_boto3_client, handle_aws_error

logger = logging.getLogger(__name__)

class DynamoDBManager:
    def __init__(self):
        self.client = get_boto3_client('dynamodb')

    @handle_aws_error
    def create_table(self, table_name, attribute_definitions, key_schema, **kwargs):
        """Create a DynamoDB table with common configurations"""
        defaults = {
            'BillingMode': 'PAY_PER_REQUEST',
            'StreamSpecification': {'StreamEnabled': False},
            'SSESpecification': {
                'Enabled': True,
                'SSEType': 'KMS'
            },
            'Tags': [
                {
                    'Key': 'Environment',
                    'Value': 'Production'
                }
            ]
        }
        params = {
            'TableName': table_name,
            'AttributeDefinitions': attribute_definitions,
            'KeySchema': key_schema,
            **defaults,
            **kwargs
        }
        
        try:
            response = self.client.create_table(**params)
            logger.info(f"Created table {table_name}: {response}")
            return response
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceInUseException':
                logger.info(f"Table {table_name} already exists")
                return None
            logger.error(f"Error creating table {table_name}: {e}")
            raise

    @handle_aws_error
    def ensure_table_exists(self, table_name, attribute_definitions, key_schema, **kwargs):
        """Ensure table exists, create if it doesn't"""
        try:
            self.client.describe_table(TableName=table_name)
            logger.info(f"Table {table_name} exists")
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceNotFoundException':
                logger.info(f"Creating table {table_name}")
                self.create_table(table_name, attribute_definitions, key_schema, **kwargs)
                waiter = self.client.get_waiter('table_exists')
                waiter.wait(TableName=table_name)
                return True
            logger.error(f"Error checking table {table_name}: {e}")
            return False

    @handle_aws_error
    def put_item(self, table_name, item, condition_expression=None):
        """Put item into DynamoDB table"""
        params = {
            'TableName': table_name,
            'Item': item
        }
        if condition_expression:
            params['ConditionExpression'] = condition_expression
            
        try:
            response = self.client.put_item(**params)
            logger.info(f"Added item to {table_name}: {response}")
            return response
        except ClientError as e:
            if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
                logger.warning(f"Item already exists in {table_name}")
                return None
            logger.error(f"Error adding item to {table_name}: {e}")
            raise

    @handle_aws_error
    def get_item(self, table_name, key):
        """Get item from DynamoDB table"""
        try:
            response = self.client.get_item(
                TableName=table_name,
                Key=key
            )
            if 'Item' in response:
                return response['Item']
            return None
        except ClientError as e:
            logger.error(f"Error getting item from {table_name}: {e}")
            raise

    @handle_aws_error
    def scan_table(self, table_name, filter_expression=None, expression_values=None):
        """Scan DynamoDB table with optional filter"""
        params = {'TableName': table_name}
        if filter_expression and expression_values:
            params['FilterExpression'] = filter_expression
            params['ExpressionAttributeValues'] = expression_values
            
        try:
            response = self.client.scan(**params)
            return response.get('Items', [])
        except ClientError as e:
            logger.error(f"Error scanning table {table_name}: {e}")
            raise

    @handle_aws_error
    def update_item(self, table_name, key, update_expression, expression_values):
        """Update item in DynamoDB table"""
        try:
            response = self.client.update_item(
                TableName=table_name,
                Key=key,
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_values
            )
            logger.info(f"Updated item in {table_name}: {response}")
            return response
        except ClientError as e:
            logger.error(f"Error updating item in {table_name}: {e}")
            raise

    @handle_aws_error
    def delete_item(self, table_name, key):
        """Delete item from DynamoDB table"""
        try:
            response = self.client.delete_item(
                TableName=table_name,
                Key=key
            )
            logger.info(f"Deleted item from {table_name}: {response}")
            return response
        except ClientError as e:
            logger.error(f"Error deleting item from {table_name}: {e}")
            raise

class VoucherDBManager(DynamoDBManager):
    """Specialized manager for Voucher-related tables"""
    
    def ensure_customer_table(self):
        """Ensure Customer table exists with proper schema"""
        return self.ensure_table_exists(
            table_name='Customer',
            attribute_definitions=[
                {'AttributeName': 'customer_id', 'AttributeType': 'S'},
                {'AttributeName': 'customer_email', 'AttributeType': 'S'}
            ],
            key_schema=[
                {'AttributeName': 'customer_id', 'KeyType': 'HASH'},
                {'AttributeName': 'customer_email', 'KeyType': 'RANGE'}
            ]
        )

    def ensure_admin_table(self):
        """Ensure Admin table exists with proper schema"""
        return self.ensure_table_exists(
            table_name='Admin',
            attribute_definitions=[
                {'AttributeName': 'admin_id', 'AttributeType': 'S'},
                {'AttributeName': 'admin_email', 'AttributeType': 'S'}
            ],
            key_schema=[
                {'AttributeName': 'admin_id', 'KeyType': 'HASH'},
                {'AttributeName': 'admin_email', 'KeyType': 'RANGE'}
            ]
        )

    def ensure_voucher_table(self):
        """Ensure Voucher table exists with proper schema"""
        return self.ensure_table_exists(
            table_name='Voucher',
            attribute_definitions=[
                {'AttributeName': 'voucher_id', 'AttributeType': 'S'},
                {'AttributeName': 'voucher_brand', 'AttributeType': 'S'}
            ],
            key_schema=[
                {'AttributeName': 'voucher_id', 'KeyType': 'HASH'},
                {'AttributeName': 'voucher_brand', 'KeyType': 'RANGE'}
            ]
        )

    def ensure_voucher_code_table(self):
        """Ensure VoucherCode table exists with proper schema"""
        return self.ensure_table_exists(
            table_name='VoucherCode',
            attribute_definitions=[
                {'AttributeName': 'code_id', 'AttributeType': 'S'},
                {'AttributeName': 'user_email', 'AttributeType': 'S'}
            ],
            key_schema=[
                {'AttributeName': 'code_id', 'KeyType': 'HASH'},
                {'AttributeName': 'user_email', 'KeyType': 'RANGE'}
            ]
        )