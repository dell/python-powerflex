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

from PyPowerFlex.objects.gen1.device import Device
from PyPowerFlex.objects.gen1.fault_set import FaultSet
from PyPowerFlex.objects.gen1.protection_domain import ProtectionDomain
from PyPowerFlex.objects.gen1.sds import Sds
from PyPowerFlex.objects.gen1.snapshot_policy import SnapshotPolicy
from PyPowerFlex.objects.gen1.storage_pool import StoragePool
from PyPowerFlex.objects.gen1.acceleration_pool import AccelerationPool
from PyPowerFlex.objects.gen1.volume import Volume
from PyPowerFlex.objects.gen1.replication_consistency_group import ReplicationConsistencyGroup
from PyPowerFlex.objects.gen1.replication_pair import ReplicationPair
from PyPowerFlex.objects.gen1.service_template import ServiceTemplate
from PyPowerFlex.objects.gen1.managed_device import ManagedDevice
from PyPowerFlex.objects.gen1.deployment import Deployment
from PyPowerFlex.objects.gen1.firmware_repository import FirmwareRepository


__all__ = [
    'Device',
    'FaultSet',
    'ProtectionDomain',
    'Sds',
    'SnapshotPolicy',
    'StoragePool',
    'AccelerationPool',
    'Volume',
    'ReplicationConsistencyGroup',
    'ReplicationPair',
    'ServiceTemplate',
    'ManagedDevice',
    'Deployment',
    'FirmwareRepository',
]
