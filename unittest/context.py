import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import azurepy  # noqa: F401

AZURE_CLIENT_BUILD_FN = "azurepy.services.azureClient.AzureClient.build"
