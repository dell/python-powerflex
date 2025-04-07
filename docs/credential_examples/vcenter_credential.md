# vCenter Credential Examples

## Overview

vCenter Credentials in PowerFlex are used to authenticate to VMware vCenter Server instances from PowerFlex Manager. vCenter credentials support the optional domain parameter, which can be used when authenticating against domain-joined vCenter environments. This document provides detailed examples for creating, retrieving, updating, and deleting vCenter Credentials using the PyPowerFlex SDK.

## Creating vCenter Credentials

### Basic Creation Without Domain

```python
from PyPowerFlex import PowerFlexClient
from PyPowerFlex.objects.credential import VCenterCredential

# Initialize the PowerFlex client
client = PowerFlexClient(
    gateway_address='powerflex-gateway.example.com',
    username='admin',
    password='password',
    verify_certificate=False
)
client.initialize()

# Create a new vCenter Credential without domain
vcenter_cred = VCenterCredential(
    label="vcenter-admin-vsphere-local",
    username="administrator@vsphere.local",
    password="super_secure_password"
)

# Add the credential to PowerFlex
result = client.credential.create(vcenter_cred)
print(f"Created credential with ID: {result['id']}")
```

### Creation With Domain Parameter

```python
from PyPowerFlex import PowerFlexClient
from PyPowerFlex.objects.credential import VCenterCredential

# Initialize the PowerFlex client
client = PowerFlexClient(
    gateway_address='powerflex-gateway.example.com',
    username='admin',
    password='password',
    verify_certificate=False
)
client.initialize()

# Create a new vCenter Credential with domain
vcenter_cred = VCenterCredential(
    label="vcenter-vcadmin-example",
    username="vcadmin",
    password="super_secure_password",
    domain="corp.example.com"  # Domain parameter
)

# Add the credential to PowerFlex
result = client.credential.create(vcenter_cred)
print(f"Created credential with ID: {result['id']}")
```

### Domain-Based Authentication Options

vCenter credentials can be configured in multiple ways depending on your authentication requirements:

**Option 1: Username with domain suffix**
```python
vcenter_cred = VCenterCredential(
    label="vcenter-admin-vsphere-local",
    username="administrator@vsphere.local",  # Domain included in username
    password="super_secure_password"
)
```

**Option 2: Separate username and domain**
```python
vcenter_cred = VCenterCredential(
    label="vcenter-admin-vsphere-local",
    username="administrator",  # Just the username
    password="super_secure_password",
    domain="vsphere.local"     # Domain as separate parameter
)
```

**Option 3: Domain\\username format**
```python
vcenter_cred = VCenterCredential(
    label="vcenter-admin-example",
    username="EXAMPLE\\administrator",  # Domain\username format
    password="super_secure_password"
)
```

## Retrieving vCenter Credentials

### Get All vCenter Credentials

```python
from PyPowerFlex import PowerFlexClient

# Initialize the PowerFlex client
client = PowerFlexClient(
    gateway_address='powerflex-gateway.example.com',
    username='admin',
    password='password',
    verify_certificate=False
)
client.initialize()

# Get all credentials
all_credentials = client.credential.get()

# Filter for vCenter credentials only
vcenter_credentials = [cred for cred in all_credentials 
                      if 'vCenterCredential' in cred]

for cred in vcenter_credentials:
    print(f"ID: {cred['id']}, Label: {cred['label']}")
    
    # Check if domain is present
    if 'domain' in cred and cred['domain']:
        print(f"  Domain: {cred['domain']}")
    print(f"  Username: {cred['username']}")
```

### Get a Specific vCenter Credential

```python
from PyPowerFlex import PowerFlexClient

# Initialize the PowerFlex client
client = PowerFlexClient(
    gateway_address='powerflex-gateway.example.com',
    username='admin',
    password='password',
    verify_certificate=False
)
client.initialize()

# Get a specific credential by ID
credential_id = "fddd77a2-74a7-4f6e-8678-e875d71978da"
try:
    credential = client.credential.get(entity_id=credential_id)
    
    # Verify it's a vCenter credential
    if 'vCenterCredential' in credential:
        print(f"Retrieved vCenter credential: {credential['label']}")
        if 'domain' in credential and credential['domain']:
            print(f"Domain: {credential['domain']}")
    else:
        print(f"Credential with ID {credential_id} is not a vCenter credential")
        
except Exception as e:
    print(f"Error retrieving credential: {e}")
```

## Updating vCenter Credentials

### Update With Domain Parameter

```python
from PyPowerFlex import PowerFlexClient
from PyPowerFlex.objects.credential import VCenterCredential

# Initialize the PowerFlex client
client = PowerFlexClient(
    gateway_address='powerflex-gateway.example.com',
    username='admin',
    password='password',
    verify_certificate=False
)
client.initialize()

# Create an updated credential object with domain
updated_cred = VCenterCredential(
    label="vcenter-admin-new-example",
    username="admin",
    password="new_super_secure_password",
    domain="new.example.com"  # Updated domain
)

# Update the credential
credential_id = "fddd77a2-74a7-4f6e-8678-e875d71978da"
try:
    result = client.credential.update(credential_id, updated_cred)
    print(f"Successfully updated credential: {result['label']}")
    if 'domain' in result and result['domain']:
        print(f"Updated domain: {result['domain']}")
except Exception as e:
    print(f"Error updating credential: {e}")
```

### Removing a Domain from a Credential

To remove a domain from a vCenter credential, provide an empty string for the domain parameter:

```python
# Create an updated credential object with empty domain
updated_cred = VCenterCredential(
    label="vcenter-admin-vsphere-local",
    username="admin@vsphere.local",  # Include domain in username if needed
    password="super_secure_password",
    domain=""  # Empty string removes the domain
)

# Update the credential
result = client.credential.update(credential_id, updated_cred)
```

## Deleting vCenter Credentials

```python
from PyPowerFlex import PowerFlexClient

# Initialize the PowerFlex client
client = PowerFlexClient(
    gateway_address='powerflex-gateway.example.com',
    username='admin',
    password='password',
    verify_certificate=False
)
client.initialize()

# Delete a credential by ID
credential_id = "fddd77a2-74a7-4f6e-8678-e875d71978da"
try:
    client.credential.delete(credential_id)
    print(f"Successfully deleted vCenter credential with ID: {credential_id}")
except Exception as e:
    print(f"Error deleting credential: {e}")
```

## Best Practices for vCenter Credentials

- Use the domain parameter when authenticating to domain-joined vCenter servers
- Consider security implications when choosing between domain formats
- For non-domain environments, use the username@domain.com format
- Regularly rotate vCenter credentials to maintain security
- Verify that credentials are valid before adding them to the system
- Include appropriate error handling in your code
- Remove unused credentials to maintain a clean credential inventory