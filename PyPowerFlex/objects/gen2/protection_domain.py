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

from marshmallow import fields, validate
from PyPowerFlex import base_client, exceptions


LOG = logging.getLogger(__name__)


# class LinkSchema(Schema):
#     rel = fields.Str(
#         metadata={
#             "description": "Rel",
#         }
#     )
#     href = fields.Str(
#         metadata={
#             "description": "Href",
#         }
#     )
#     def on_bind_field(self, field_name, field_obj):
#         field_obj.data_key = camelcase(field_obj.data_key or field_name)
#     class Meta:
#         unknown = EXCLUDE


class ProtectionDomainSchema(base_client.BaseSchema):
    """Protection Domain schema."""
    id = fields.Str(
        metadata={
            "description": "Protection Domain Id",
        }
    )
    name = fields.Str(
        required=True,
        metadata={
            "description": "Protection Domain Name",
            "updatable": True,
        }
    )
    state = fields.Str(
        validate=validate.OneOf(["Active", "Inactive"]),
        data_key="protectionDomainState",
        metadata={
            "description": "Protection Domain State: Active/Inactive, default: Active",
            "updatable": True,
        }
    )
    rebuild_enabled = fields.Boolean(
        metadata={
            "description": "Enable rebuild, default: True",
            "updatable": True,
        }
    )
    rebalance_enabled = fields.Boolean(
        metadata={
            "description": "Enable rebalance, default: True",
            "updatable": True,
        }
    )
    rebuild_network_throttling_enabled = fields.Boolean(
        metadata={
            "description": "Rebuild network throttling enabled",
        }
    )
    rebalance_network_throttling_enabled = fields.Boolean(
        metadata={
            "description": "Rebalance network throttling enabled",
        }
    )
    gen_type = fields.Str(
        metadata={
            "description": "Gen Type: EC or Mirroring",
        }
    )
    overall_concurrent_io_limit = fields.Integer(
        metadata={
            "description": "Overall concurrent IO limit, default: 4",
            "updatable": True,
        }
    )
    bandwidth_limit_overall_ios = fields.Integer(
        metadata={
            "description": "Bandwidth limit overall IOs, default: 400",
            "updatable": True,
        }
    )
    bandwidth_limit_bg_dev_scanner = fields.Integer(
        metadata={
            "description": "Bandwidth limit background device scanner, default: 10",
            "updatable": True,
        }
    )
    bandwidth_limit_garbage_collector = fields.Integer(
        metadata={
            "description": "Bandwidth limit garbage collector, default: 65535",
            "updatable": True,
        }
    )
    bandwidth_limit_singly_impacted_rebuild = fields.Integer(
        metadata={
            "description": "Bandwidth limit singly impacted rebuild, default: 400",
            "updatable": True,
        }
    )
    bandwidth_limit_doubly_impacted_rebuild = fields.Integer(
        metadata={
            "description": "Bandwidth limit doubly impacted rebuild, default: 400",
            "updatable": True,
        }
    )
    bandwidth_limit_rebalance = fields.Integer(
        metadata={
            "description": "Bandwidth limit rebalance, default: 40",
            "updatable": True,
        }
    )
    bandwidth_limit_other = fields.Integer(
        metadata={
            "description": "Bandwidth limit rebalance, default: 10",
            "updatable": True,
        }
    )
    bandwidth_limit_node_network = fields.Integer(
        metadata={
            "description": "Bandwidth limit node network, default: 25",
            "updatable": True,
        }
    )
    # links = fields.List(fields.Nested(LinkSchema),
    #     metadata={
    #         "description": "Links",
    #     }
    # )


def load_protection_domain_schema(obj):
    """Load protection domain schema."""
    return ProtectionDomainSchema().load(obj)


class ProtectionDomain(base_client.EntityRequest):
    """
    A class representing Protection Domain client.
    """

    def list(self):
        """List PowerFlex protection domains.

        :rtype: list[dict]
        """
        return list(map(load_protection_domain_schema, self.get()))

    def get_by_id(self, protection_domain_id):
        """Get PowerFlex protection domain.

        :type protection_domain_id: str
        :rtype: dict
        """
        return load_protection_domain_schema(self.get(entity_id=protection_domain_id))

    def get_by_name(self, name):
        """Get PowerFlex protection domain.

        :type name: str
        :rtype: dict
        """
        result = self.get(filter_fields={'name': name})
        if len(result) >= 1:
            return load_protection_domain_schema(result[0])
        return None

    def delete(self, protection_domain_id):
        """Remove PowerFlex protection domain.

        :type protection_domain_id: str
        :rtype: None
        """
        return self._delete_entity(protection_domain_id)

    def create(self, pd):
        """Create PowerFlex protection domain.

        :type pd: dict
        :rtype: dict
        """
        pd = load_protection_domain_schema(pd)
        params = {"name": pd['name']}

        new_pd = load_protection_domain_schema(self._create_entity(params))
        pd['id'] = new_pd['id']
        _, pd = self.update(ProtectionDomainSchema().dump(pd), new_pd)
        return pd

    def update(self, pd, current_pd=None):
        """Update PowerFlex protection domain.

        :type pd: dict
        :rtype: dict
        """
        current_pd = current_pd if current_pd is not None else self.get_by_id(
            pd['id'])
        pd = load_protection_domain_schema(
            {**ProtectionDomainSchema().dump(current_pd), **pd})

        has_update = False

        if pd['name'] != current_pd['name']:
            has_update = True
            self.rename(pd['id'], pd['name'])

        if pd['state'] != current_pd['state']:
            has_update = True
            if pd['state'] == "Inactive":
                self.inactivate(pd['id'], force=True)
            else:
                self.activate(pd['id'], force=True)

        if pd['rebuild_enabled'] != current_pd['rebuild_enabled']:
            has_update = True
            self.set_rebuild_enabled(pd['id'], pd['rebuild_enabled'])
        if pd['rebalance_enabled'] != current_pd['rebalance_enabled']:
            has_update = True
            self.set_rebalance_enabled(pd['id'], pd['rebalance_enabled'])
        # self.disable_inflight_bandwidth_flow_control(pd['id'])
        # self.enable_inflight_bandwidth_flow_control(pd['id'])

        policy = {
            # TODO: unlimited, favorApplication
            "policy": "favorApplication",
        }

        field_map = {
            'overall_concurrent_io_limit': 'overallConcurrentIoLimit',
            'bandwidth_limit_overall_ios': 'bandwidthLimitOverallIos',
            'bandwidth_limit_bg_dev_scanner': 'bandwidthLimitBgDevScanner',
            'bandwidth_limit_garbage_collector': 'bandwidthLimitGarbageCollector',
            'bandwidth_limit_singly_impacted_rebuild': 'bandwidthLimitSinglyImpactedRebuild',
            'bandwidth_limit_doubly_impacted_rebuild': 'bandwidthLimitDoublyImpactedRebuild',
            'bandwidth_limit_rebalance': 'bandwidthLimitRebalance',
            'bandwidth_limit_other': 'bandwidthLimitOther',
            'bandwidth_limit_node_network': 'bandwidthLimitNodeNetwork',
        }

        for py_key, api_key in field_map.items():
            if pd[py_key] != current_pd[py_key]:
                policy[api_key] = pd[py_key]

        if len(policy) > 1:
            has_update = True
            self.set_secondary_io_policy(pd['id'], policy)

        return has_update, self.get_by_id(pd['id'])

    def activate(self, protection_domain_id, force=False):
        """Activate PowerFlex protection domain.

        :type protection_domain_id: str
        :type force: bool
        :rtype: None
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

    def inactivate(self, protection_domain_id, force=False):
        """Inactivate PowerFlex protection domain.

        :type protection_domain_id: str
        :type force: bool
        :rtype: None
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

    def enable_inflight_bandwidth_flow_control(self, protection_domain_id):
        """Enable inflight bandwidth flow control.

        :type id: str
        :rtype: None
        """

        action = 'enableInflightBandwidthFlowControl'

        r, response = self.send_post_request(self.base_action_url,
                                             action=action,
                                             entity=self.entity,
                                             entity_id=protection_domain_id)
        if r.status_code != requests.codes.ok:
            msg = (
                f"Failed to enable inflight bandwidth flow control in PowerFlex {self.entity} "
                f"with id {protection_domain_id}. Error: {response}"
            )
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

    def disable_inflight_bandwidth_flow_control(self, protection_domain_id):
        """Disable inflight bandwidth flow control.

        :type protection_domain_id: str
        :rtype: None
        """

        action = 'disableInflightBandwidthFlowControl'

        r, response = self.send_post_request(self.base_action_url,
                                             action=action,
                                             entity=self.entity,
                                             entity_id=protection_domain_id)
        if r.status_code != requests.codes.ok:
            msg = (
                f"Failed to disable inflight bandwidth flow control in PowerFlex {self.entity} "
                f"with id {protection_domain_id}. Error: {response}"
            )
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

    def set_rebuild_enabled(self, protection_domain_id, enabled):
        """Set rebuild state.

        :type protection_domain_id: str
        :type enabled: bool
        :rtype: None
        """

        action = 'setRebuildEnabled'
        params = {
            "rebuildEnabled": enabled,
        }

        r, response = self.send_post_request(self.base_action_url,
                                             action=action,
                                             entity=self.entity,
                                             entity_id=protection_domain_id,
                                             params=params)
        if r.status_code != requests.codes.ok:
            msg = (
                f"Failed to set rebuild state in PowerFlex {self.entity} "
                f"with id {protection_domain_id}. Error: {response}"
            )
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

    def set_rebalance_enabled(self, protection_domain_id, enabled):
        """Set rebalance state.

        :type protection_domain_id: str
        :type enabled: bool
        :rtype: None
        """

        action = 'setRebalanceEnabled'
        params = {
            "rebalanceEnabled": enabled,
        }

        r, response = self.send_post_request(self.base_action_url,
                                             action=action,
                                             entity=self.entity,
                                             entity_id=protection_domain_id,
                                             params=params)
        if r.status_code != requests.codes.ok:
            msg = (
                f"Failed to set rebalance state in PowerFlex {self.entity} "
                f"with id {protection_domain_id}. Error: {response}"
            )
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

    def set_secondary_io_policy(self, protection_domain_id, policy):
        """Set secondary I/O policy.

        :type protection_domain_id: str
        :type policy: Dict
        :rtype: None
        """

        action = 'setSecondaryIoPolicy'
        params = {
            "policy": policy["policy"],
        }
        field_map = {
            'overall_concurrent_io_limit': 'overallConcurrentIoLimit',
            'bandwidth_limit_overall_ios': 'bandwidthLimitOverallIos',
            'bandwidth_limit_bg_dev_scanner': 'bandwidthLimitBgDevScanner',
            'bandwidth_limit_garbage_collector': 'bandwidthLimitGarbageCollector',
            'bandwidth_limit_singly_impacted_rebuild': 'bandwidthLimitSinglyImpactedRebuild',
            'bandwidth_limit_doubly_impacted_rebuild': 'bandwidthLimitDoublyImpactedRebuild',
            'bandwidth_limit_rebalance': 'bandwidthLimitRebalance',
            'bandwidth_limit_other': 'bandwidthLimitOther',
            'bandwidth_limit_node_network': 'bandwidthLimitNodeNetwork',
        }

        for py_key, api_key in field_map.items():
            if py_key in policy:
                params[api_key] = policy[py_key]

        r, response = self.send_post_request(self.base_action_url,
                                             action=action,
                                             entity=self.entity,
                                             entity_id=protection_domain_id,
                                             params=params)
        if r.status_code != requests.codes.ok:
            msg = (
                f"Failed to set secondary I/O policy in PowerFlex {self.entity} "
                f"with id {protection_domain_id}. Error: {response}"
            )
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

    # def get_storage_nodes(self, protection_domain_id, filter_fields=None, fields=None):
    #     """Get related PowerFlex Storage Nodes for protection domain.

    #     :type protection_domain_id: str
    #     :type filter_fields: dict
    #     :type fields: list|tuple
    #     :rtype: list[dict]
    #     """

    #     return self.get_related(protection_domain_id,
    #                             'StorageNode',
    #                             filter_fields,
    #                             fields)

    def get_storage_pools(self,
                          protection_domain_id,
                          filter_fields=None,
                          response_field=None):
        """Get related PowerFlex storage pools for protection domain.

        :type protection_domain_id: str
        :type filter_fields: dict
        :type response_field: list|tuple
        :rtype: list[dict]
        """

        return self.get_related(protection_domain_id,
                                'StoragePool',
                                filter_fields,
                                response_field)

    def rename(self, protection_domain_id, name):
        """Rename PowerFlex protection domain.

        :type protection_domain_id: str
        :type name: str
        :rtype: None
        """

        action = 'setProtectionDomainName'

        params = {"name": name}

        self._rename_entity(action, protection_domain_id, params)

    # def query_selected_statistics(self, properties, ids=None):
    #     """Query PowerFlex protection domain statistics.

    #     :type properties: list
    #     :type ids: list of protection domain IDs or None for all protection
    #                domains
    #     :rtype: dict
    #     """

    #     action = "querySelectedStatistics"

    #     params = {'properties': properties}

    #     if ids:
    #         params["ids"] = ids
    #     else:
    #         params["allIds"] = ""

    #     return self._query_selected_statistics(action, params)
