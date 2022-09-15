from typing import List

from azure.core.exceptions import ResourceExistsError
from azure.core.polling import LROPoller
from azure.mgmt.resource.resources import ResourceManagementClient
import azure.mgmt.resource.resources.models as models

from azurepy.services.resource_providers import ResourceProviders


class Resources:
    def __init__(self, client: ResourceManagementClient):
        """Constructor

        Args:
            client (ResourceManagementClient): Resource management client
        """
        self.client = client
        self.resource_providers = ResourceProviders(client)

    def all_resources(
        self, resource_group: models.ResourceGroup
    ) -> List[models.ResourceListResult]:
        """Return all resources in a resource group.

        Args:
            resource_group (models.ResourceGroup): resource group object

        Returns:
            List[models.ResourceListResult]: List of resources
        """
        return [
            r
            for r in map(
                self.__metadata,
                self.client.resources.list_by_resource_group(
                    resource_group_name=resource_group.name,
                    expand="createdTime,changedTime",
                ),
            )
            if r.api_version is not None
        ]

    def get(self, resource_group: models.ResourceGroup, name: str) -> models.ResourceListResult:
        """Return resource in resource group.

        Args:
            resource_group (models.ResourceGroup): resource group object
            name (str): name of resource

        Returns:
            models.ResourceListResult: resource object
        """
        for r in self.all_resources(resource_group):
            if r.name == name:
                return r
        return None

    def delete(self, resource: models.ResourceListResult) -> LROPoller:
        """Delete a resource in a resource group

        Args:
            resource (models.ResourceListResult): resource group object

        Returns:
            LROPoller: Poller for the delete operation
        """
        try:
            return self.client.resources.begin_delete_by_id(resource.id, resource.api_version)
        except ResourceExistsError:
            return None

    def __metadata(self, resource: models.ResourceListResult):
        idx = resource.type.find("/")
        res_type = resource.type[0:idx] if idx != -1 else resource.type

        resource.api_version = self.resource_providers.api_version(res_type, resource.location)

        return resource
