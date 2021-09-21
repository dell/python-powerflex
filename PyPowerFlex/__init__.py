# Copyright (c) 2020 Dell Inc. or its subsidiaries.
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

from packaging import version

from PyPowerFlex import configuration
from PyPowerFlex import exceptions
from PyPowerFlex import objects
from PyPowerFlex import token
from PyPowerFlex import utils


__all__ = [
    'PowerFlexClient'
]


class PowerFlexClient:
    __slots__ = (
        '__is_initialized',
        'configuration',
        'token',
        'device',
        'fault_set',
        'protection_domain',
        'sdc',
        'sds',
        'snapshot_policy',
        'storage_pool',
        'acceleration_pool',
        'system',
        'volume'
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
        return super(PowerFlexClient, self).__getattribute__(item)

    def __add_storage_entity(self, attr_name, entity_class):
        setattr(self, attr_name, entity_class(self.token, self.configuration))

    def initialize(self):
        self.configuration.validate()
        self.__add_storage_entity('device', objects.Device)
        self.__add_storage_entity('fault_set', objects.FaultSet)
        self.__add_storage_entity('protection_domain',
                                  objects.ProtectionDomain)
        self.__add_storage_entity('sdc', objects.Sdc)
        self.__add_storage_entity('sds', objects.Sds)
        self.__add_storage_entity('snapshot_policy', objects.SnapshotPolicy)
        self.__add_storage_entity('storage_pool', objects.StoragePool)
        self.__add_storage_entity('acceleration_pool',
                                  objects.AccelerationPool)
        self.__add_storage_entity('system', objects.System)
        self.__add_storage_entity('volume', objects.Volume)
        utils.init_logger(self.configuration.log_level)
        if version.parse(self.system.api_version()) < version.Version('3.0'):
            raise exceptions.PowerFlexClientException(
                'PowerFlex (VxFlex OS) versions lower than '
                '3.0 are not supported.'
            )
        self.__is_initialized = True
