# aws_utils_library/exceptions.py
class AWSError(Exception):
    pass

class DynamoDBError(AWSError):
    pass

class S3Error(AWSError):
    pass