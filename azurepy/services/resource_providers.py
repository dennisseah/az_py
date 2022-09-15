from azure.mgmt.resource.resources import ResourceManagementClient


class ResourceProviders:
    __api_versions_cache = None

    def __init__(self, client: ResourceManagementClient):
        """Constructor

        Args:
            client (ResourceManagementClient): Resource management client
        """
        self.client = client

    def providers(self):
        """Returns all Azure providers

        Returns:
            list: list of provider names
        """
        cache = self.__get_api_versions_cache()
        namespaces = sorted(set([x["namespace"] for x in cache]))
        return list(map(lambda ns: ".".join([p.capitalize() for p in ns.split(".")]), namespaces))

    def api_version(self, res_type: str, res_loc: str) -> str:
        """Returns API version string of an Azure resource

        Args:
            res_type (str): resource type name
            res_loc (str): location of the resource

        Returns:
            str: API version string
        """
        cache = self.__get_api_versions_cache()
        matches = [x for x in cache if x["namespace"] == res_type.lower()]

        for match in matches:
            if res_loc.lower() in match["locations"]:
                return match["api_version"]

        return None

    def __get_api_versions_cache(self):
        if self.__api_versions_cache:
            return self.__api_versions_cache

        self.__api_versions_cache = []

        for provider in self.client.providers.list():
            ns = provider.namespace.lower()

            for resource_type in provider.resource_types:
                if len(resource_type.api_versions) > 0:
                    self.__api_versions_cache.append(
                        {
                            "namespace": ns,
                            "api_version": resource_type.api_versions[0],
                            "locations": [loc.lower().replace(" ", "") for loc in resource_type.locations],
                        }
                    )

        return self.__api_versions_cache
