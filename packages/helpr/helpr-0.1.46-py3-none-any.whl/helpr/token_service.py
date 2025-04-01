"""
JWT Token Helper module for generating and verifying tokens.
"""
from typing import Any, Dict, Optional
from datetime import datetime, timedelta
from authlib.jose import JsonWebToken, JsonWebKey
from authlib.jose.errors import ExpiredTokenError, DecodeError, InvalidTokenError
from .exceptions import AppException
from .secret_manager import JWTSigningKeyProvider

class TokenException(AppException):
    """Base exception for token-related error"""
    def __init__(self, message: str, error_code: int = 1000, http_code: int = 400):
        super().__init__(message=message, error_code=error_code, http_code=http_code)

class TokenTypeMismatchException(TokenException):
    """Raised when token type doesn't match expected type"""
    def __init__(self, message: str = "Token type does not match expected type"):
        super().__init__(message=message, error_code=1001, http_code=400)

class TokenGenerationException(TokenException):
    """Raised when token generation fails"""
    def __init__(self, message: str = "Failed to generate token"):
        super().__init__(message=message, error_code=1002, http_code=500)

class TokenVerificationException(TokenException):
    """Raised when token verification fails"""
    def __init__(self, message: str = "Failed to verify token"):
        super().__init__(message=message, error_code=1003, http_code=401)

class JWTHelper:
    """Helper class for JWT token operations"""
    
    def __init__(self, key_provider: JWTSigningKeyProvider, algorithm: str = 'RS256'):
        """
        Initialize the JWT Helper.
        
        Args:
            key_provider: Provider object that supplies private and public keys
            algorithm (str): Algorithm to use for token signing

        Raises:
            ValueError: If algorithm is not supported
        """
        if algorithm not in ['RS256', 'RS384', 'RS512']:
            raise ValueError(f"Unsupported algorithm: {algorithm}")
            
        self.key_provider = key_provider
        self._algo = algorithm
        
    def verify_token(
        self,
        token: str,
        expected_token_type: str
    ) -> Dict[str, Any]:
        """
        Verify and decode JWT token.

        Args:
            token (str): Token to verify
            expected_token_type (str): Expected token type

        Returns:
            dict: Decoded token payload

        Raises:
            TokenVerificationException: For invalid or expired tokens
            TokenTypeMismatchException: When token type doesn't match
            ValueError: If token or expected_token_type is empty
        """
        if not token:
            raise ValueError("token cannot be empty")
        if not expected_token_type:
            raise ValueError("expected_token_type cannot be empty")
            
        try:
            jwt_instance = JsonWebToken(algorithms=[self._algo])
            decoded_token = jwt_instance.decode(token, self.key_provider.public_key())
            decoded_token.validate()
            
            if decoded_token['token_use'] != expected_token_type:
                raise TokenTypeMismatchException()
                
            return decoded_token
        except TokenTypeMismatchException:
            raise
        except ExpiredTokenError:
            raise TokenVerificationException("Token has expired")
        except (DecodeError, InvalidTokenError):
            raise TokenVerificationException("Invalid token")
        except Exception as e:
            raise TokenVerificationException(f"Token verification failed: {str(e)}")
        