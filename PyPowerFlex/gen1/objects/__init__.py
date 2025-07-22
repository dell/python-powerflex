# Copyright (c) 2024 Dell Inc. or its subsidiaries.
# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""This module contains the objects for interacting with the PowerFlex APIs."""

from PyPowerFlex.gen1.objects.device import Device
from PyPowerFlex.gen1.objects.fault_set import FaultSet
from PyPowerFlex.gen1.objects.protection_domain import ProtectionDomain
from PyPowerFlex.gen1.objects.sdc import Sdc
from PyPowerFlex.gen1.objects.sds import Sds
from PyPowerFlex.gen1.objects.sdt import Sdt
from PyPowerFlex.gen1.objects.snapshot_policy import SnapshotPolicy
from PyPowerFlex.gen1.objects.storage_pool import StoragePool
from PyPowerFlex.gen1.objects.acceleration_pool import AccelerationPool
from PyPowerFlex.gen1.objects.system import System
from PyPowerFlex.gen1.objects.volume import Volume
from PyPowerFlex.gen1.objects.utility import PowerFlexUtility
from PyPowerFlex.gen1.objects.replication_consistency_group import ReplicationConsistencyGroup
from PyPowerFlex.gen1.objects.replication_pair import ReplicationPair
from PyPowerFlex.gen1.objects.service_template import ServiceTemplate
from PyPowerFlex.gen1.objects.managed_device import ManagedDevice
from PyPowerFlex.gen1.objects.deployment import Deployment
from PyPowerFlex.gen1.objects.firmware_repository import FirmwareRepository
from PyPowerFlex.gen1.objects.host import Host


__all__ = [
    'Device',
    'FaultSet',
    'ProtectionDomain',
    'Sdc',
    'Sds',
    'Sdt',
    'SnapshotPolicy',
    'StoragePool',
    'AccelerationPool',
    'System',
    'Volume',
    'PowerFlexUtility',
    'ReplicationConsistencyGroup',
    'ReplicationPair',
    'ServiceTemplate',
    'ManagedDevice',
    'Deployment',
    'FirmwareRepository',
    'Host',
]
