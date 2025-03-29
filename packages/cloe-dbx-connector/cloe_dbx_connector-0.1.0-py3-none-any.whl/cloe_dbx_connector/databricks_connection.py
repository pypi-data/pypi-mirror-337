import logging
import os

from databricks.sdk import WorkspaceClient
from databricks.sdk.errors import DatabricksError
from dotenv import load_dotenv
from pydantic import BaseModel

# Load environment variables
load_dotenv(override=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("databricks_connector.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


class DatabricksConnector(BaseModel):
    """
    Handles authentification and connection to Databricks.
    Supports both Service Principal and Token-based authentication.
    """

    host: str | None = None
    token: str | None = None
    client_id: str | None = None
    client_secret: str | None = None
    tenant_id: str | None = None

    @classmethod
    def from_env(cls):
        """Factory method to create an instance from environment variables"""
        host = os.getenv("CLOE_DBX_HOST")
        token = os.getenv("CLOE_DBX_TOKEN")
        client_id = os.getenv("CLOE_DBX_CLIENT_ID")
        client_secret = os.getenv("CLOE_DBX_CLIENT_SECRET")
        tenant_id = os.getenv("CLOE_DBX_TENANT_ID")

        if not host:
            raise ValueError("Authentication credentials missing: Please provide a host.")

        if not token and not (client_id and client_secret and tenant_id):
            raise ValueError(
                "Authentication credentials missing: Please provide either a token or service principal details."
            )

        return cls.model_construct(
            host=host,
            token=token,
            client_id=client_id,
            client_secret=client_secret,
            tenant_id=tenant_id,
        )

    def get_workspace_client(self) -> WorkspaceClient:
        """
        Establishes a connection to Databricks.
        """
        auth_params = self.get_auth_params()
        return WorkspaceClient(**auth_params)

    def get_auth_params(self) -> dict:
        """
        Returns the correct authentication parameters and validates input.
        """
        if not self.host or not self.host.startswith("https://"):
            raise ValueError("Invalid Databricks host. Ensure it starts with 'https://'.")

        if self.token:
            return {"host": self.host, "token": self.token}

        if self.client_id and self.client_secret and self.tenant_id:
            return {
                "host": self.host,
                "azure_client_id": self.client_id,
                "azure_client_secret": self.client_secret,
                "azure_tenant_id": self.tenant_id,
            }

        raise ValueError("Authentication credentials missing: Provide either a token or service principal details.")

    def list_catalogs(self):
        """
        Fetches all catalogs from Databricks and returns them.
        """
        try:
            client = self.get_workspace_client()
            catalogs = client.catalogs.list()

            if not catalogs:
                logger.info("No catalogs found in the workspace.")
                return []

            catalog_names = [catalog.name for catalog in catalogs]
            logger.info("Available Catalogs in Databricks:")
            for catalog in catalog_names:
                logger.info(f" - {catalog}")

            return catalog_names

        except DatabricksError as e:
            logger.error(f"Failed to fetch catalogs: {e}")
            return []
        except Exception as error:
            logger.error(f"Unexpected Error: {error}")
            return []
