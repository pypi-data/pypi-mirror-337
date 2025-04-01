# aws_voucher/cognito.py
import logging
from botocore.exceptions import ClientError
from .core import get_boto3_client, handle_aws_error

logger = logging.getLogger(__name__)

class CognitoManager:
    def __init__(self):
        self.client = get_boto3_client('cognito-idp')
        self._user_pool_id = None
        self._app_client_id = None

    @property
    def user_pool_id(self):
        """Lazy-load user pool ID"""
        if self._user_pool_id is None:
            self._user_pool_id = self._get_or_create_user_pool('Voucher')
        return self._user_pool_id

    @property
    def app_client_id(self):
        """Lazy-load app client ID"""
        if self._app_client_id is None:
            self._app_client_id = self._get_or_create_app_client(self.user_pool_id, 'VoucherAppClient')
        return self._app_client_id

    @handle_aws_error
    def _get_or_create_user_pool(self, pool_name):
        """Get existing or create new user pool"""
        try:
            pools = self.client.list_user_pools(MaxResults=20)
            for pool in pools['UserPools']:
                if pool['Name'] == pool_name:
                    logger.info(f"Using existing user pool: {pool['Id']}")
                    return pool['Id']
            
            # Create new pool if not found
            response = self.client.create_user_pool(
                PoolName=pool_name,
                Policies={
                    'PasswordPolicy': {
                        'MinimumLength': 8,
                        'RequireUppercase': True,
                        'RequireLowercase': True,
                        'RequireNumbers': True,
                        'RequireSymbols': True
                    }
                },
                Schema=[
                    {
                        'Name': 'email',
                        'AttributeDataType': 'String',
                        'Mutable': True,
                        'Required': True
                    }
                ],
                AutoVerifiedAttributes=['email'],
                UsernameAttributes=['email'],
                EmailVerificationMessage='Your verification code is {####}',
                EmailVerificationSubject='Verify your email for MyUserPool',
                VerificationMessageTemplate={
                    'DefaultEmailOption': 'CONFIRM_WITH_CODE'
                }
            )
            pool_id = response['UserPool']['Id']
            logger.info(f"Created new user pool: {pool_id}")
            return pool_id
        except ClientError as e:
            logger.error(f"Error with user pool: {e}")
            raise

    @handle_aws_error
    def _get_or_create_app_client(self, user_pool_id, client_name):
        """Get existing or create new app client"""
        try:
            clients = self.client.list_user_pool_clients(
                UserPoolId=user_pool_id,
                MaxResults=20
            )
            for client in clients['UserPoolClients']:
                if client['ClientName'] == client_name:
                    logger.info(f"Using existing app client: {client['ClientId']}")
                    return client['ClientId']
            
            # Create new client if not found
            response = self.client.create_user_pool_client(
                UserPoolId=user_pool_id,
                ClientName=client_name,
                GenerateSecret=False,
                ExplicitAuthFlows=[
                    'ALLOW_USER_PASSWORD_AUTH',
                    'ALLOW_ADMIN_USER_PASSWORD_AUTH',
                    'ALLOW_REFRESH_TOKEN_AUTH'
                ]
            )
            client_id = response['UserPoolClient']['ClientId']
            logger.info(f"Created new app client: {client_id}")
            return client_id
        except ClientError as e:
            logger.error(f"Error with app client: {e}")
            raise

    @handle_aws_error
    def register_user(self, email, password):
        """Register a new user"""
        try:
            response = self.client.sign_up(
                ClientId=self.app_client_id,
                Username=email,
                Password=password,
                UserAttributes=[
                    {
                        'Name': 'email',
                        'Value': email
                    }
                ]
            )
            logger.info(f"User registered: {email}")
            return response
        except self.client.exceptions.UsernameExistsException:
            logger.warning(f"User already exists: {email}")
            return None
        except ClientError as e:
            logger.error(f"Error registering user: {e}")
            raise

    @handle_aws_error
    def confirm_user(self, email, confirmation_code):
        """Confirm user registration"""
        try:
            response = self.client.confirm_sign_up(
                ClientId=self.app_client_id,
                Username=email,
                ConfirmationCode=confirmation_code
            )
            logger.info(f"User confirmed: {email}")
            return response
        except self.client.exceptions.CodeMismatchException:
            logger.warning(f"Invalid confirmation code for: {email}")
            return None
        except ClientError as e:
            logger.error(f"Error confirming user: {e}")
            raise

    @handle_aws_error
    def delete_user(self, email):
        """Delete a user from Cognito"""
        try:
            response = self.client.admin_delete_user(
                UserPoolId=self.user_pool_id,
                Username=email
            )
            logger.info(f"User deleted: {email}")
            return response
        except ClientError as e:
            logger.error(f"Error deleting user: {e}")
            raise