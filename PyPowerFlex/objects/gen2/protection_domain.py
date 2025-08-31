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

from PyPowerFlex import base_client, exceptions


LOG = logging.getLogger(__name__)


class ProtectionDomain(base_client.EntityRequest):
    """
    A class representing Protection Domain client.
    """

    def list(self):
        """List PowerFlex protection domains.

        :rtype: list[dict]
        """
        return list(self.get())

    def get_by_id(self, protection_domain_id):
        """Get PowerFlex protection domain.

        :type protection_domain_id: str
        :rtype: dict
        """
        return self.get(entity_id=protection_domain_id)

    def get_by_name(self, name):
        """Get PowerFlex protection domain.

        :type name: str
        :rtype: dict
        """
        result = self.get(filter_fields={'name': name})
        return result[0] if len(result) > 0 else None

    def delete(self, protection_domain_id):
        """Remove PowerFlex protection domain.

        :type protection_domain_id: str
        :rtype: None
        """
        return self._delete_entity(protection_domain_id)

    def check_create_params(self, pd):
        """Check create parameters."""
        required_fields = ["name"]
        missing_fields = [
            field for field in required_fields if field not in pd]

        if missing_fields:
            msg = "name is required for creating a storage pool."
            raise exceptions.InvalidInput(msg)

    def create(self, pd):
        """Create PowerFlex protection domain.

        :type pd: dict
        :rtype: dict
        """
        self.check_create_params(pd)
        params = {"name": pd['name']}
        new_pd = self._create_entity(params)
        _, pd = self.update(pd, new_pd)
        return pd

    def check_update_params(self, pd_params, current_pd):
        """Check update parameters."""
        protection_domain_id = pd_params.get("id")
        if protection_domain_id and protection_domain_id != current_pd["id"]:
            e = exceptions.nonupdatable_exception(
                "protection domain ID", self.entity, pd_params["id"]
            )
            LOG.error(e.message)
            raise e

    def _compare_update_params(self, pd_params, current_pd):
        """Compare parameters and determine if an update is needed.

        :type pd_params: dict
        :type current_pd: dict
        :rtype: tuple[bool, dict]
        """
        need_update = False
        changes = {}  # Store the changes to be applied

        new_name = pd_params.get('newName')
        if new_name and new_name != current_pd['name']:
            need_update = True
            changes['name'] = new_name

        state = pd_params.get('protectionDomainState')
        if state and state != current_pd['protectionDomainState']:
            need_update = True
            changes['protectionDomainState'] = state

        rebuild_enabled = pd_params.get('rebuildEnabled')
        if rebuild_enabled is not None and \
                rebuild_enabled != current_pd['rebuildEnabled']:
            need_update = True
            changes['rebuildEnabled'] = rebuild_enabled

        rebalance_enabled = pd_params.get('rebalanceEnabled')
        if rebalance_enabled is not None and \
                rebalance_enabled != current_pd['rebalanceEnabled']:
            need_update = True
            changes['rebalanceEnabled'] = rebalance_enabled

        field_map = {
            "policy": "policy",  # unlimited or favorApplication
            'overallConcurrentIoLimit': 'overallConcurrentIoLimit',
            'bandwidthLimitOverallIos': 'bandwidthLimitOverallIos',
            'bandwidthLimitBgDevScanner': 'bandwidthLimitBgDevScanner',
            'bandwidthLimitSinglyImpactedRebuild': 'bandwidthLimitSinglyImpactedRebuild',
            'bandwidthLimitDoublyImpactedRebuild': 'bandwidthLimitDoublyImpactedRebuild',
            'bandwidthLimitRebalance': 'bandwidthLimitRebalance',
            'bandwidthLimitOther': 'bandwidthLimitOther',
            'bandwidthLimitNodeNetwork': 'bandwidthLimitNodeNetwork',
        }

        for py_key, api_key in field_map.items():
            if (current_pd.get(py_key) is not None and
                pd_params.get(py_key) is not None and
                    current_pd[py_key] != pd_params[py_key]):
                changes[api_key] = pd_params[py_key]
                need_update = True

        return need_update, changes

    def need_update(self, pd_params, current_pd=None):
        """Check if PowerFlex protection domain needs to be updated.

        :type pd_params: dict
        :type current_pd: dict
        :rtype: bool, dict
        """
        current_pd = current_pd if current_pd is not None else self.get_by_id(
            pd_params["id"])
        need_update, changes = self._compare_update_params(
            pd_params, current_pd)
        return need_update, changes

    def update(self, pd_params, current_pd=None):
        """Update PowerFlex protection domain.

        :type pd: dict
        :rtype: dict
        """
        need_update, changes = self._compare_update_params(
            pd_params, current_pd)
        if not need_update:
            return False, current_pd

        has_update = True

        if 'name' in changes:
            self.rename(pd_params['id'], changes['name'])

        if 'protectionDomainState' in changes:
            if changes['protectionDomainState'] == "Inactive":
                self.inactivate(pd_params['id'], force=True)
            else:
                self.activate(pd_params['id'], force=True)

        if 'rebuildEnabled' in changes:
            self.set_rebuild_enabled(
                pd_params['id'], changes['rebuildEnabled'])

        if 'rebalanceEnabled' in changes:
            self.set_rebalance_enabled(
                pd_params['id'], changes['rebalanceEnabled'])

        policy = {}
        policy_param_list = ['policy',
                             'overallConcurrentIoLimit',
                             'bandwidthLimitOverallIos',
                             'bandwidthLimitBgDevScanner',
                             'bandwidthLimitSinglyImpactedRebuild',
                             'bandwidthLimitDoublyImpactedRebuild',
                             'bandwidthLimitRebalance',
                             'bandwidthLimitOther',
                             'bandwidthLimitNodeNetwork']
        policy = {
            k: v for k, v in changes.items() if k in policy_param_list
        }

        if policy:
            has_update = True
            self.set_secondary_io_policy(pd_params['id'], policy)

        return has_update, self.get_by_id(pd_params['id'])

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
        """
        Sets the secondary I/O policy for a protection domain.

        :param protection_domain_id: The ID of the protection domain.
        :type protection_domain_id: str
        :param policy: A dictionary containing the policy details.
                        policy contains a sub param 'policy' that 
                        accepts 'unlimited' or 'favorApplication'.
                        The sub param 'policy' is mandatory.
        :type policy: Dict
        :return: None
        :rtype: None

        Note: The overall and bandwidth parameters will only take effect 
        when the policy is set to 'favorApplication'.
        """

        action = 'setSecondaryIoPolicy'

        if 'policy' not in policy:
            msg = "policy is required for setting secondary I/O policy."
            raise exceptions.InvalidInput(msg)

        params = {
            "policy": policy["policy"],
        }
        field_map = {
            'overall_concurrent_io_limit': 'overallConcurrentIoLimit',
            'bandwidth_limit_overall_ios': 'bandwidthLimitOverallIos',
            'bandwidth_limit_bg_dev_scanner': 'bandwidthLimitBgDevScanner',
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
                                             params=policy)
        if r.status_code != requests.codes.ok:
            msg = (
                f"Failed to set secondary I/O policy in PowerFlex {self.entity} "
                f"with id {protection_domain_id}. Error: {response}"
            )
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

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
