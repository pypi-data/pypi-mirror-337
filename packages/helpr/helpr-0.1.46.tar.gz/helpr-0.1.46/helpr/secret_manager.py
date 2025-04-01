import boto3
from botocore.exceptions import ClientError
import json

from abc import ABC, abstractmethod
from authlib.jose import JsonWebKey

class JWTSigningKeyProvider(ABC):
    @abstractmethod
    def private_key(self) -> JsonWebKey:
        pass
    @abstractmethod
    def public_key(self) -> JsonWebKey:
        pass
    @abstractmethod
    def public_key_kid(self)  -> str:
        pass


class AWSSecretManagerKeyProvider(JWTSigningKeyProvider):

    def __init__(self, secret_name, region_name, aws_access_key_id, aws_secret_access_key):
        jwt_secrets = SecretManager(secret_name, region_name, aws_access_key_id, aws_secret_access_key)
        jwt_secret = jwt_secrets.load_secrets()
        
        private_key_str = jwt_secret.get('private_key')
        public_key_str = jwt_secret.get('public_key')
        
        if not private_key_str or not public_key_str:
            raise ValueError("Missing required JWT keys in AWS Secret Manager")
            
        try:
            self._private_key = JsonWebKey.import_key(private_key_str)
            self._public_key = JsonWebKey.import_key(public_key_str)
        except Exception as e:
            raise ValueError(f"Failed to import JWT keys: {str(e)}")
        
    def private_key(self) -> JsonWebKey:
        return self._private_key

    def public_key(self) -> JsonWebKey:
        return self._public_key

    def public_key_kid(self) -> str:
        return self._public_key.as_dict()['kid']

class SecretManager:

    def __init__(self, secret_name, region_name, aws_access_key_id, aws_secret_access_key):
        self.secret_name = secret_name
        self._cached_secrets = None
        self._region_name = region_name
        self._aws_access_key_id = aws_access_key_id
        self._aws_secret_access_key = aws_secret_access_key

    def fetch_secrets(self):
        # Create a Secrets Manager client with credentials
        session = boto3.session.Session(
            aws_access_key_id=self._aws_access_key_id,
            aws_secret_access_key=self._aws_secret_access_key,
            region_name=self._region_name
        )
        client = session.client(
            service_name='secretsmanager'
        )

        try:
            get_secret_value_response = client.get_secret_value(
                SecretId=self.secret_name
            )
        except ClientError as e:
            raise e

        secret = get_secret_value_response['SecretString']
        return json.loads(secret)

    def load_secrets(self):
        if self._cached_secrets is None:
            self._cached_secrets = self.fetch_secrets()
        return self._cached_secrets