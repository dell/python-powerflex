# PowerFlex Credential Management

## Overview

The PyPowerFlex SDK provides comprehensive support for managing credentials in a PowerFlex environment. This document covers the credential management functionality, including supported credential types, API operations, and usage examples.

Credential management in PowerFlex allows you to centrally store and manage authentication credentials for various components in your infrastructure, simplifying administration and improving security.

## Requirements

- PowerFlex Gateway version 4.0 or higher
- Appropriate permissions to manage credentials

## Credential Types

The PowerFlex Credential Management API supports the following credential types:

| Credential Type | Description | Domain Support |
|----------------|-------------|---------------|
| Server Credential | Used for authenticating to server components | No |
| IOM Credential | Used for I/O Module authentication | No |
| vCenter Credential | Used for authenticating to VMware vCenter | Yes |
| EM Credential | Used for Enterprise Manager authentication | Yes |
| ScaleIO Credential | Used for ScaleIO/PowerFlex component authentication | No |
| PS Credential | Used for PowerScale authentication | Yes |
| OS Credential | Used for operating system authentication | Yes |
| OS User Credential | Used for OS user-level authentication | Yes |

## Basic Operations

The credential management API supports the following operations:

- **Create**: Add a new credential to the system
- **Retrieve**: Get information about one or more credentials
- **Update**: Modify an existing credential
- **Delete**: Remove a credential from the system

## Usage Examples

### Initializing the Client

```python
from PyPowerFlex import PowerFlexClient

# Initialize the client
client = PowerFlexClient(
    gateway_address='powerflex-gateway.example.com',
    username='admin',
    password='password',
    verify_certificate=False
)
client.initialize()

# Access the credential management functionality
credential_client = client.credential
```

### Creating Credentials

The SDK provides specific classes for each credential type. Here's an example of creating a Server Credential:

```python
from PyPowerFlex.objects.credential import ServerCredential

# Create a new server credential
server_cred = ServerCredential(
    label="Web Server Admin",
    username="admin",
    password="secure_password"
)

# Add the credential to PowerFlex
result = credential_client.create(server_cred)
print(f"Created credential with ID: {result['id']}")
```

For credential types that support domains (vCenter, EM, PS, OS, OS User), you can include the domain parameter:

```python
from PyPowerFlex.objects.credential import VCenterCredential

# Create a new vCenter credential with domain
vcenter_cred = VCenterCredential(
    label="vCenter Admin",
    username="administrator@vsphere.local",
    password="secure_password",
    domain="vsphere.local"
)

# Add the credential to PowerFlex
result = credential_client.create(vcenter_cred)
```

### Retrieving Credentials

To retrieve all credentials:

```python
# Get all credentials
all_credentials = credential_client.get()
```

To retrieve a specific credential by ID:

```python
# Get a specific credential by ID
credential_id = "1234567890"
credential = credential_client.get(entity_id=credential_id)
```

### Updating Credentials

To update an existing credential:

```python
from PyPowerFlex.objects.credential import ServerCredential

# Create an updated credential object
updated_cred = ServerCredential(
    label="Updated Server Credential",
    username="admin",
    password="new_secure_password"
)

# Update the credential
credential_id = "1234567890"
result = credential_client.update(credential_id, updated_cred)
```

### Deleting Credentials

To delete a credential:

```python
# Delete a credential by ID
credential_id = "1234567890"
credential_client.delete(credential_id)
```

## Error Handling

The credential management API includes comprehensive error handling for various scenarios:

```python
from PyPowerFlex import exceptions

try:
    credentials = credential_client.get()
except exceptions.PowerFlexClientException as e:
    print(f"Error retrieving credentials: {e}")
except exceptions.ClientNotInitialized:
    print("PowerFlex client not initialized")
```

## Version Compatibility

The credential management functionality automatically checks for compatibility with your PowerFlex Gateway version:

```python
try:
    result = credential_client.create(server_cred)
except exceptions.PowerFlexClientException as e:
    if "requires PowerFlex Gateway version" in str(e):
        print("Your PowerFlex Gateway version does not support credential management")
    else:
        print(f"Error: {e}")
```

## Additional Resources

For detailed examples of each credential type, see the following:

- [Server Credential Examples](credential_examples/server_credential.md)
- [IOM Credential Examples](credential_examples/iom_credential.md)
- [vCenter Credential Examples](credential_examples/vcenter_credential.md)
- [EM Credential Examples](credential_examples/em_credential.md)
- [ScaleIO Credential Examples](credential_examples/scaleio_credential.md)
- [PS Credential Examples](credential_examples/ps_credential.md)
- [OS Credential Examples](credential_examples/os_credential.md)
- [OS User Credential Examples](credential_examples/os_user_credential.md)