import os

from azure.mgmt.resource.resources import ResourceManagementClient

from azurepy.services.authentication import Authentication
from azurepy.errors.exceptions import MissingEnvironmentParameterError

SUBSCRIPTION_KEY = "AZURE_SUBSCRIPTION_ID"


class AzureClient:
    def build(self) -> ResourceManagementClient:
        """Build and return a Azure resource management client.

        Returns:
            ResourceManagementClient: Azure resource management client.
        """
        subscription_id = os.getenv(SUBSCRIPTION_KEY)

        if not subscription_id:
            raise MissingEnvironmentParameterError(f"{SUBSCRIPTION_KEY} environment parameter value was missing.")

        authentication = Authentication()
        return ResourceManagementClient(authentication.credential(), subscription_id)
