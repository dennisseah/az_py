import os
import pytest
from unittest import mock, TestCase
from unittest.mock import patch

from context import azurepy  # noqa F401

from azurepy.services.azureClient import AzureClient, SUBSCRIPTION_KEY
from azurepy.errors.exceptions import MissingEnvironmentParameterError


class TestAzureClient(TestCase):
    @mock.patch.dict(os.environ, {}, clear=True)
    def test_missing_azure_subscription(self):
        with patch.dict("os.environ"):
            if SUBSCRIPTION_KEY in os.environ:
                del os.environ[SUBSCRIPTION_KEY]
            client = AzureClient()
            with pytest.raises(MissingEnvironmentParameterError):
                client.build()

    @mock.patch.dict(os.environ, {SUBSCRIPTION_KEY: ""}, clear=True)
    def test_blank_azure_subscription(self):
        client = AzureClient()
        with pytest.raises(MissingEnvironmentParameterError):
            client.build()

    @mock.patch.dict(os.environ, {SUBSCRIPTION_KEY: "test"}, clear=True)
    def test_azure_subscription(self):
        client = AzureClient()
        assert client.build() is not None
