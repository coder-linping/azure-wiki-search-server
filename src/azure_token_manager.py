from azure.identity import AzureCliCredential, InteractiveBrowserCredential, ChainedTokenCredential
from azure.core.credentials import AccessToken
from azure.core.exceptions import ClientAuthenticationError
from typing import Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Auzre Devops resource Id
ADO_RESOURCE_ID = "499b84ac-1321-427f-aa17-267ca6975798"

class AzureTokenManager:

    def __init__(self):
        self.scope = ADO_RESOURCE_ID
        self.credential = None
        self.access_token = None

        self.credential = ChainedTokenCredential(
                AzureCliCredential(),
                InteractiveBrowserCredential()
            )
        self.authenticate()
        
    def authenticate(self) -> Optional[AccessToken]:
        if not self.credential:
            logger.error("Credential not initialized")
            return None
            
        try:
            logger.info("Attempting authentication with chained credential...")            
            token = self.credential.get_token(self.scope)
            
            self.access_token = token
            logger.info("Successfully authenticated with chained credential")
            return token
            
        except ClientAuthenticationError as e:
            logger.error(f"Chained authentication failed: {e}")
            logger.info("Make sure you're logged in with 'az login' or allow browser authentication")
            return None        
        except Exception as e:
            logger.error(f"Unexpected error with chained auth: {e}")
            return None
    
    def get_access_token(self) -> str:
        if self.access_token and self.is_token_valid():
            return self.access_token.token
        else:
            self.authenticate()
            return self.access_token.token if self.access_token else ""
    
    def is_token_valid(self) -> bool:
        if not self.access_token:
            return False
            
        import time
        return self.access_token.expires_on > time.time()
