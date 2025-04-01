# aws_voucher/s3.py
import logging
import json
from botocore.exceptions import ClientError
from .core import get_boto3_client, handle_aws_error

logger = logging.getLogger(__name__)

class S3Manager:
    def __init__(self):
        self.client = get_boto3_client('s3')

    @handle_aws_error
    def create_bucket(self, bucket_name, region=None):
        """Create an S3 bucket with public access configuration"""
        try:
            self.client.head_bucket(Bucket=bucket_name)
            logger.info(f"Bucket {bucket_name} already exists")
            return True
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == '404':
                try:
                    if region is None or region == 'us-east-1':
                        self.client.create_bucket(Bucket=bucket_name)
                    else:
                        location = {'LocationConstraint': region}
                        self.client.create_bucket(
                            Bucket=bucket_name,
                            CreateBucketConfiguration=location
                        )
                    
                    # Configure public access
                    self.client.put_public_access_block(
                        Bucket=bucket_name,
                        PublicAccessBlockConfiguration={
                            'BlockPublicAcls': False,
                            'IgnorePublicAcls': False,
                            'BlockPublicPolicy': False,
                            'RestrictPublicBuckets': False
                        }
                    )
                    logger.info(f"Bucket {bucket_name} created with public access")
                    return True
                except ClientError as e:
                    logger.error(f"Error creating bucket: {e}")
                    return False
            elif error_code == 'BucketAlreadyOwnedByYou':
                logger.info(f"Bucket {bucket_name} already owned by you")
                return True
            else:
                logger.error(f"Unexpected error checking bucket: {e}")
                return False

    @handle_aws_error
    def set_bucket_policy(self, bucket_name, policy_dict=None):
        """Set bucket policy for public read access"""
        if policy_dict is None:
            policy_dict = {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Principal": "*",
                        "Action": [
                            "s3:GetObject",
                            "s3:ListBucket"
                        ],
                        "Resource": [
                            f"arn:aws:s3:::{bucket_name}",
                            f"arn:aws:s3:::{bucket_name}/*"
                        ]
                    }
                ]
            }
        
        try:
            self.client.put_bucket_policy(
                Bucket=bucket_name,
                Policy=json.dumps(policy_dict)
            )
            logger.info(f"Bucket policy updated for {bucket_name}")
            return True
        except ClientError as e:
            logger.error(f"Error updating bucket policy: {e}")
            return False

    @handle_aws_error
    def upload_fileobj(self, file_obj, bucket_name, object_name):
        """Upload file-like object to S3"""
        try:
            self.client.upload_fileobj(file_obj, bucket_name, object_name)
            url = f"https://{bucket_name}.s3.amazonaws.com/{object_name}"
            logger.info(f"File uploaded to {url}")
            return url
        except ClientError as e:
            logger.error(f"Error uploading file: {e}")
            return None

    @handle_aws_error
    def delete_object(self, bucket_name, object_key):
        """Delete object from S3 bucket"""
        try:
            self.client.delete_object(Bucket=bucket_name, Key=object_key)
            logger.info(f"Deleted {object_key} from {bucket_name}")
            return True
        except ClientError as e:
            logger.error(f"Error deleting object: {e}")
            return False

    @handle_aws_error
    def delete_bucket(self, bucket_name):
        """Delete bucket and all its contents"""
        try:
            # List and delete all objects
            paginator = self.client.get_paginator('list_objects_v2')
            for page in paginator.paginate(Bucket=bucket_name):
                if 'Contents' in page:
                    delete_keys = {'Objects': [{'Key': obj['Key']} for obj in page['Contents']]}
                    self.client.delete_objects(Bucket=bucket_name, Delete=delete_keys)
            
            # Delete the bucket
            self.client.delete_bucket(Bucket=bucket_name)
            logger.info(f"Bucket {bucket_name} deleted successfully")
            return True
        except ClientError as e:
            logger.error(f"Error deleting bucket: {e}")
            return False