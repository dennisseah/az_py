import os

from azure.core.polling import LROPoller
from azure.core.exceptions import ResourceExistsError

from unittest import TestCase
from unittest.mock import MagicMock, patch

from context import AZURE_CLIENT_BUILD_FN, azurepy  # noqa F401

from azurepy.services.azure_client import AzureClient
from azurepy.services.resource_providers import ResourceProviders
from azurepy.services.resources import Resources


class ResourceTypeData:
    def __init__(self, api_versions, locations):
        self.api_versions = api_versions
        self.locations = locations


class ResourceData:
    def __init__(self, name, type, location):
        self.name = name
        self.type = type
        self.location = location


class MockResources:
    def list_by_resource_group(self, resource_group_name: str, expand=str):
        return [ResourceData("group1", "Microsoft.OperationsManagement/solutions", "westus2")]

    def begin_delete_by_id(self, id, api_version):
        if id == "test":
            return LROPoller

        raise ResourceExistsError


class MockResourceManagementClient:
    def __init__(self):
        self.resources = MockResources()


class TestResources(TestCase):
    @patch.dict(os.environ, {}, clear=True)
    @patch.object(ResourceProviders, "api_version", MagicMock(return_value="1.0.2"))
    def test_get_all_resources(self):
        with patch(AZURE_CLIENT_BUILD_FN) as mock_azure_client:
            mock_resource_group = MagicMock()
            mock_resource_group.name.return_value = "test"

            mock_azure_client.return_value = MockResourceManagementClient()
            client = AzureClient().build()
            rg = Resources(client)
            assert len(rg.all_resources(resource_group=mock_resource_group)) == 1

    @patch.dict(os.environ, {}, clear=True)
    @patch.object(ResourceProviders, "api_version", MagicMock(return_value="1.0.2"))
    def test_get_resource(self):
        assert self.__test_get_resource_not_exist("group1") is not None

    @patch.dict(os.environ, {}, clear=True)
    @patch.object(ResourceProviders, "api_version", MagicMock(return_value="1.0.2"))
    def test_get_resource_not_exist(self):
        assert self.__test_get_resource_not_exist("group2") is None

    def __test_get_resource_not_exist(self, name):
        with patch(AZURE_CLIENT_BUILD_FN) as mock_azure_client:
            mock_resource_group = MagicMock()
            mock_resource_group.name.return_value = "test"

            mock_azure_client.return_value = MockResourceManagementClient()
            client = AzureClient().build()
            res = Resources(client)
            return res.get(resource_group=mock_resource_group, name=name)

    @patch.dict(os.environ, {}, clear=True)
    def test_delete(self):
        assert self.__test_delete("test") is not None

    @patch.dict(os.environ, {}, clear=True)
    def test_delete_no_exist(self):
        assert self.__test_delete("test1") is None

    def __test_delete(self, id):
        with patch(AZURE_CLIENT_BUILD_FN) as mock_azure_client:
            mock_resource_group = MagicMock()
            mock_resource_group.name.return_value = "test"

            mock_azure_client.return_value = MockResourceManagementClient()
            client = AzureClient().build()
            res = Resources(client)

            mock_resource = MagicMock()
            mock_resource.id = id
            mock_resource.api_version = "1.0.2"
            return res.delete(mock_resource)
