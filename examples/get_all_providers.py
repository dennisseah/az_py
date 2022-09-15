import json

from context import azurepy  # noqa F401

from azurepy.services.azure_client import AzureClient
from azurepy.services.resource_providers import ResourceProviders

if __name__ == "__main__":
    client = AzureClient().build()
    resource_providers = ResourceProviders(client)
    print(json.dumps(resource_providers.providers(), indent=4))
