# aws_voucher/core.py
import boto3
from botocore.config import Config
import logging
from functools import lru_cache

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AWSConfig:
    """
    Central configuration for AWS services
    """
    def __init__(self, region_name='us-east-1', max_retries=3, timeout=30):
        self.region_name = region_name
        self.max_retries = max_retries
        self.timeout = timeout
        self._config = Config(
            region_name=region_name,
            retries={
                'max_attempts': max_retries,
                'mode': 'standard'
            },
            connect_timeout=timeout,
            read_timeout=timeout
        )
    
    @property
    def config(self):
        return self._config

@lru_cache(maxsize=None)
def get_aws_config():
    """
    Cached AWS configuration to avoid repeated initialization
    """
    return AWSConfig()

def get_boto3_client(service_name, config=None):
    """
    Get a cached boto3 client with proper configuration
    """
    if config is None:
        config = get_aws_config()
    return boto3.client(service_name, config=config.config)

def handle_aws_error(func):
    """
    Decorator to handle common AWS errors
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"AWS Error in {func.__name__}: {str(e)}")
            raise
    return wrapper