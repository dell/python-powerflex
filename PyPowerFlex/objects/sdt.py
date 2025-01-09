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

"""Module for interacting with SDT APIs."""

# pylint: disable=too-few-public-methods,no-member,too-many-arguments,too-many-positional-arguments

import logging
import requests
from PyPowerFlex import base_client
from PyPowerFlex import exceptions
from PyPowerFlex import utils

LOG = logging.getLogger(__name__)


class SdtIp(dict):
    """PowerFlex sdt ip object.

    JSON-serializable, should be used as `sdt_ips` list item
    in `Sdt.create` method or sdt_ip item in `Sdt.add_sdt_ip` method.
    """

    def __init__(self, ip, role):
        params = utils.prepare_params(
            {
                "ip": ip,
                "role": role,
            },
            dump=False,
        )
        super().__init__(**params)


class SdtIpRoles:
    """SDT ip roles."""

    storage_only = "StorageOnly"
    host_only = "HostOnly"
    storage_and_host = "StorageAndHost"


class Sdt(base_client.EntityRequest):
    """
    A class representing SDT client.
    """
    def create(
        self,
        sdt_ips,
        sdt_name,
        protection_domain_id,
        storage_port=None,
        nvme_port=None,
        discovery_port=None,
    ):
        """Create PowerFlex SDT.

        :type sdt_ips: list[dict]
        :type storage_port: int
        :type nvme_port: int
        :type discovery_port: int
        :type sdt_name: str
        :type protection_domain_id: str
        :rtype: dict
        """

        params = {
            "ips": sdt_ips,
            "storagePort": storage_port,
            "nvmePort": nvme_port,
            "discoveryPort": discovery_port,
            "name": sdt_name,
            "protectionDomainId": protection_domain_id,
        }

        return self._create_entity(params)

    def rename(self, sdt_id, name):
        """Rename PowerFlex SDT.

        :type sdt_id: str
        :type name: str
        :rtype: dict
        """

        action = "renameSdt"

        params = {'newName': name}

        return self._rename_entity(action, sdt_id, params)

    def add_ip(self, sdt_id, ip, role):
        """Add PowerFlex SDT target IP address.

        :type sdt_id: str
        :type ip: str
        :type role: str
        :rtype: dict
        """

        action = "addIp"

        params = {
            "ip": ip,
            "role": role,
        }

        r, response = self.send_post_request(
            self.base_action_url,
            action=action,
            entity=self.entity,
            entity_id=sdt_id,
            params=params,
        )
        if r.status_code != requests.codes.ok:
            msg = (
                f"Failed to add IP for PowerFlex {self.entity} "
                f"with id {sdt_id}. Error: {response}"
            )
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

        return self.get(entity_id=sdt_id)

    def remove_ip(self, sdt_id, ip):
        """Remove PowerFlex SDT target IP address.

        :type sdt_id: str
        :type ip: str
        :rtype: dict
        """

        action = "removeIp"

        params = {"ip": ip}

        r, response = self.send_post_request(
            self.base_action_url,
            action=action,
            entity=self.entity,
            entity_id=sdt_id,
            params=params,
        )
        if r.status_code != requests.codes.ok:
            msg = f"Failed to remove IP from PowerFlex {self.entity} " \
                  f"with id {sdt_id}. Error: {response}"
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

        return self.get(entity_id=sdt_id)

    def set_ip_role(self, sdt_id, ip, role):
        """Set PowerFlex SDT target IP address role.

        :type sdt_id: str
        :type ip: str
        :param role: one of predefined attributes of SdtIpRoles
        :type role: str
        :rtype: dict
        """

        action = "modifyIpRole"

        params = {
            "ip": ip,
            "newRole": role
        }

        r, response = self.send_post_request(
            self.base_action_url,
            action=action,
            entity=self.entity,
            entity_id=sdt_id,
            params=params,
        )
        if r.status_code != requests.codes.ok:
            msg = f"Failed to set ip role for PowerFlex {self.entity} " \
                  f"with id {sdt_id}. Error: {response}"
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

        return self.get(entity_id=sdt_id)

    def set_storage_port(self, sdt_id, storage_port):
        """Set PowerFlex SDT storage port.

        :type sdt_id: str
        :type storage_port: int
        :rtype: dict
        """

        action = "modifyStoragePort"

        params = {"newStoragePort": storage_port}

        r, response = self.send_post_request(
            self.base_action_url,
            action=action,
            entity=self.entity,
            entity_id=sdt_id,
            params=params,
        )
        if r.status_code != requests.codes.ok:
            msg = (
                f"Failed to set storage port for PowerFlex {self.entity} "
                f"with id {sdt_id}. Error: {response}"
            )
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

        return self.get(entity_id=sdt_id)

    def set_nvme_port(self, sdt_id, nvme_port):
        """Set PowerFlex SDT NVMe port.

        :type sdt_id: str
        :type nvme_port: int
        :rtype: dict
        """

        action = "modifyNvmePort"

        params = {"newNvmePort": nvme_port}

        r, response = self.send_post_request(
            self.base_action_url,
            action=action,
            entity=self.entity,
            entity_id=sdt_id,
            params=params,
        )
        if r.status_code != requests.codes.ok:
            msg = (
                f"Failed to set nvme port for PowerFlex {self.entity} "
                f"with id {sdt_id}. Error: {response}"
            )
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

        return self.get(entity_id=sdt_id)

    def set_discovery_port(self, sdt_id, discovery_port):
        """Set PowerFlex SDT discovery port.

        :type sdt_id: str
        :type discovery_port: int
        :rtype: dict
        """

        action = "modifyDiscoveryPort"

        params = {"newDiscoveryPort": discovery_port}

        r, response = self.send_post_request(
            self.base_action_url,
            action=action,
            entity=self.entity,
            entity_id=sdt_id,
            params=params,
        )
        if r.status_code != requests.codes.ok:
            msg = (
                f"Failed to set discovery port for PowerFlex {self.entity} "
                f"with id {sdt_id}. Error: {response}"
            )
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

        return self.get(entity_id=sdt_id)

    def enter_maintenance_mode(self, sdt_id):
        """Enter Maintenance Mode.

        :type sdt_id: str
        :rtype: dict
        """

        action = "enterMaintenanceMode"

        r, response = self.send_post_request(
            self.base_action_url,
            action=action,
            entity=self.entity,
            entity_id=sdt_id,
            params=None,
        )
        if r.status_code != requests.codes.ok:
            msg = (
                f"Failed to enter maintenance mode for PowerFlex {self.entity} "
                f"with id {sdt_id}. Error: {response}"
            )
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

        return self.get(entity_id=sdt_id)

    def exit_maintenance_mode(self, sdt_id):
        """Exit Maintenance Mode.

        :type sdt_id: str
        :rtype: dict
        """

        action = "exitMaintenanceMode"

        r, response = self.send_post_request(
            self.base_action_url,
            action=action,
            entity=self.entity,
            entity_id=sdt_id,
            params=None,
        )
        if r.status_code != requests.codes.ok:
            msg = (
                f"Failed to exit maintenance mode for PowerFlex {self.entity} "
                f"with id {sdt_id}. Error: {response}"
            )
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

        return self.get(entity_id=sdt_id)

    def delete(self, sdt_id, force=None):
        """Remove PowerFlex SDT.

        :type sdt_id: str
        :type force: bool
        :rtype: None
        """

        params = {"force": force}

        return self._delete_entity(sdt_id, params)
