from typing import Iterable

from azure.mgmt.resource.resources import ResourceManagementClient
from azure.core.polling import LROPoller
from azure.core.exceptions import ResourceNotFoundError
import azure.mgmt.resource.resources.models as models


class ResourceGroups:
    def __init__(self, client: ResourceManagementClient):
        """Constructor

        Args:
            client (ResourceManagementClient): Resource management client
        """
        self.client = client

    def get(self, name: str) -> models.ResourceGroup:
        """Return resource group instance if exist

        Args:
            name (str): name of resource group

        Returns:
            models.ResourceGroup: resource group instance
        """
        try:
            return self.client.resource_groups.get(name)
        except ResourceNotFoundError:
            return None

    def list(self) -> Iterable["models.ResourceGroupListResult"]:
        """List all resource groups in the subscription.

        Returns:
            iterator: iterator of models.ResourceGroupListResult
        """
        return self.client.resource_groups.list()

    def delete(self, name: str) -> LROPoller:
        """Delete a resource group.

        Args:
            name (str): name of the resource group

        Returns:
            LROPoller: poller
        """
        return (
            self.client.resource_groups.begin_delete(name)
            if self.client.resource_groups.check_existence(name)
            else None
        )
