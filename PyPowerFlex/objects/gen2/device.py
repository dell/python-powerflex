# Copyright (c) 2025 Dell Inc. or its subsidiaries.
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
    ssd = 'SSD'
    pmem = 'PMEM'


class Device(base_client.EntityRequest):
    """
    A class representing Device client.
    """

    def create(self,
               current_pathname,
               media_type,
               device_group_id,
               node_id,
               force=None,
               name=None):
        """Create PowerFlex device.

        :type current_pathname: str
        :type device_group_id: str
        :type node_id: str
        :type force: bool
        :param media_type: one of predefined attributes of MediaType
        :type media_type: str
        :type name: str
        :rtype: dict
        """

        if not all([current_pathname, media_type, device_group_id, node_id]):
            msg = 'current_pathname, media_type, device_group_id and node_id must be set.'
            raise exceptions.InvalidInput(msg)

        params = {
            "deviceCurrentPathname": current_pathname,
            "deviceGroupId": device_group_id,
            "nodeId": node_id,
            "forceDeviceTakeover": force,
            "mediaType": media_type,
            "name": name
        }

        return self._create_entity(params)

    def delete(self, device_id):
        """Remove PowerFlex device.

        :type device_id: str
        :rtype: None
        """

        return self._delete_entity(device_id)

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

    def set_capacity_limit(self, device_id, capacity_limit_gb):
        """Update PowerFlex device capacity limit in GB.
        :type device_id: str
        :type capacity_limit_gb: int
        :rtype: dict
        """

        action = 'setDeviceCapacityLimit'
        params = {"capacityLimitInGB": capacity_limit_gb}
        r, response = self.send_post_request(self.base_action_url,
                                             action=action,
                                             entity=self.entity,
                                             entity_id=device_id,
                                             params=params)
        if r.status_code != requests.codes.ok:
            msg = (
                f"Failed to set capacity limit for PowerFlex {self.entity} "
                f"with id {device_id}. "
                f"Error: {response}"
            )
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

        return self.get(entity_id=device_id)

    def clear_errors(self, device_id, force=None):
        """Clear PowerFlex device errors.
        :type device_id: str
        :type force: bool
        :rtype: dict
        """

        action = 'clearDeviceError'

        params = {"forceClear": force}

        return self._perform_entity_operation_based_on_action(
            action=action,
            entity_id=device_id,
            params=params,
            add_entity=False)

    def activate(self, device_id, node_id):
        """Activate PowerFlex device.

        :type device_id: str
        :type node_id: str
        :rtype: dict
        """

        action = 'activateDevice'

        params = {"storageNodeId": node_id}

        return self._perform_entity_operation_based_on_action(
            action=action,
            entity_id=device_id,
            params=params,
            add_entity=False)

    def query_device_metrics(self, device_id, metrics=None):
        """Query PowerFlex Metrics for device.

        :type device_id: str
        :type metrics: list|tuple
        :rtype: dict
        """
        return self.query_metrics('device', [device_id], metrics)
