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

"""Module for interacting with device APIs."""

# pylint: disable=too-few-public-methods,too-many-arguments,too-many-positional-arguments,no-member,duplicate-code

import logging

import requests

from PyPowerFlex import base_client
from PyPowerFlex import exceptions


LOG = logging.getLogger(__name__)


class MediaType:
    """Device media types."""

    hdd = 'HDD'
    ssd = 'SSD'
    nvdimm = 'NVDIMM'


class ExternalAccelerationType:
    """Device external acceleration types."""

    invalid = 'Invalid'
    none = 'None'
    read = 'Read'
    write = 'Write'
    read_and_write = 'ReadAndWrite'


class Device(base_client.EntityRequest):
    """
    A class representing Device client.
    """
    def create(self,
               current_pathname,
               sds_id,
               acceleration_pool_id=None,
               external_acceleration_type=None,
               force=None,
               media_type=None,
               name=None,
               storage_pool_id=None):
        """Create PowerFlex device.

        :type current_pathname: str
        :type sds_id: str
        :type acceleration_pool_id: str
        :param external_acceleration_type: one of predefined attributes of
                                           ExternalAccelerationType
        :type external_acceleration_type: str
        :type force: bool
        :param media_type: one of predefined attributes of MediaType
        :type media_type: str
        :type name: str
        :type storage_pool_id: str
        :rtype: dict
        """

        if (
                all([storage_pool_id, acceleration_pool_id]) or
                not any([storage_pool_id, acceleration_pool_id])
        ):
            msg = 'Either storage_pool_id or acceleration_pool_id must be ' \
                  'set.'
            raise exceptions.InvalidInput(msg)

        params = {
            "deviceCurrentPathname": current_pathname,
            "sdsId": sds_id,
            "accelerationPoolId": acceleration_pool_id,
            "externalAccelerationType": external_acceleration_type,
            "forceDeviceTakeover": force,
            "mediaType": media_type,
            "name": name,
            "storagePoolId": storage_pool_id
        }

        return self._create_entity(params)

    def delete(self, device_id, force=None):
        """Remove PowerFlex device.

        :type device_id: str
        :type force: bool
        :rtype: None
        """

        params = {
            "forceRemove": force
        }

        return self._delete_entity(device_id, params)

    def rename(self, device_id, name):
        """Rename PowerFlex device.

        :type device_id: str
        :type name: str
        :rtype: dict
        """

        action = 'setDeviceName'

        params = {
            "newName": name
        }

        return self._rename_entity(action, device_id, params)

    def set_media_type(self,
                       device_id,
                       media_type):
        """Set PowerFlex device media type.

        :type device_id: str
        :param media_type: one of predefined attributes of MediaType
        :type media_type: str
        :rtype: dict
        """

        action = 'setMediaType'

        params = {"mediaType": media_type}

        r, response = self.send_post_request(self.base_action_url,
                                             action=action,
                                             entity=self.entity,
                                             entity_id=device_id,
                                             params=params)
        if r.status_code != requests.codes.ok:
            msg = (
                f"Failed to set media type for PowerFlex {self.entity} "
                f"with id {device_id}. Error: {response}"
            )
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

        return self.get(entity_id=device_id)

    def query_selected_statistics(self, properties, ids=None):
        """Query PowerFlex device statistics.

        :type properties: list
        :type ids: list of device IDs or None for all devices
        :rtype: dict
        """

        action = "querySelectedStatistics"

        params = {'properties': properties}

        if ids:
            params["ids"] = ids
        else:
            params["allIds"] = ""

        return self._query_selected_statistics(action, params)
