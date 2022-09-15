import os
import pytest

from azure.core.exceptions import ServiceRequestError

from unittest import mock, TestCase
from unittest.mock import patch, MagicMock

from context import azurepy  # noqa F401

from azurepy.errors.exceptions import ServiceError
from azurepy.services.blob_storage import BlobStorage


class MockRetentionPolicy:
    def __init__(self, enabled, days):
        self.enabled = enabled
        self.days = days


class MockAnalyticsLogging:
    def __init__(self):
        self.version = "1.0"
        self.delete = False
        self.read = False
        self.write = False
        self.retention_policy = MockRetentionPolicy(False, None)


class MockMetrics:
    def __init__(self, version, enabled, include_apis, retention_policy):
        self.version = version
        self.enabled = enabled
        self.include_apis = include_apis
        self.retention_policy = retention_policy


class MockStaticWebsite:
    def __init__(self):
        self.index_document = None
        self.error_document404_path = None
        self.default_index_document_path = None


class MockCors:
    def __init__(self):
        self.allowed_origins = False
        self.allowed_methods = True
        self.allowed_headers = False
        self.exposed_headers = False
        self.max_age_in_seconds = 10


class MockEncryptionScope:
    def __init__(self):
        self.default_encryption_scope = "$account-encryption-key"
        self.prevent_encryption_scope_override = False


def mock_get_containers():
    return [
        {
            "name": "container",
            "last_modified": "2022-09-15 01:41:49+00:00",
            "etag": '"0x8DA96BB75175BEE"',
            "lease": {"status": "unlocked", "state": "available", "duration": None},
            "public_access": "blob",
            "has_immutability_policy": False,
            "deleted": None,
            "version": None,
            "has_legal_hold": False,
            "metadata": None,
            "encryption_scope": MockEncryptionScope(),
            "immutable_storage_with_versioning_enabled": False,
        }
    ]


def mock_get_service_properties():
    return {
        "analytics_logging": MockAnalyticsLogging(),
        "hour_metrics": MockMetrics("1.0", True, True, MockRetentionPolicy(True, 7)),
        "minute_metrics": MockMetrics("1.0", False, None, MockRetentionPolicy(False, None)),
        "cors": [MockCors()],
        "delete_retention_policy": MockRetentionPolicy(False, None),
        "static_website": MockStaticWebsite(),
        "target_version": "4.0",
    }


class TestBlobStorage(TestCase):
    @mock.patch.dict(os.environ, {}, clear=True)
    def test_get_properties(self):
        with patch("azure.storage.blob.BlobServiceClient.get_service_properties") as mock_get_props:
            mock_get_props.return_value = mock_get_service_properties()

            blob_storage = BlobStorage("test")
            prop = blob_storage.get_properties()
            assert "analytics_logging" in prop
            assert "hour_metrics" in prop
            assert "minute_metrics" in prop
            assert "cors" in prop
            assert "delete_retention_policy" in prop
            assert "static_website" in prop
            assert "target_version" in prop

    @mock.patch.dict(os.environ, {}, clear=True)
    def test_get_properties_no_exist(self):
        with patch("azure.storage.blob.BlobServiceClient.get_service_properties") as mock_get_props:
            mock_get_props.side_effect = ServiceRequestError("missing")

            blob_storage = BlobStorage("test")
            with pytest.raises(
                ServiceError, match="Could not get properties for blob account, test"
            ):
                blob_storage.get_properties()

    @mock.patch.dict(os.environ, {}, clear=True)
    def test_list_containers(self):
        with patch("azure.storage.blob.BlobServiceClient.list_containers") as mock_list_containers:
            mock_list_containers.return_value = mock_get_containers()

            blob_storage = BlobStorage("test")
            containers = blob_storage.list_containers()
            assert len(containers) == 1
            container = containers[0]
            assert "name" in container
            assert "last_modified" in container
            assert "etag" in container
            assert "lease" in container
            assert "public_access" in container
            assert "has_immutability_policy" in container
            assert "deleted" in container
            assert "version" in container
            assert "has_legal_hold" in container
            assert "metadata" in container
            assert "encryption_scope" in container
            assert "immutable_storage_with_versioning_enabled" in container

    @mock.patch.dict(os.environ, {}, clear=True)
    def test_list_containers_error(self):
        with patch("azure.storage.blob.BlobServiceClient.list_containers") as mock_list_containers:
            mock_list_containers.side_effect = ServiceRequestError("missing")

            blob_storage = BlobStorage("test")
            with pytest.raises(
                ServiceError, match="Could not list container for blob account, test"
            ):
                blob_storage.list_containers()
