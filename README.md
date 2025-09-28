# PyPowerFlex

Python SDK for Dell PowerFlex.

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
| timeout | (int) Timeout for PowerFlex API request **Default**: 120.
| log_level | (int) Logging level (e. g. logging.DEBUG). **Default**: logging.ERROR. |

#### Available resources

Common
* Deployment
* FirmwareRepository
* NvmeHost
* ManagedDevice
* Sdc
* Sdt
* ServiceTemplate

Gen1
* AccelerationPool
* Device
* FaultSet
* ProtectionDomain
* ReplicationConsistencyGroup
* ReplicationPair
* Sds
* SnapshotPolicy
* StoragePool
* System
* Volume

Gen2
* DeviceGroup
* Device
* ProtectionDomain
* SnapshotPolicy
* StorageNode
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
# Create device
from PyPowerFlex.objects.device import MediaType
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
[{'ipList': [{'ip': '192.100.xxx.xxx', 'role': 'all'},
             {'ip': '172.160.xxx.xxx', 'role': 'sdcOnly'}]},
 {'ipList': [{'ip': '192.101.xxx.xxx', 'role': 'all'},
             {'ip': '172.161.xxx.xxx', 'role': 'sdcOnly'}]},
 {'ipList': [{'ip': '192.102.xxx.xxx', 'role': 'all'},
             {'ip': '172.162.xxx.xxx', 'role': 'sdcOnly'}]}]

# Delete protection domain
client.protection_domain.delete('9300c1f900000000')
{}

# Add SDS IP-address
from PyPowerFlex.objects.sds import SdsIp
from PyPowerFlex.objects.sds import SdsIpRoles

client.sds.add_ip('63471cdc00000000', SdsIp('172.17.xxx.xxx', SdsIpRoles.sdc_only))
client.sds.get(filter_fields={'id': '63471cdc00000000'}, fields=['id', 'ipList'])
[{'id': '63471cdc00000000',
  'ipList': [{'ip': '192.168.xxx.xxx', 'role': 'all'},
             {'ip': '172.16.xxx.xxx', 'role': 'sdcOnly'},
             {'ip': '172.17.xxx.xxx', 'role': 'sdcOnly'}]}]

# Set SDS IP-address role
client.sds.set_ip_role('63471cdc00000000', '172.17.xxx.xxx', SdsIpRoles.sds_only, force=True)
[{'id': '63471cdc00000000',
  'ipList': [{'ip': '192.168.xxx.xxx', 'role': 'all'},
             {'ip': '172.16.xxx.xxx', 'role': 'sdcOnly'},
             {'ip': '172.17.xxx.xxx', 'role': 'sdsOnly'}]}]

# Remove SDS IP-address
client.sds.remove_ip('63471cdc00000000', '172.16.xxx.xxx')
[{'id': '63471cdc00000000',
  'ipList': [{'ip': '192.168.xxx.xxx', 'role': 'all'},
             {'ip': '172.17.xxx.xxx', 'role': 'sdcOnly'}]}]

# Create snapshot policy
client.snapshot_policy.create(15, [3, 4, 5, 6])

# Rename snapshot policy
client.snapshot_policy.rename('f047913500000000', 'SnapshotPolicy_sp2')

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

# Rename storage pool
client.storage_pool.rename('dbd4dbcd00000000', 'StoragePool_sp2')
client.storage_pool.get(filter_fields={'id': 'dbd4dbcd00000000'},
                        fields=['name', 'id'])
[{'name': 'StoragePool_sp2', 'id': 'dbd4dbcd00000000'}]

# Set media tye for storage pool
from PyPowerFlex.objects.storage_pool import MediaType
client.storage_pool.set_media_type(storage_pool_id='dbd4dbcd00000000',
                                   media_type=MediaType.ssd,
                                   override_device_configuration=None)

# Create acceleration pool
from PyPowerFlex.objects.acceleration_pool import MediaType
client.acceleration_pool.create(media_type=MediaType.ssd,
                                protection_domain_id='1caf743100000000',
                                name='ACP_SSD',
                                is_rfcache=True)
client.acceleration_pool.get(filter_fields={'id': '9c8c5c7800000001'}, 
                             fields=['name', 'id'])
[{'name': 'ACP_SSD', 'id': '9c8c5c7800000001'}]

# Delete acceleration pool
client.acceleration_pool.delete('9c8c5c7800000001')
{}

# Rename SDC
client.sdc.rename('a7e798d100000000', 'SDC_2')
client.sdc.get(filter_fields={'id': 'a7e798d100000000'},
               fields=['name', 'id'])
[{'name': 'SDC_2', 'id': 'a7e798d100000000'}]

# Set performance profile for SDC
client.sdc.set_performance_profile('a7e798d100000000', 'HighPerformance')

# Add a fault set to a protection domain
client.fault_set.create(protection_domain_id='dc65bd9900000000',
                        name='sio-fs1')
client.fault_set.get(filter_fields={'id': 'fba27fae00000001'},
                     fields=['name', 'id'])
[{'name': 'sio-fs1', 'id': 'fba27fae00000001'}]

# Clear fault set
client.fault_set.clear('fba27fae00000001')
{}

# Create volume
from PyPowerFlex.objects.volume import VolumeType
from PyPowerFlex.objects.volume import CompressionMethod
from PyPowerFlex.objects.volume import VolumeClass
client.volume.create(storage_pool_id='76f2b2fd00000000',
                     size_in_gb=40,
                     name='new_thin_vol',
                     volume_type=VolumeType.thin,
                     use_rmcache=True,
                     compression_method=CompressionMethod.normal)

# Volume can be created with custom volume class
client.volume.create(storage_pool_id='76f2b2fd00000001',
                     size_in_gb=40,
                     name='new_custom_class_volume',
                     volume_type=VolumeType.thin,
                     use_rmcache=True,
                     compression_method=CompressionMethod.normal,
                     volume_class=VolumeClass.datastore)

# Extend volume size
client.volume.extend(volume_id='4a3a153e00000000',
                     size_in_gb=48)
client.volume.get(filter_fields={'id': '4a3a153e00000000'},
                  fields=['name', 'id'])
[{'name': 'sio-new_thin_vol', 'id': '4a3a153e00000000'}]
```
