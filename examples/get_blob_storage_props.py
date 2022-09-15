import json
import sys

from context import azurepy  # noqa F401

from azurepy.services.blob_storage import BlobStorage

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("ERROR: blob storage account name is needed.")
    else:
        account_name = sys.argv[1]

        blob_storage = BlobStorage(account_name)
        print(json.dumps(blob_storage.list_containers(), indent=2))
        print(json.dumps(blob_storage.get_properties(), indent=2))
