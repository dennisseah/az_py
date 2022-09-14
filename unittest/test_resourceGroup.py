import os
from unittest import mock, TestCase
from unittest.mock import patch

from azure.core.exceptions import ResourceNotFoundError
from azure.core.polling import LROPoller

from context import azurepy, AZURE_CLIENT_BUILD_FN  # noqa F401

from azurepy.services.azureClient import AzureClient
from azurepy.services.resourceGroups import ResourceGroups


class ResourceGroupData:
    def __init__(self, name: str):
        self.name = name


class MockResourceGroups:
    def get(self, name: str):
        if name == "test":
            return ResourceGroupData(name)
        raise ResourceNotFoundError

    def list(self):
        return [ResourceGroupData("rg1"), ResourceGroupData("rg2")]

    def check_existence(self, name: str):
        return name == "test"

    def begin_delete(self, name: str):
        return LROPoller


class MockResourceManagementClient:
    def __init__(self):
        self.resource_groups = MockResourceGroups()


class TestResourceGroup(TestCase):
    @mock.patch.dict(os.environ, {}, clear=True)
    def test_get_resource_group(self):
        assert self.__test_get_resource_group("test") is not None

    @mock.patch.dict(os.environ, {}, clear=True)
    def test_get_resource_group_not_exist(self):
        assert self.__test_get_resource_group("test1") is None

    def __test_get_resource_group(self, name):
        with patch(AZURE_CLIENT_BUILD_FN) as mock_azure_client:
            mock_azure_client.return_value = MockResourceManagementClient()
            client = AzureClient().build()
            resource_groups = ResourceGroups(client)
            return resource_groups.get(name)

    @mock.patch.dict(os.environ, {}, clear=True)
    def test_list(self):
        with patch(AZURE_CLIENT_BUILD_FN) as mock_azure_client:
            mock_azure_client.return_value = MockResourceManagementClient()
            client = AzureClient().build()
            resource_groups = ResourceGroups(client)
            rgs = resource_groups.list()
            assert len(rgs) == 2

    @mock.patch.dict(os.environ, {}, clear=True)
    def test_delete_resource_group(self):
        assert self.__test_delete_resource_group("test") is not None

    @mock.patch.dict(os.environ, {}, clear=True)
    def test_delete_resource_group_not_exist(self):
        assert self.__test_delete_resource_group("test1") is None

    def __test_delete_resource_group(self, name):
        with patch("azurepy.services.azureClient.AzureClient.build") as mock_azure_client:
            mock_azure_client.return_value = MockResourceManagementClient()
            client = AzureClient().build()
            resource_groups = ResourceGroups(client)
            return resource_groups.delete(name)
