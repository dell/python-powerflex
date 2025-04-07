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

from PyPowerFlex.objects.device import Device
from PyPowerFlex.objects.fault_set import FaultSet
from PyPowerFlex.objects.protection_domain import ProtectionDomain
from PyPowerFlex.objects.sdc import Sdc
from PyPowerFlex.objects.sds import Sds
from PyPowerFlex.objects.sdt import Sdt
from PyPowerFlex.objects.snapshot_policy import SnapshotPolicy
from PyPowerFlex.objects.storage_pool import StoragePool
from PyPowerFlex.objects.acceleration_pool import AccelerationPool
from PyPowerFlex.objects.system import System
from PyPowerFlex.objects.volume import Volume
from PyPowerFlex.objects.utility import PowerFlexUtility
from PyPowerFlex.objects.replication_consistency_group import ReplicationConsistencyGroup
from PyPowerFlex.objects.replication_pair import ReplicationPair
from PyPowerFlex.objects.service_template import ServiceTemplate
from PyPowerFlex.objects.managed_device import ManagedDevice
from PyPowerFlex.objects.deployment import Deployment
from PyPowerFlex.objects.firmware_repository import FirmwareRepository
from PyPowerFlex.objects.host import Host
from PyPowerFlex.objects.credential import Credential


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
    'Credential',
]
