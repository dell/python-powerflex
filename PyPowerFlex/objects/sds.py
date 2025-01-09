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

"""Module for interacting with SDS APIs."""

# pylint: disable=too-few-public-methods,no-member,too-many-arguments,too-many-positional-arguments,too-many-locals,duplicate-code

import logging

import requests

from PyPowerFlex import base_client
from PyPowerFlex import exceptions
from PyPowerFlex import utils


LOG = logging.getLogger(__name__)


class DeviceTestMode:
    """SDS devices test modes."""

    test_only = 'testOnly'
    no_test = 'noTest'
    test_and_activate = 'testAndActivate'


class DrlMode:
    """SDS drl modes."""

    volatile = 'Volatile'
    nonvolatile = 'NonVolatile'


class SdsIpRoles:
    """SDS ip roles."""

    sds_only = 'sdsOnly'
    sdc_only = 'sdcOnly'
    all = 'all'


class PerformanceProfile:
    """SDS performance profiles."""

    highperformance = 'HighPerformance'
    compact = 'Compact'


class AccelerationDeviceInfo(dict):
    """PowerFlex acceleration device object.

    JSON-serializable, should be used as `acceleration_devices_info` list item
    in `Sds.create` method.
    """

    def __init__(self,
                 device_path,
                 accp_id,
                 device_name=None):
        params = utils.prepare_params(
            {
                'accelerationDevicePath': device_path,
                'accpId': accp_id,
                'accelerationDeviceName': device_name,
            },
            dump=False
        )
        super().__init__(**params)


class DeviceInfo:
    """PowerFlex device object.

    JSON-serializable, should be used as `devices_info` list item
    in `Sds.create` method.
    """

    def __init__(self,
                 device_path,
                 storage_pool_id,
                 device_name=None,
                 media_type=None):
        params = utils.prepare_params(
            {
                'devicePath': device_path,
                'storagePoolId': storage_pool_id,
                'deviceName': device_name,
                'mediaType': media_type,
            },
            dump=False
        )
        super().__init__(**params)


class RfcacheDevice(dict):
    """PowerFlex Rfcache device object.

    JSON-serializable, should be used as `rfcache_devices_info` list item
    in `Sds.create` method.
    """

    def __init__(self, path, name):
        params = utils.prepare_params(
            {
                'path': path,
                'name': name,
            },
            dump=False
        )
        super().__init__(**params)


class SdsIp(dict):
    """PowerFlex sds ip object.

    JSON-serializable, should be used as `sds_ips` list item
    in `Sds.create` method or sds_ip item in `Sds.add_sds_ip` method.
    """

    def __init__(self, ip, role):
        params = utils.prepare_params(
            {
                'ip': ip,
                'role': role,
            },
            dump=False
        )
        super().__init__(**params)


class Sds(base_client.EntityRequest):
    """
    A class representing SDS client.
    """
    def add_ip(self, sds_id, sds_ip):
        """Add PowerFlex SDS IP-address.

        :type sds_id: str
        :type sds_ip: dict
        :rtype: dict
        """

        action = 'addSdsIp'

        r, response = self.send_post_request(self.base_action_url,
                                             action=action,
                                             entity=self.entity,
                                             entity_id=sds_id,
                                             params=sds_ip)
        if r.status_code != requests.codes.ok:
            msg = (
                f"Failed to add IP for PowerFlex {self.entity} "
                f"with id {sds_id}. Error: {response}"
            )
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

        return self.get(entity_id=sds_id)

    def create(self,
               protection_domain_id,
               sds_ips,
               acceleration_devices_info=None,
               devices_info=None,
               device_test_mode=None,
               device_test_time_sec=None,
               drl_mode=None,
               fault_set_id=None,
               force_clean=None,
               force_device_takeover=None,
               name=None,
               num_of_io_buffers=None,
               rfcache_devices_info=None,
               rmcache_enabled=None,
               rmcache_size_in_kb=None,
               sds_port=None,
               ):
        """Create PowerFlex SDS.

        :type protection_domain_id: str
        :type sds_ips: list[dict]
        :type acceleration_devices_info: list[dict]
        :type devices_info: list[dict]
        :param device_test_mode: one of predefined attributes of DeviceTestMode
        :type device_test_mode: str
        :type device_test_time_sec: int
        :param drl_mode: one of predefined attributes of DrlMode
        :type drl_mode: str
        :type fault_set_id: str
        :type force_clean: bool
        :type force_device_takeover: bool
        :type name: str
        :type num_of_io_buffers: int
        :type rfcache_devices_info: list[dict]
        :type rmcache_enabled: bool
        :type rmcache_size_in_kb: int
        :type sds_port: int
        :rtype: dict
        """

        params = {
            "protectionDomainId": protection_domain_id,
            "sdsIpList": sds_ips,
            "accelerationDeviceInfoList": acceleration_devices_info,
            "deviceInfoList": devices_info,
            "deviceTestMode": device_test_mode,
            "deviceTestTimeSecs": device_test_time_sec,
            "drlMode": drl_mode,
            "faultSetId": fault_set_id,
            "forceClean": force_clean,
            "forceDeviceTakeover": force_device_takeover,
            "name": name,
            "numOfIoBuffers": num_of_io_buffers,
            "sdsRfcacheDeviceInfoList": rfcache_devices_info,
            "rmcacheEnabled": rmcache_enabled,
            "rmcacheSizeInKb": rmcache_size_in_kb,
            "sdsPort": sds_port
        }

        return self._create_entity(params)

    def delete(self, sds_id, force=None):
        """Remove PowerFlex SDS.

        :type sds_id: str
        :type force: bool
        :rtype: None
        """

        params = {"force": force}

        return self._delete_entity(sds_id, params)

    def get_devices(self, sds_id, filter_fields=None, fields=None):
        """Get related PowerFlex devices for SDS.

        :type sds_id: str
        :type filter_fields: dict
        :type fields: list|tuple
        :rtype: list[dict]
        """

        return self.get_related(sds_id, 'Device', filter_fields, fields)

    def rename(self, sds_id, name):
        """Rename PowerFlex SDS.

        :type sds_id: str
        :type name: str
        :rtype: dict
        """

        action = 'setSdsName'

        params = {"name": name}

        return self._rename_entity(action, sds_id, params)

    def remove_ip(self, sds_id, ip):
        """Remove PowerFlex SDS IP-address.

        :type sds_id: str
        :type ip: str
        :rtype: dict
        """

        action = 'removeSdsIp'

        params = {"ip": ip}

        r, response = self.send_post_request(self.base_action_url,
                                             action=action,
                                             entity=self.entity,
                                             entity_id=sds_id,
                                             params=params)
        if r.status_code != requests.codes.ok:
            msg = f"Failed to remove IP from PowerFlex {self.entity} " \
                  f"with id {sds_id}. Error: {response}"
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

        return self.get(entity_id=sds_id)

    def set_ip_role(self, sds_id, ip, role, force=None):
        """Set PowerFlex SDS IP-address role.

        :type sds_id: str
        :type ip: str
        :param role: one of predefined attributes of SdsIpRoles
        :type role: str
        :type force: bool
        :rtype: dict
        """

        action = 'setSdsIpRole'

        params = {
            'sdsIpToSet': ip,
            'newRole': role,
            'forceRoleModification': force
        }

        r, response = self.send_post_request(self.base_action_url,
                                             action=action,
                                             entity=self.entity,
                                             entity_id=sds_id,
                                             params=params)
        if r.status_code != requests.codes.ok:
            msg = (
                f"Failed to set ip role for PowerFlex {self.entity} "
                f"with id {sds_id}. Error: {response}"
            )
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

        return self.get(entity_id=sds_id)

    def set_port(self, sds_id, sds_port):
        """Set PowerFlex SDS port.

        :type sds_id: str
        :type sds_port: int
        :rtype: dict
        """

        action = 'setSdsPort'

        params = {
            'sdsPort': sds_port
        }

        r, response = self.send_post_request(self.base_action_url,
                                             action=action,
                                             entity=self.entity,
                                             entity_id=sds_id,
                                             params=params)
        if r.status_code != requests.codes.ok:
            msg = f"Failed to set port for PowerFlex {self.entity} " \
                  f"with id {sds_id}. Error: {response}"
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

        return self.get(entity_id=sds_id)

    def set_rfcache_enabled(self, sds_id, rfcache_enabled):
        """Enable/disable Rfcache for PowerFlex SDS.

        :type sds_id: str
        :type rfcache_enabled: bool
        :rtype: dict
        """

        action = 'disableRfcache'
        if rfcache_enabled:
            action = 'enableRfcache'

        r, response = self.send_post_request(self.base_action_url,
                                             action=action,
                                             entity=self.entity,
                                             entity_id=sds_id)
        if r.status_code != requests.codes.ok:
            msg = (
                f"Failed to enable/disable Rfcache for PowerFlex {self.entity} "
                f"with id {sds_id}. Error: {response}"
            )
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

        return self.get(entity_id=sds_id)

    def set_rmcache_enabled(self, sds_id, rmcache_enabled):
        """Enable/disable Rmcache for PowerFlex SDS.

        :type sds_id: str
        :type rmcache_enabled: bool
        :rtype: dict
        """

        action = 'setSdsRmcacheEnabled'

        params = {
            'rmcacheEnabled': rmcache_enabled
        }

        r, response = self.send_post_request(self.base_action_url,
                                             action=action,
                                             entity=self.entity,
                                             entity_id=sds_id,
                                             params=params)
        if r.status_code != requests.codes.ok:
            msg = (
                f"Failed to enable/disable Rmcache for PowerFlex {self.entity} "
                f"with id {sds_id}. Error: {response}"
            )
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

        return self.get(entity_id=sds_id)

    def set_rmcache_size(self, sds_id, rmcache_size):
        """Set Rmcache size for PowerFlex SDS.

        :type sds_id: str
        :type rmcache_size: int
        :rtype: dict
        """

        action = 'setSdsRmcacheSize'

        params = {"rmcacheSizeInMB": rmcache_size}

        r, response = self.send_post_request(self.base_action_url,
                                             action=action,
                                             entity=self.entity,
                                             entity_id=sds_id,
                                             params=params)
        if r.status_code != requests.codes.ok:
            msg = (
                f"Failed to set Rmcache size for PowerFlex {self.entity} "
                f"with id {sds_id}. Error: {response}"
            )
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

        return self.get(entity_id=sds_id)

    def set_performance_parameters(self, sds_id, performance_profile):
        """Set performance parameters for PowerFlex SDS.

        :type sds_id: str
        :type performance_profile: str
        :rtype: dict
        """

        action = 'setSdsPerformanceParameters'

        params = {"perfProfile": performance_profile}

        r, response = self.send_post_request(self.base_action_url,
                                             action=action,
                                             entity=self.entity,
                                             entity_id=sds_id,
                                             params=params)
        if r.status_code != requests.codes.ok:
            msg = (
                f"Failed to set performance parameters for PowerFlex "
                f"{self.entity} with id {sds_id}. Error: {response}"
            )
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

        return self.get(entity_id=sds_id)

    def query_selected_statistics(self, properties, ids=None):
        """Query PowerFlex SDS statistics.

        :type properties: list
        :type ids: list of SDS IDs or None for all SDS
        :rtype: dict
        """

        action = "querySelectedStatistics"

        params = {'properties': properties}

        if ids:
            params["ids"] = ids
        else:
            params["allIds"] = ""

        return self._query_selected_statistics(action, params)
