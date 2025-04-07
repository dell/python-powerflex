# EM Credential Examples

## Overview

EM (element Manager) Credentials in PowerFlex are used to authenticate to element Manager components. This document provides detailed examples for creating, retrieving, updating, and deleting EM Credentials using the PyPowerFlex SDK.

EM Credentials support the optional domain parameter, which can be specified when necessary for your environment.

## Creating EM Credentials

### Basic Creation

```python
from PyPowerFlex import PowerFlexClient
from PyPowerFlex.objects.credential import EmCredential

# Initialize the PowerFlex client
client = PowerFlexClient(
    gateway_address='powerflex-manager.example.com',
    username='admin',
    password='password',
    verify_certificate=False
)
client.initialize()

# Create a new EM Credential
em_cred = EmCredential(
    label="em-admin",
    username="admin",
    password="secure_password"
)

# Add the credential to PowerFlex
result = client.credential.create(em_cred)
print(f"Created credential with ID: {result['id']}")
```

### Creation with Domain Parameter

```python
from PyPowerFlex import PowerFlexClient
from PyPowerFlex.objects.credential import EmCredential

# Initialize the PowerFlex client
client = PowerFlexClient(
    gateway_address='powerflex-manager.example.com',
    username='admin',
    password='password',
    verify_certificate=False
)
client.initialize()

# Create a new EM Credential with domain
em_cred = EmCredential(
    label="em-domain-admin",
    username="admin",
    password="secure_password",
    domain="element.local"  # Domain parameter
)

# Add the credential to PowerFlex
result = client.credential.create(em_cred)
print(f"Created credential with ID: {result['id']}")
```

### Creation with Error Handling

```python
from PyPowerFlex import PowerFlexClient, exceptions
from PyPowerFlex.objects.credential import EmCredential

# Initialize the PowerFlex client
client = PowerFlexClient(
    gateway_address='powerflex-manager.example.com',
    username='admin',
    password='password',
    verify_certificate=False
)
client.initialize()

try:
    # Create a new EM Credential
    em_cred = EmCredential(
        label="em-admin-prod",
        username="admin",
        password="super_secure_password",
        domain="element.local"
    )
    
    # Add the credential to PowerFlex
    result = client.credential.create(em_cred)
    print(f"Created credential with ID: {result['id']}")
    
except exceptions.PowerFlexFailCreating as e:
    print(f"Failed to create credential: {e}")
except exceptions.PowerFlexClientException as e:
    print(f"Client error: {e}")
```

## Retrieving EM Credentials

### Get All EM Credentials

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

# Filter for EM credentials only
em_credentials = [cred for cred in all_credentials 
                 if 'emCredential' in cred]

for cred in em_credentials:
    print(f"ID: {cred['id']}, Label: {cred['label']}")
    # Domain information will also be available for EM credentials
    if 'domain' in cred:
        print(f"Domain: {cred['domain']}")
```

### Get a Specific EM Credential

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
credential_id = "9b553ce4-8a92-4f7c-b543-e91a7d2c8e05"
try:
    credential = client.credential.get(entity_id=credential_id)
    
    # Verify it's an EM credential
    if 'emCredential' in credential:
        print(f"Retrieved EM credential: {credential['label']}")
        if 'domain' in credential:
            print(f"Domain: {credential['domain']}")
    else:
        print(f"Credential with ID {credential_id} is not an EM credential")
        
except Exception as e:
    print(f"Error retrieving credential: {e}")
```

## Updating EM Credentials

### Basic Update

```python
from PyPowerFlex import PowerFlexClient
from PyPowerFlex.objects.credential import EmCredential

# Initialize the PowerFlex client
client = PowerFlexClient(
    gateway_address='powerflex-manager.example.com',
    username='admin',
    password='password',
    verify_certificate=False
)
client.initialize()

# Create an updated credential object
updated_cred = EmCredential(
    label="em-admin-updated",
    username="admin",
    password="new_super_secure_password"
)

# Update the credential
credential_id = "9b553ce4-8a92-4f7c-b543-e91a7d2c8e05"
try:
    result = client.credential.update(credential_id, updated_cred)
    print(f"Successfully updated credential: {result['label']}")
except Exception as e:
    print(f"Error updating credential: {e}")
```

### Update with Domain Change

```python
from PyPowerFlex import PowerFlexClient
from PyPowerFlex.objects.credential import EmCredential

# Initialize the PowerFlex client
client = PowerFlexClient(
    gateway_address='powerflex-manager.example.com',
    username='admin',
    password='password',
    verify_certificate=False
)
client.initialize()

# Create an updated credential object with new domain
updated_cred = EmCredential(
    label="em-admin-updated",
    username="admin",
    password="secure_password",
    domain="new-domain.local"  # Updated domain
)

# Update the credential
credential_id = "9b553ce4-8a92-4f7c-b543-e91a7d2c8e05"
try:
    result = client.credential.update(credential_id, updated_cred)
    print(f"Successfully updated credential: {result['label']}")
    print(f"New domain: {result.get('domain', 'No domain')}")
except Exception as e:
    print(f"Error updating credential: {e}")
```

## Deleting EM Credentials

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
credential_id = "9b553ce4-8a92-4f7c-b543-e91a7d2c8e05"
try:
    client.credential.delete(credential_id)
    print(f"Successfully deleted credential with ID: {credential_id}")
except Exception as e:
    print(f"Error deleting credential: {e}")
```

## Best Practices

- Use descriptive label names to easily identify the purpose of each credential
- Include domain information when applicable for your environment
- Regularly rotate credentials to maintain security
- Verify that credentials are valid before adding them to the system
- Include appropriate error handling in your code
- Remove unused credentials to maintain a clean credential inventory
- Use secure password generation for maximum security