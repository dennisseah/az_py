from azure.identity import DefaultAzureCredential

# TODO: handle different kind of authentication method.


class Authentication:
    def credential(self):
        return DefaultAzureCredential()
