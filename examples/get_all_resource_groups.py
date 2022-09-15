from context import azurepy  # noqa F401

from azurepy.services.azure_client import AzureClient
from azurepy.services.resource_groups import ResourceGroups

if __name__ == "__main__":
    client = AzureClient().build()
    resource_groups = ResourceGroups(client)
    for rg in resource_groups.list():
        print(rg.name)
