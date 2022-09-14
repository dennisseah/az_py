import sys
from context import azurepy  # noqa F401

from azurepy.services.azureClient import AzureClient
from azurepy.services.resourceGroups import ResourceGroups
from azurepy.services.resources import Resources


def __del_resources(to_delete):
    leftover = []

    while len(to_delete) > 0:
        r = to_delete.pop(0)

        poller = resources.delete(r)
        if poller:
            poller.wait()
        else:
            leftover.append(r)

    return leftover


def _del_all_resources(to_delete):
    orig_cnt = len(to_delete)
    final_cnt = orig_cnt - 1

    while final_cnt > 0 and final_cnt < orig_cnt:
        orig_cnt = len(to_delete)
        to_delete = __del_resources(to_delete)
        final_cnt = len(to_delete)

    return final_cnt


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
            to_delete = resources.all_resources(res_group)

            if len(to_delete) == 0:
                print(f"there were no resource in {rg_name}.")
            else:
                leftover = _del_all_resources(to_delete)

                if leftover > 0:
                    print(f"unable to delete {leftover} resources in {rg_name}.")
                else:
                    print(f"all resources in {rg_name} were deleted.")
