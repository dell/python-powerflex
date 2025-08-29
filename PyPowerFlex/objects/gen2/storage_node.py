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

"""Module for interacting with Storage Node APIs."""

# pylint: disable=too-few-public-methods,no-member,too-many-arguments,too-many-positional-arguments,too-many-locals,duplicate-code

import logging

import requests

from PyPowerFlex import base_client
from PyPowerFlex import exceptions
from PyPowerFlex import utils


LOG = logging.getLogger(__name__)


class StorageNodeIpRoles:
    """StorageNode ip roles."""

    storage = 'Storage'
    app = 'App'
    storage_and_app = 'StorageAndApp'


class StorageNodeIp(dict):
    """PowerFlex storage node ip object.

    JSON-serializable, should be used as `ipsList` list item
    in `Storage_node.create` method or ipsList item in `Storage_node.add_ip` method.
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


class StorageNode(base_client.EntityRequest):
    """PowerFlex Storage Node object."""
    @property
    def entity(self):
        """
        Returns the entity name.
        """
        return "Node"

    def add_ip(self, node_id, node_ip):
        """Add PowerFlex Storage Node IP-address.

        :type node_id: str
        :type node_ip: dict
        :rtype: dict
        """

        action = 'addIp'

        r, response = self.send_post_request(self.base_action_url,
                                             action=action,
                                             entity=self.entity,
                                             entity_id=node_id,
                                             params=node_ip)
        if r.status_code != requests.codes.ok:
            msg = (
                f"Failed to add IP for PowerFlex Storage Node "
                f"with id {node_id}. Error: {response}"
            )
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

        return self.get(entity_id=node_id)

    def create(self,
               name,
               node_ips,
               protection_domain_id,
               ):
        """Create PowerFlex Storage Node.
        :type name: str
        :type protection_domain_id: str
        :type node_ips: list[dict]
        :rtype: dict
        """

        params = {
            "protectionDomainId": protection_domain_id,
            "ips": node_ips,
            "name": name,
        }

        return self._create_entity(params)

    def delete(self, node_id):
        """Remove PowerFlex Storage Node.

        :type node_id: str
        :type force: bool
        :rtype: None
        """

        return self._delete_entity(node_id)

    def rename(self, node_id, name):
        """Rename PowerFlex Storage Node.

        :type node_id: str
        :type name: str
        :rtype: dict
        """

        action = 'renameStorageNode'

        params = {"name": name}

        return self._rename_entity(action, node_id, params)

    def remove_ip(self, node_id, ip):
        """Remove PowerFlex Storage Node IP-address.

        :type node_id: str
        :type ip: str
        :rtype: dict
        """

        action = 'removeIp'

        params = {"ip": ip}

        r, response = self.send_post_request(self.base_action_url,
                                             action=action,
                                             entity=self.entity,
                                             entity_id=node_id,
                                             params=params)
        if r.status_code != requests.codes.ok:
            msg = f"Failed to remove IP from PowerFlex Storage Node " \
                f"with id {node_id}. Error: {response}"
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

        return self.get(entity_id=node_id)

    def set_ip_role(self, node_id, ip, role):
        """Set PowerFlex Storage Node IP-address role.

        :type node_id: str
        :type ip: str
        :param role: one of predefined attributes of StorageNodeIpRoles
        :type role: str
        :type force: bool
        :rtype: dict
        """

        action = 'modifyIpRole'

        params = {
            'ip': ip,
            'newRole': role,
        }

        r, response = self.send_post_request(self.base_action_url,
                                             action=action,
                                             entity=self.entity,
                                             entity_id=node_id,
                                             params=params)
        if r.status_code != requests.codes.ok:
            msg = (
                f"Failed to set ip role for PowerFlex Storage Node "
                f"with id {node_id}. Error: {response}"
            )
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

        return self.get(entity_id=node_id)

    def update_original_pathnames(self, node_id, force=None):
        """Update original pathnames for PowerFlex Storage Node.

        :type node_id: str
        :type force: bool
        :rtype: dict
        """

        action = 'updateNodeOriginalPathnames'

        params = {"forceFailedDevices": force}

        r, response = self.send_post_request(self.base_action_url,
                                             action=action,
                                             entity=self.entity,
                                             entity_id=node_id,
                                             params=params)
        if r.status_code != requests.codes.ok:
            msg = (
                f"Failed to update original pathnames for PowerFlex {self.entity} "
                f"with id {node_id}. "
                f"Error: {response}"
            )
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

        return self.get(entity_id=node_id)
