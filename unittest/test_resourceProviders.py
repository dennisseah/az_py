import os
from unittest import mock, TestCase
from unittest.mock import patch

from context import AZURE_CLIENT_BUILD_FN, azurepy  # noqa F401

from azurepy.services.azureClient import AzureClient
from azurepy.services.resourceProviders import ResourceProviders


class ResourceTypeData:
    def __init__(self, api_versions, locations):
        self.api_versions = api_versions
        self.locations = locations


class ProviderData:
    def __init__(self, namespace):
        self.namespace = namespace
        self.resource_types = [
            ResourceTypeData(
                api_versions=["1.0.2", "1.0.1"],
                locations=["East US", "West US", "West US 2"],
            )
        ]


class MockProviders:
    def list(self):
        return [ProviderData("Provider1")]


class MockResourceManagementClient:
    def __init__(self):
        self.providers = MockProviders()


class TestResourceProviders(TestCase):
    @mock.patch.dict(os.environ, {}, clear=True)
    def test_get_providers(self):
        with patch(AZURE_CLIENT_BUILD_FN) as mock_azure_client:
            mock_azure_client.return_value = MockResourceManagementClient()
            client = AzureClient().build()
            rp = ResourceProviders(client)
            assert rp.providers()[0] == "Provider1"

    @mock.patch.dict(os.environ, {}, clear=True)
    def test_get_api_version(self):
        with patch(AZURE_CLIENT_BUILD_FN) as mock_azure_client:
            mock_azure_client.return_value = MockResourceManagementClient()
            client = AzureClient().build()
            rp = ResourceProviders(client)
            assert rp.api_version("Provider1", "westus") == "1.0.2"
            assert rp.api_version("Provider1", "westus2") == "1.0.2"

    @mock.patch.dict(os.environ, {}, clear=True)
    def test_get_api_version_no_match(self):
        with patch(AZURE_CLIENT_BUILD_FN) as mock_azure_client:
            mock_azure_client.return_value = MockResourceManagementClient()
            client = AzureClient().build()
            rp = ResourceProviders(client)
            assert rp.api_version("Provider1", "asia") is None
