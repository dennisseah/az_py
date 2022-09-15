import sys
from context import azurepy  # noqa F401

from azurepy.services.azure_client import AzureClient
from azurepy.services.resource_groups import ResourceGroups

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("ERROR: resource group name is needed.")
    else:
        rg_name = sys.argv[1]

        client = AzureClient().build()
        resource_groups = ResourceGroups(client)

        op = resource_groups.delete(rg_name)
        if op:
            print(f"deleting {rg_name} ...")
            op.wait()
        else:
            print(f"{rg_name} did not exist.")
