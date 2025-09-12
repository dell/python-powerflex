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

"""This module is used for the initialization of PowerFlex Client."""

# pylint: disable=invalid-name,too-many-arguments,too-many-positional-arguments

from packaging import version

from PyPowerFlex import configuration
from PyPowerFlex import exceptions
from PyPowerFlex import powerflex_token
from PyPowerFlex import utils
from PyPowerFlex.objects import common
from PyPowerFlex.objects import gen1
from PyPowerFlex.objects import gen2

__all__ = [
    'PowerFlexClient'
]


class PowerFlexClient:
    """
    Client class for interacting with PowerFlex API.

    This class initializes the client with the provided configuration and provides
    access to the various storage entities available in the PowerFlex system.
    """
    __slots__ = (
        # gen1
        '__is_initialized',
        'configuration',
        'token',
        'device',
        'fault_set',
        'protection_domain',
        'sdc',
        'sds',
        'sdt',
        'snapshot_policy',
        'storage_pool',
        'acceleration_pool',
        'system',
        'volume',
        'utility',
        'replication_consistency_group',
        'replication_pair',
        'service_template',
        'managed_device',
        'deployment',
        'firmware_repository',
        'host',
        # gen2
        'storage_node',
        'device_group',
    )

    def __init__(self,
                 gateway_address=None,
                 gateway_port=443,
                 username=None,
                 password=None,
                 verify_certificate=False,
                 certificate_path=None,
                 timeout=120,
                 log_level=None):
        self.configuration = configuration.Configuration(gateway_address,
                                                         gateway_port,
                                                         username,
                                                         password,
                                                         verify_certificate,
                                                         certificate_path,
                                                         timeout,
                                                         log_level)
        self.token = powerflex_token.PowerFlexToken()
        self.__is_initialized = False

    def __getattr__(self, item):
        if not self.__is_initialized and item in self.__slots__:
            raise exceptions.ClientNotInitialized
        return super().__getattribute__(item)

    def __add_storage_entity(self, attr_name, entity_class):
        setattr(self, attr_name, entity_class(self.token, self.configuration))

    def initialize(self):
        """
        Initializes the client.

        Raises:
            PowerFlexClientException: If the PowerFlex API version is lower than 3.0.
        """
        # common objects here
        self.add_objects_common()
        self.configuration.validate()

        utils.init_logger(self.configuration.log_level)
        if version.parse(self.system.api_version()) < version.Version('3.0'):
            raise exceptions.PowerFlexClientException(
                'PowerFlex (VxFlex OS) versions lower than '
                '3.0 are not supported.'
            )

        if version.parse(self.system.api_version()) > version.Version('3.0') and \
           version.parse(self.system.api_version()) < version.Version('5.0'):
            self.add_objects_gen1()
        elif version.parse(self.system.api_version()) >= version.Version('5.0'):
            self.add_objects_gen2()
        self.__is_initialized = True

    def add_objects_common(self):
        """Add common objects here."""
        self.__add_storage_entity('system', common.System)
        self.__add_storage_entity('sdc', common.Sdc)
        self.__add_storage_entity('sdt', common.Sdt)
        self.__add_storage_entity('host', common.Host)
        self.__add_storage_entity('utility', common.PowerFlexUtility)
        self.__add_storage_entity('service_template', common.ServiceTemplate)
        self.__add_storage_entity('managed_device', common.ManagedDevice)
        self.__add_storage_entity('deployment', common.Deployment)
        self.__add_storage_entity('firmware_repository', common.FirmwareRepository)

    def add_objects_gen1(self):
        """Add gen1 objects here."""
        self.__add_storage_entity('system', gen1.System)
        self.__add_storage_entity('device', gen1.Device)
        self.__add_storage_entity(
            'fault_set', gen1.FaultSet)
        self.__add_storage_entity('protection_domain',
                                  gen1.ProtectionDomain)
        self.__add_storage_entity('sds', gen1.Sds)
        self.__add_storage_entity(
            'snapshot_policy', gen1.SnapshotPolicy)
        self.__add_storage_entity('storage_pool', gen1.StoragePool)
        self.__add_storage_entity('acceleration_pool',
                                  gen1.AccelerationPool)
        self.__add_storage_entity('volume', gen1.Volume)
        self.__add_storage_entity(
            'replication_consistency_group',
            gen1.ReplicationConsistencyGroup)
        self.__add_storage_entity('replication_pair', gen1.ReplicationPair)

    def add_objects_gen2(self):
        """Add gen2 objects here."""
        self.__add_storage_entity('system', gen2.System)
        self.__add_storage_entity('storage_node', gen2.StorageNode)
        self.__add_storage_entity('protection_domain', gen2.ProtectionDomain)
        self.__add_storage_entity('storage_pool', gen2.StoragePool)
        self.__add_storage_entity('snapshot_policy', gen2.SnapshotPolicy)
        self.__add_storage_entity('device', gen2.Device)
        self.__add_storage_entity('device_group', gen2.DeviceGroup)
        self.__add_storage_entity('volume', gen2.Volume)
