# PowerFlex Credential Management Quick Start Guide

This guide provides a quick introduction to using the credential management functionality in the PyPowerFlex SDK.

## Prerequisites

- PyPowerFlex SDK version 1.15.0 or later
- PowerFlex Gateway version 4.0 or higher
- Appropriate permissions to manage credentials

## 1. Initialize the PowerFlex Client

```python
from PyPowerFlex import PowerFlexClient

client = PowerFlexClient(
    gateway_address='powerflex-gateway.example.com',
    username='admin',
    password='password',
    verify_certificate=False
)
client.initialize()

# Access the credential management functionality
cred_client = client.credential
```

## 2. Choose the Right Credential Type

The SDK supports 8 credential types:

| Type | Class Name | Domain Support | Use Case |
|------|------------|----------------|----------|
| Server | `ServerCredential` | No | iDRAC authentication |
| IOM | `IomCredential` | No | Switch authentication |
| vCenter | `VCenterCredential` | Yes | VMware vCenter authentication |
| EM | `EmCredential` | Yes | Element Manager authentication |
| ScaleIO | `ScaleIOCredential` | No | PowerFlex component authentication |
| PS | `PSCredential` | Yes | PowerScale authentication |
| OS | `OSCredential` | Yes | Operating system authentication |
| OS User | `OSUserCredential` | Yes | OS user-level authentication |

Import the credential type you need:

```python
from PyPowerFlex.objects.credential import ServerCredential
# or
from PyPowerFlex.objects.credential import VCenterCredential
# etc.
```

## 3. Create a New Credential

### Without Domain (Server, IOM, ScaleIO)

```python
# Create a server credential
server_cred = ServerCredential(
    label="idrac-admin",
    username="root",
    password="secure_password"
)

# Add it to PowerFlex
result = client.credential.create(server_cred)
credential_id = result['id']
```

### With Domain (vCenter, EM, PS, OS, OS User)

```python
# Create a vCenter credential with domain
vcenter_cred = VCenterCredential(
    label="vcenter-admin",
    username="administrator",
    password="secure_password",
    domain="vsphere.local"
)

# Add it to PowerFlex
result = client.credential.create(vcenter_cred)
credential_id = result['id']
```

## 4. Retrieve Credentials

### Get All Credentials

```python
# Get all credentials
all_credentials = client.credential.get()

# Print credential information
for cred in all_credentials:
    print(f"ID: {cred['id']}, Label: {cred['label']}")
```

### Get a Specific Credential

```python
# Get a specific credential by ID
credential = client.credential.get(entity_id="credential_id")
```

## 5. Update a Credential

```python
# Create an updated credential object
updated_cred = ServerCredential(
    label="Updated Label",
    username="admin",
    password="new_secure_password"
)

# Update the credential
client.credential.update("credential_id", updated_cred)
```

## 6. Delete a Credential

```python
# Delete a credential by ID
client.credential.delete("credential_id")
```

## 7. Error Handling

```python
from PyPowerFlex import exceptions

try:
    # Attempt a credential operation
    credentials = client.credential.get()
except exceptions.PowerFlexCredentialNotSupported as e:
    print(f"Gateway version not supported: {e}")
except exceptions.PowerFlexCredentialTypeError as e:
    print(f"Invalid credential type: {e}")
except exceptions.PowerFlexFailCredentialOperation as e:
    print(f"Operation failed: {e}")
except exceptions.PowerFlexClientException as e:
    print(f"General client error: {e}")
```

## Next Steps

For more detailed examples and usage scenarios, see:
- [Full Credential Management Documentation](credential_management.md)
- [Server Credential Examples](credential_examples/server_credential.md)
- [vCenter Credential Examples](credential_examples/vcenter_credential.md)
- [Other credential type examples in the credential_examples directory]