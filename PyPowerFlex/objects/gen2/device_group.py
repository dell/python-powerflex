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

"""Module for interacting with device group APIs."""

# pylint: disable=too-few-public-methods,too-many-arguments,too-many-positional-arguments,no-member,duplicate-code

import logging

import requests

from PyPowerFlex import base_client
from PyPowerFlex import exceptions


LOG = logging.getLogger(__name__)


class MediaType:
    """Device Group media types."""
    ssd = 'SSD'
    pmem = 'PMEM'


class DeviceGroup(base_client.EntityRequest):
    """
    A class representing Device Group client.
    """
    def create(self,
               name,
               protection_domain_id,
               media_type,
               spare_node_count=None,
               spare_device_count=None):
        """Create PowerFlex device group.

        :type protection_domain_id: str
        :param media_type: one of predefined attributes of MediaType
        :type media_type: str
        :type name: str
        :type spare_node_count: int
        :type spare_device_count: int
        :rtype: dict
        """

        if not all([name, protection_domain_id, media_type]):
            msg = 'name, protection_domain_id and media_type must be set.'
            raise exceptions.InvalidInput(msg)

        params = {
            "dgName": name,
            "mediaType": media_type,
            "protectionDomainId": protection_domain_id,
            "spareNodeCount": spare_node_count,
            "spareDeviceCount": spare_device_count
        }

        return self._create_entity(params)

    def delete(self, device_group_id):
        """Remove PowerFlex device group.
        :type device_group_id: str
        :rtype: None
        """
        return self._delete_entity(device_group_id)

    def modify(self,
               device_group_id,
               new_name=None,
               spare_node_count=None,
               spare_device_count=None):
        """Modify PowerFlex device group.

        :type new_name: str
        :type spare_node_count: int
        :type spare_device_count: int
        :rtype: None
        """

        action = 'modifyDeviceGroup'

        params = {
            "newName": new_name,
            "spareNodeCount": spare_node_count,
            "spareDeviceCount": spare_device_count
        }
        r, response = self.send_post_request(self.base_action_url,
                                             action=action,
                                             entity=self.entity,
                                             entity_id=device_group_id,
                                             params=params)
        if r.status_code != requests.codes.ok:
            msg = (
                f"Failed to modify PowerFlex {self.entity} with id {device_group_id}. "
                f"Error: {response}"
            )
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

        return self.get(entity_id=device_group_id)

    def query_usable_capacity(self, device_group_id):
        """Query PowerFlex device group usable capacity.

        :type device_group_id: str
        :rtype: dict
        """

        action = 'queryUsableCapacity'
        r, response = self.send_post_request(self.base_action_url,
                                             action=action,
                                             entity=self.entity,
                                             entity_id=device_group_id)
        if r.status_code != requests.codes.ok:
            msg = (
                f"Failed to query usable capacity for PowerFlex {self.entity} "
                f"with id {device_group_id}. "
                f"Error: {response}"
            )
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

        return response

    def query_device_group_metrics(self, device_group_id, metrics=None):
        """Query PowerFlex Metrics for device group.

        :type device_group_id: str
        :type metrics: list|tuple
        :rtype: dict
        """
        return self.query_metrics('device_group', [device_group_id], metrics)
