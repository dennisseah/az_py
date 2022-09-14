# Azure Python helper services

## 1. Setup

### 1.1 Create service principal

`az ad sp create-for-rbac --name osba -o table`

and set these environment parameters
```
AZURE_CLIENT_ID
AZURE_TENANT_ID
AZURE_CLIENT_SECRET
```

for the subscription(s) that we are going to work on, and grant the permissions to the
service principal.
and set the environment parameter, `AZURE_SUBSCRIPTION_ID`

### 1.2 Install Virtual Environment

`python3 -m venv .venv`
### 1.3 Install Libraries

```
source .venv/bin/activate

pip3 install -r requirements.txt
pip3 install -r requirements-dev.txt
```


## 2. Examples

```
python3 examples/get_all_providers.py
python3 examples/get_all_resource_groups.py
python3 examples/get_all_resources.py example
python3 examples/delete_all_resources.py example
python3 examples/delete_resource_group.py example

```

## 3. Unit Test

```
python3  -m pytest --doctest-modules --cov-report term-missing --cov=azurepy unittest
```
