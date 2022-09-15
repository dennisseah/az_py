import sys

from context import azurepy  # noqa F401

from azurepy.services.azure_client import AzureClient
from azurepy.services.resource_groups import ResourceGroups
from azurepy.services.resources import Resources

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("ERROR: resource group name is needed.")
    else:
        rg_name = sys.argv[1]

        client = AzureClient().build()
        resource_groups = ResourceGroups(client)
        resources = Resources(client)

        res_group = resource_groups.get(rg_name)

        if not res_group:
            print(f"{rg_name} did not exist.")
        else:
            res = resources.all_resources(res_group)

            if len(res) == 0:
                print(f"there were no resource in {rg_name}.")
            else:
                for r in res:
                    print(r)
