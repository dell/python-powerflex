# PyPowerFlex

Python SDK for Dell EMC PowerFlex.

Supports PowerFlex (VxFlex OS) version 3.0 and later.

## Installation and usage

### Installation

```shell script
python setup.py install
```

### Usage

#### Configuration options

| Option | Description |
| :---: | :---: |    
| gateway_address | (str) PowerFlex API address. | 
| gateway_port | (int) PowerFlex API port. **Default**: 443. | 
| username | (str) PowerFlex API username. |
| password | (str) PowerFlex API password. |
| verify_certificate | (bool) Verify server's certificate. **Default**: False. |
| certificate_path | (str) Path to server's certificate. **Default**: None. |
| timeout | (int) Timeout for PowerFlex API request. **Default**: 120.
| log_level | (int) Logging level (e. g. logging.DEBUG). **Default**: logging.ERROR. |

#### Available resources

* Device
* FaultSet
* ProtectionDomain
* Sdc
* Sds
* SnapshotPolicy
* StoragePool
* System
* Volume

#### Initialize PowerFlex client

```python
from PyPowerFlex import PowerFlexClient

client = PowerFlexClient(gateway_address='1.2.3.4', 
                         gateway_port=443, 
                         username='admin', 
                         password='admin')
client.initialize()
```

#### Filtering and fields querying

SDK supports flat filtering and fields querying.

```python
from PyPowerFlex.objects.device import MediaType

client.device.get(filter_fields={'mediaType': MediaType.ssd, 
                                 'name': ['/dev/sdd', '/dev/sde']}, 
                  fields=['id', 'name', 'mediaType'])

[{'id': '3eddd9dd00010003', 'mediaType': 'SSD', 'name': '/dev/sde'},
 {'id': '3edcd9d800000002', 'mediaType': 'SSD', 'name': '/dev/sdd'},
 {'id': '3edcd9d900000003', 'mediaType': 'SSD', 'name': '/dev/sde'},
 {'id': '3edd00e900010002', 'mediaType': 'SSD', 'name': '/dev/sdd'},
 {'id': '3eded9e000020002', 'mediaType': 'SSD', 'name': '/dev/sdd'},
 {'id': '3eded9e100020003', 'mediaType': 'SSD', 'name': '/dev/sde'}]
```

#### Examples

```python
from PyPowerFlex.objects.device import MediaType

# Create device
client.device.create('/dev/sdd', 
                     sds_id='63471cdd00000001', 
                     media_type=MediaType.ssd, 
                     storage_pool_id='889dd7b900000000',
                     name='/dev/sdd')

# Rename device
client.device.get(filter_fields={'name': '/dev/sdd', 'id': '3eddd9dc00010002'}, 
                  fields=['name', 'id'])      

[{'name': '/dev/sdd', 'id': '3eddd9dc00010002'}]

client.device.rename('3eddd9dc00010002', '/dev/sdd-renamed') 

client.device.get(filter_fields={'id': '3eddd9dc00010002'}, 
                  fields=['name', 'id'])  

[{'name': '/dev/sdd-renamed', 'id': '3eddd9dc00010002'}]

# Remove device
client.device.delete('3eddd9dc00010002')

{}

# Get Protection Domain related SDSs
client.protection_domain.get_sdss('b922fb3700000000', fields=['ipList', 'name'])

[{'ipList': [{'ip': '192.168.221.182', 'role': 'all'},
             {'ip': '172.16.221.182', 'role': 'all'}]},
 {'ipList': [{'ip': '192.168.221.181', 'role': 'all'},
             {'ip': '172.16.221.181', 'role': 'all'}]},
 {'ipList': [{'ip': '192.168.221.180', 'role': 'all'},
             {'ip': '172.16.221.180', 'role': 'all'}]}]

# Add SDS IP-address
from PyPowerFlex.objects.sds import SdsIp
from PyPowerFlex.objects.sds import SdsIpRoles

client.sds.add_ip('63471cdc00000000', SdsIp('1.2.3.4', SdsIpRoles.sdc_only))

client.sds.get(filter_fields={'id': '63471cdc00000000'}, fields=['id', 'ipList'])

[{'id': '63471cdc00000000',
  'ipList': [{'ip': '192.168.221.180', 'role': 'all'},
             {'ip': '172.16.221.180', 'role': 'all'},
             {'ip': '1.2.3.4', 'role': 'sdcOnly'}]}]

# Set SDS IP-address role
client.sds.set_ip_role('63471cdc00000000', '1.2.3.4', SdsIpRoles.sds_only, force=True)

[{'id': '63471cdc00000000',
  'ipList': [{'ip': '192.168.221.180', 'role': 'all'},
             {'ip': '172.16.221.180', 'role': 'all'},
             {'ip': '1.2.3.4', 'role': 'sdsOnly'}]}]

# Remove SDS IP-address
client.sds.remove_ip('63471cdc00000000', '1.2.3.4')

[{'id': '63471cdc00000000',
  'ipList': [{'ip': '192.168.221.180', 'role': 'all'},
             {'ip': '172.16.221.180', 'role': 'all'}]}]

# Create Snapshot Policy
client.snapshot_policy.create(15, [3, 4, 5, 6])

# Snapshot volumes
from PyPowerFlex.objects.system import SnapshotDef

system_id = client.system.get(fields=['id'])[0]['id']
client.system.snapshot_volumes(system_id, 
                               [SnapshotDef('afa52f0c00000003', 'snap1'), 
                                SnapshotDef('afa52f0c00000003', 'snap2')])

{'snapshotGroupId': '5aaf81e800000002', 'volumeIdList': ['afa5561900000007', 'afa5561a00000008']}

# Remove ConsistencyGroup snapshot
client.system.remove_cg_snapshots(system_id, '5aaf81e800000002')

{'numberOfVolumes': 2}
```
