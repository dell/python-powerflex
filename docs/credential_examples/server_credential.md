# Server Credential Examples

## Overview

Server Credentials in PowerFlex are used to authenticate to iDRACs from PowerFlex Manager. This document provides detailed examples for creating, retrieving, updating, and deleting Server Credentials using the PyPowerFlex SDK.

## Creating Server Credentials

### Basic Creation

```python
from PyPowerFlex import PowerFlexClient
from PyPowerFlex.objects.credential import ServerCredential

# Initialize the PowerFlex client
client = PowerFlexClient(
    gateway_address='powerflex-manager.example.com',
    username='admin',
    password='password',
    verify_certificate=False
)
client.initialize()

# Create a new Server Credential
server_cred = ServerCredential(
    label="idrac-root-build",
    username="admin",
    password="secure_password"
)

# Add the credential to PowerFlex
result = client.credential.create(server_cred)
print(f"Created credential with ID: {result['id']}")
```

### Creation with Error Handling

```python
from PyPowerFlex import PowerFlexClient, exceptions
from PyPowerFlex.objects.credential import ServerCredential

# Initialize the PowerFlex client
client = PowerFlexClient(
    gateway_address='powerflex-manager.example.com',
    username='admin',
    password='password',
    verify_certificate=False
)
client.initialize()

try:
    # Create a new Server Credential
    server_cred = ServerCredential(
        label="idrac-root-prod",
        username="root",
        password="super_secure_password"
    )
    
    # Add the credential to PowerFlex
    result = client.credential.create(server_cred)
    print(f"Created credential with ID: {result['id']}")
    
except exceptions.PowerFlexFailCreating as e:
    print(f"Failed to create credential: {e}")
except exceptions.PowerFlexClientException as e:
    print(f"Client error: {e}")
```

## Retrieving Server Credentials

### Get All Server Credentials

```python
from PyPowerFlex import PowerFlexClient

# Initialize the PowerFlex client
client = PowerFlexClient(
    gateway_address='powerflex-manager.example.com',
    username='admin',
    password='password',
    verify_certificate=False
)
client.initialize()

# Get all credentials
all_credentials = client.credential.get()

# Filter for server credentials only
server_credentials = [cred for cred in all_credentials 
                     if 'serverCredential' in cred]

for cred in server_credentials:
    print(f"ID: {cred['id']}, Label: {cred['label']}")
```

### Get a Specific Server Credential

```python
from PyPowerFlex import PowerFlexClient

# Initialize the PowerFlex client
client = PowerFlexClient(
    gateway_address='powerflex-manager.example.com',
    username='admin',
    password='password',
    verify_certificate=False
)
client.initialize()

# Get a specific credential by ID
credential_id = "fddd77a2-74a7-4f6e-8678-e875d71978da"
try:
    credential = client.credential.get(entity_id=credential_id)
    
    # Verify it's a server credential
    if 'serverCredential' in credential:
        print(f"Retrieved server credential: {credential['label']}")
    else:
        print(f"Credential with ID {credential_id} is not a server credential")
        
except Exception as e:
    print(f"Error retrieving credential: {e}")
```

## Updating Server Credentials

```python
from PyPowerFlex import PowerFlexClient
from PyPowerFlex.objects.credential import ServerCredential

# Initialize the PowerFlex client
client = PowerFlexClient(
    gateway_address='powerflex-manager.example.com',
    username='admin',
    password='password',
    verify_certificate=False
)
client.initialize()

# Create an updated credential object
updated_cred = ServerCredential(
    label="idrac-root-build",
    username="root",
    password="new_super_secure_password"
)

# Update the credential
credential_id = "fddd77a2-74a7-4f6e-8678-e875d71978da"
try:
    result = client.credential.update(credential_id, updated_cred)
    print(f"Successfully updated credential: {result['label']}")
except Exception as e:
    print(f"Error updating credential: {e}")
```

## Deleting Server Credentials

```python
from PyPowerFlex import PowerFlexClient

# Initialize the PowerFlex client
client = PowerFlexClient(
    gateway_address='powerflex-manager.example.com',
    username='admin',
    password='password',
    verify_certificate=False
)
client.initialize()

# Delete a credential by ID
credential_id = "fddd77a2-74a7-4f6e-8678-e875d71978da"
try:
    client.credential.delete(credential_id)
    print(f"Successfully deleted credential with ID: {credential_id}")
except Exception as e:
    print(f"Error deleting credential: {e}")
```

## Best Practices

- Use descriptive label names to easily identify the purpose of each credential
- Regularly rotate credentials to maintain security
- Verify that credentials are valid before adding them to the system
- Include appropriate error handling in your code
- Remove unused credentials to maintain a clean credential inventory
- Use secure password generation for maximum security