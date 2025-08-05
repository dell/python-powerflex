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

"""This module contains the objects for interacting with the PowerFlex 5.0+ APIs."""

from PyPowerFlex.objects.gen2.storage_node import StorageNode
from PyPowerFlex.objects.gen2.protection_domain import ProtectionDomain
from PyPowerFlex.objects.gen2.storage_pool import StoragePool
from PyPowerFlex.objects.gen2.snapshot_policy import SnapshotPolicy
from PyPowerFlex.objects.gen2.device import Device
from PyPowerFlex.objects.gen2.device_group import DeviceGroup
from PyPowerFlex.objects.gen2.volume import Volume
from PyPowerFlex.objects.gen2.system import System

__all__ = [
    'StorageNode',
    'ProtectionDomain',
    'StoragePool',
    'SnapshotPolicy',
    'Device',
    'DeviceGroup',
    'Volume',
    'System'
]
