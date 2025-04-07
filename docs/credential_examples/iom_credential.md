# IOM Credential Examples

## Overview

IOM (I/O Module) Credentials in PowerFlex are used to authenticate to I/O modules and switches from PowerFlex Manager. This document provides detailed examples for creating, retrieving, updating, and deleting IOM Credentials using the PyPowerFlex SDK.

## Creating IOM Credentials

### Basic Creation

```python
from PyPowerFlex import PowerFlexClient
from PyPowerFlex.objects.credential import IomCredential

# Initialize the PowerFlex client
client = PowerFlexClient(
    gateway_address='powerflex-manager.example.com',
    username='admin',
    password='password',
    verify_certificate=False
)
client.initialize()

# Create a new IOM Credential
iom_cred = IomCredential(
    label="switch-admin",
    username="admin",
    password="secure_password"
)

# Add the credential to PowerFlex
result = client.credential.create(iom_cred)
print(f"Created credential with ID: {result['id']}")
```

### Creation with Error Handling

```python
from PyPowerFlex import PowerFlexClient, exceptions
from PyPowerFlex.objects.credential import IomCredential

# Initialize the PowerFlex client
client = PowerFlexClient(
    gateway_address='powerflex-manager.example.com',
    username='admin',
    password='password',
    verify_certificate=False
)
client.initialize()

try:
    # Create a new IOM Credential
    iom_cred = IomCredential(
        label="switch-admin-prod",
        username="admin",
        password="super_secure_password"
    )
    
    # Add the credential to PowerFlex
    result = client.credential.create(iom_cred)
    print(f"Created credential with ID: {result['id']}")
    
except exceptions.PowerFlexFailCreating as e:
    print(f"Failed to create credential: {e}")
except exceptions.PowerFlexClientException as e:
    print(f"Client error: {e}")
```

## Retrieving IOM Credentials

### Get All IOM Credentials

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

# Filter for IOM credentials only
iom_credentials = [cred for cred in all_credentials 
                  if 'iomCredential' in cred]

for cred in iom_credentials:
    print(f"ID: {cred['id']}, Label: {cred['label']}")
```

### Get a Specific IOM Credential

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
credential_id = "8a442bd3-75e9-48c1-9ad3-f8b3e6941c02"
try:
    credential = client.credential.get(entity_id=credential_id)
    
    # Verify it's an IOM credential
    if 'iomCredential' in credential:
        print(f"Retrieved IOM credential: {credential['label']}")
    else:
        print(f"Credential with ID {credential_id} is not an IOM credential")
        
except Exception as e:
    print(f"Error retrieving credential: {e}")
```

## Updating IOM Credentials

```python
from PyPowerFlex import PowerFlexClient
from PyPowerFlex.objects.credential import IomCredential

# Initialize the PowerFlex client
client = PowerFlexClient(
    gateway_address='powerflex-manager.example.com',
    username='admin',
    password='password',
    verify_certificate=False
)
client.initialize()

# Create an updated credential object
updated_cred = IomCredential(
    label="switch-admin-updated",
    username="admin",
    password="new_super_secure_password"
)

# Update the credential
credential_id = "8a442bd3-75e9-48c1-9ad3-f8b3e6941c02"
try:
    result = client.credential.update(credential_id, updated_cred)
    print(f"Successfully updated credential: {result['label']}")
except Exception as e:
    print(f"Error updating credential: {e}")
```

## Deleting IOM Credentials

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
credential_id = "8a442bd3-75e9-48c1-9ad3-f8b3e6941c02"
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