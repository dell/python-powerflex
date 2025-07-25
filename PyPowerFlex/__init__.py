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
from PyPowerFlex import token
from PyPowerFlex import utils
import PyPowerFlex.objects.common as common
import PyPowerFlex.objects.gen1 as gen1
import PyPowerFlex.objects.gen2 as gen2

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
        self.token = token.Token()
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
        # to get system api version
        self.add_objects_by_version(gen1)
        self.configuration.validate()

        utils.init_logger(self.configuration.log_level)
        if version.parse(self.system.api_version()) < version.Version('3.0'):
            raise exceptions.PowerFlexClientException(
                'PowerFlex (VxFlex OS) versions lower than '
                '3.0 are not supported.'
            )

        api_ver = version.parse(self.system.api_version())

        if api_ver < version.Version('3.0'):
            raise exceptions.PowerFlexClientException(
                'PowerFlex (VxFlex OS) versions lower than 3.0 are not supported.'
            )
        if version.Version("3.0") < api_ver < version.Version("5.0"):
            self.add_objects_by_version(gen1)
        elif api_ver >= version.Version("5.0"):
            self.add_objects_by_version(gen2)
        self.__is_initialized = True

    def add_objects_by_version(self, module):
        """
        Dynamically registers storage entities based on module version.
        :param module: Either gen1 or gen2 module
        """
        entity_map = [
            ('device', 'Device'),
            ('fault_set', 'FaultSet'),
            ('protection_domain', 'ProtectionDomain'),
            ('sds', 'Sds'),
            ('snapshot_policy', 'SnapshotPolicy'),
            ('storage_pool', 'StoragePool'),
            ('acceleration_pool', 'AccelerationPool'),
            ('volume', 'Volume'),
            ('utility', 'PowerFlexUtility'),
            ('replication_consistency_group', 'ReplicationConsistencyGroup'),
            ('replication_pair', 'ReplicationPair'),
            ('service_template', 'ServiceTemplate'),
            ('managed_device', 'ManagedDevice'),
            ('deployment', 'Deployment'),
            ('firmware_repository', 'FirmwareRepository'),
            ('storage_node', 'StorageNode'),  # Only available in gen2
        ]

        for attr_name, class_name in entity_map:
            entity_class = getattr(module, class_name, None)
            if entity_class:
                self.__add_storage_entity(attr_name, entity_class)
