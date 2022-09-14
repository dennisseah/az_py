from context import azurepy  # noqa F401

from azurepy.services.azureClient import AzureClient
from azurepy.services.resourceGroups import ResourceGroups

if __name__ == "__main__":
    client = AzureClient().build()
    resource_groups = ResourceGroups(client)
    for rg in resource_groups.list():
        print(rg.name)
