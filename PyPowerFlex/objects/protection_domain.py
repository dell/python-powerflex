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

"""Module for interacting with protection domain APIs."""

# pylint: disable=too-few-public-methods,no-member,too-many-arguments,too-many-positional-arguments,duplicate-code

import logging

import requests

from PyPowerFlex import base_client
from PyPowerFlex import exceptions


LOG = logging.getLogger(__name__)


class RFCacheOperationMode:
    """RFcache operation mode."""

    none = 'None'
    read = 'Read'
    write = 'Write'
    read_and_write = 'ReadAndWrite'
    write_miss = 'WriteMiss'


class ProtectionDomain(base_client.EntityRequest):
    """
    A class representing Protection Domain client.
    """
    def activate(self, protection_domain_id, force=False):
        """Activate PowerFlex protection domain.

        :type protection_domain_id: str
        :type force: bool
        :rtype: dict
        """

        action = 'activateProtectionDomain'

        params = {
            "forceActivate": force
        }

        r, response = self.send_post_request(self.base_action_url,
                                             action=action,
                                             entity=self.entity,
                                             entity_id=protection_domain_id,
                                             params=params)
        if r.status_code != requests.codes.ok:
            msg = (
                f"Failed to activate PowerFlex {self.entity} "
                f"with id {protection_domain_id}. Error: {response}"
            )
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

        return self.get(entity_id=protection_domain_id)

    def create(self, name):
        """Create PowerFlex protection domain.

        :type name: str
        :rtype: dict
        """

        params = {"name": name}

        return self._create_entity(params)

    def get_sdss(self, protection_domain_id, filter_fields=None, fields=None):
        """Get related PowerFlex SDSs for protection domain.

        :type protection_domain_id: str
        :type filter_fields: dict
        :type fields: list|tuple
        :rtype: list[dict]
        """

        return self.get_related(protection_domain_id,
                                'Sds',
                                filter_fields,
                                fields)

    def get_storage_pools(self,
                          protection_domain_id,
                          filter_fields=None,
                          fields=None):
        """Get related PowerFlex storage pools for protection domain.

        :type protection_domain_id: str
        :type filter_fields: dict
        :type fields: list|tuple
        :rtype: list[dict]
        """

        return self.get_related(protection_domain_id,
                                'StoragePool',
                                filter_fields,
                                fields)

    def delete(self, protection_domain_id):
        """Remove PowerFlex protection domain.

        :type protection_domain_id: str
        :rtype: None
        """

        return self._delete_entity(protection_domain_id)

    def inactivate(self, protection_domain_id, force=False):
        """Inactivate PowerFlex protection domain.

        :type protection_domain_id: str
        :type force: bool
        :rtype: dict
        """

        action = 'inactivateProtectionDomain'

        params = {
            "forceShutdown": force
        }

        r, response = self.send_post_request(self.base_action_url,
                                             action=action,
                                             entity=self.entity,
                                             entity_id=protection_domain_id,
                                             params=params)
        if r.status_code != requests.codes.ok:
            msg = (
                f"Failed to inactivate PowerFlex {self.entity} "
                f"with id {protection_domain_id}. Error: {response}"
            )
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

        return self.get(entity_id=protection_domain_id)

    def rename(self, protection_domain_id, name):
        """Rename PowerFlex protection domain.

        :type protection_domain_id: str
        :type name: str
        :rtype: dict
        """

        action = 'setProtectionDomainName'

        params = {"name": name}

        return self._rename_entity(action, protection_domain_id, params)

    def network_limits(self, protection_domain_id, rebuild_limit=None,
                       rebalance_limit=None, vtree_migration_limit=None,
                       overall_limit=None):
        """
        Setting the Network limits of the protection domain.

        :type protection_domain_id: str
        :type rebuild_limit: int
        :type rebalance_limit: int
        :type vtree_migration_limit: int
        :type overall_limit: int
        :rtype dict
        """

        action = "setSdsNetworkLimits"

        params = {
            "rebuildLimitInKbps": rebuild_limit,
            "rebalanceLimitInKbps": rebalance_limit,
            "vtreeMigrationLimitInKbps": vtree_migration_limit,
            "overallLimitInKbps": overall_limit
        }
        r, response = self.send_post_request(self.base_action_url,
                                             action=action,
                                             entity=self.entity,
                                             entity_id=protection_domain_id,
                                             params=params)

        if r.status_code != requests.codes.ok:
            msg = (
                f"Failed to update the network limits of PowerFlex {self.entity} "
                f"with id {protection_domain_id}. Error: {response}"
            )
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

        return self.get(entity_id=protection_domain_id)

    def set_rfcache_enabled(self, protection_domain_id, enable_rfcache=None):
        """
        Enable/Disable the RFcache in the Protection Domain.

        :type protection_domain_id: str
        :type enable_rfcache: bool
        :rtype dict
        """

        action = "disableSdsRfcache"
        if enable_rfcache:
            action = "enableSdsRfcache"

        r, response = self.send_post_request(self.base_action_url,
                                             action=action,
                                             entity=self.entity,
                                             entity_id=protection_domain_id)
        if r.status_code != requests.codes.ok:
            msg = (
                f"Failed to enable/disable RFcache in PowerFlex {self.entity} "
                f"with id {protection_domain_id}. Error: {response}"
            )
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

        return self.get(entity_id=protection_domain_id)

    def rfcache_parameters(self, protection_domain_id, page_size=None,
                           max_io_limit=None, pass_through_mode=None):
        """
        Set RF cache parameters of the protection domain.

        :type protection_domain_id: str
        :type page_size: int
        :type max_io_limit: int
        :type pass_through_mode: str
        :rtype dict
        """

        action = "setRfcacheParameters"

        params = {
            "pageSizeKb": page_size,
            "maxIOSizeKb": max_io_limit,
            "rfcacheOperationMode": pass_through_mode
        }

        r, response = self.send_post_request(self.base_action_url,
                                             action=action,
                                             entity=self.entity,
                                             entity_id=protection_domain_id,
                                             params=params)

        if r.status_code != requests.codes.ok:
            msg = (
                f"Failed to set RFcache parameters in PowerFlex {self.entity} "
                f"with id {protection_domain_id}. Error: {response}"
            )
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

        return self.get(entity_id=protection_domain_id)

    def query_selected_statistics(self, properties, ids=None):
        """Query PowerFlex protection domain statistics.

        :type properties: list
        :type ids: list of protection domain IDs or None for all protection
                   domains
        :rtype: dict
        """

        action = "querySelectedStatistics"

        params = {'properties': properties}

        if ids:
            params["ids"] = ids
        else:
            params["allIds"] = ""

        return self._query_selected_statistics(action, params)
