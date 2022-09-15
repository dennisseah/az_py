from azure.core.exceptions import ServiceRequestError
from azure.storage.blob import BlobServiceClient

from azurepy.services.authentication import Authentication
from azurepy.errors.exceptions import ServiceError


class BlobStorage:
    def __init__(self, name: str):
        auth = Authentication()
        self.name = name

        self.client = BlobServiceClient(
            account_url=f"https://{name}.blob.core.windows.net",
            credential=auth.credential(),
        )

    def get_properties(self):
        try:
            prop = self.client.get_service_properties()
            return {
                "analytics_logging": self.__str_blob_analytics_logging(prop["analytics_logging"]),
                "hour_metrics": self.__str_metrics(prop["hour_metrics"]),
                "minute_metrics": self.__str_metrics(prop["minute_metrics"]),
                "cors": self.__str_cors(prop["cors"]),
                "delete_retention_policy": self.__str_retention_policy(
                    prop["delete_retention_policy"]
                ),
                "static_website": self.__str_static_website(prop["static_website"]),
                "target_version": prop["target_version"],
            }
        except ServiceRequestError:
            raise ServiceError(f"Could not get properties for blob account, {self.name}")

    def list_containers(self):
        try:
            return [self.__str_blob_container(c) for c in self.client.list_containers()]
        except ServiceRequestError:
            raise ServiceError(f"Could not list container for blob account, {self.name}")

    def __str_blob_analytics_logging(self, analytics_logging):
        return {
            "version": analytics_logging.version,
            "delete": analytics_logging.delete,
            "read": analytics_logging.read,
            "write": analytics_logging.write,
            "retention_policy": self.__str_retention_policy(analytics_logging.retention_policy),
        }

    def __str_metrics(self, metrics):
        return {
            "version": metrics.version,
            "enabled": metrics.enabled,
            "include_apis": metrics.include_apis,
            "retention_policy": self.__str_retention_policy(metrics.retention_policy),
        }

    def __str_retention_policy(self, retention_policy):
        return {
            "enabled": retention_policy.enabled,
            "days": retention_policy.days,
        }

    def __str_cors(self, cors_instance):
        def fn(cor):
            return {
                "allowed_origins": cor.allowed_origins,
                "allowed_methods": cor.allowed_methods,
                "allowed_headers": cor.allowed_headers,
                "exposed_headers": cor.exposed_headers,
                "max_age_in_seconds": cor.max_age_in_seconds,
            }

        return [fn(cor) for cor in cors_instance]

    def __str_static_website(self, static_website):
        return {
            "index_document": static_website.index_document,
            "error_document404_path": static_website.error_document404_path,
            "default_index_document_path": static_website.default_index_document_path,
        }

    def __str_blob_container(self, container):
        return {
            "name": container["name"],
            "last_modified": str(container["last_modified"]),
            "etag": container["etag"],
            "lease": self.__str_lease(container["lease"]),
            "public_access": container["public_access"],
            "has_immutability_policy": container["has_immutability_policy"],
            "deleted": container["deleted"],
            "version": container["version"],
            "has_legal_hold": container["has_legal_hold"],
            "metadata": container["metadata"],
            "encryption_scope": self.__str__container_encryption_scope(
                container["encryption_scope"]
            ),
            "immutable_storage_with_versioning_enabled": container[
                "immutable_storage_with_versioning_enabled"
            ],
        }

    def __str_lease(self, lease):
        return {
            "status": lease["status"],
            "state": lease["state"],
            "duration": lease["duration"],
        }

    def __str__container_encryption_scope(self, scope):
        return {
            "default_encryption_scope": scope.default_encryption_scope,
            "prevent_encryption_scope_override": scope.prevent_encryption_scope_override,
        }
