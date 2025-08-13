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

"""Module for interacting with snapshot policy APIs in PowerFlex 5.x."""

# pylint: disable=too-few-public-methods,no-member,too-many-arguments,too-many-positional-arguments,duplicate-code

import logging

import requests

from PyPowerFlex import exceptions
from PyPowerFlex.objects.gen1.snapshot_policy import SnapshotPolicy as SnapshotPolicyGen1


LOG = logging.getLogger(__name__)


class AutoSnapshotRemovalAction:
    """Auto snapshot deletion strategy."""

    detach = 'Detach'
    remove = 'Remove'


class SnapshotPolicy(SnapshotPolicyGen1):
    """
    A class representing Snapshot Policy client.
    """
    def add_source_volume(self, snapshot_policy_id, volume_id):
        """Assign source volume to PowerFlex snapshot policy.

        :type snapshot_policy_id: str
        :type volume_id: str
        :rtype: dict
        """

        action = 'assignSnapshotPolicy'

        params = {"sourceVolumeId": volume_id}

        r, response = self.send_post_request(self.base_action_url,
                                             action=action,
                                             entity=self.entity,
                                             entity_id=snapshot_policy_id,
                                             params=params)
        if r.status_code != requests.codes.ok:
            msg = (
                f"Failed to assign source volume {volume_id} to PowerFlex {self.entity} "
                f"with id {snapshot_policy_id}. "
                f"Error: {response}"
            )
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

        return self.get(entity_id=snapshot_policy_id)

    def remove_source_volume(self,
                             snapshot_policy_id,
                             volume_id,
                             auto_snap_removal_action,
                             detach_locked_auto_snaps=None):
        """Unassign source volume from PowerFlex snapshot policy.

        :type snapshot_policy_id: str
        :type volume_id: str
        :param auto_snap_removal_action: one of predefined attributes of
                                         AutoSnapshotRemovalAction
        :type auto_snap_removal_action: str
        :type detach_locked_auto_snaps: bool
        :rtype: dict
        """

        action = 'unassignSnapshotPolicy'

        params = {
            "sourceVolumeId": volume_id,
            "autoSnapshotRemovalAction": auto_snap_removal_action,
            "detachLockedAutoSnapshots": detach_locked_auto_snaps
        }

        r, response = self.send_post_request(self.base_action_url,
                                             action=action,
                                             entity=self.entity,
                                             entity_id=snapshot_policy_id,
                                             params=params)
        if r.status_code != requests.codes.ok:
            msg = (
                f"Failed to unassign source volume {volume_id} from PowerFlex {self.entity} "
                f"with id {snapshot_policy_id}. "
                f"Error: {response}"
            )
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

        return self.get(entity_id=snapshot_policy_id)

    def get_statistics(self, snapshot_policy_id, fields=None):
        """Get PowerFlex Snapshot Policy Statistics not supported in PowerFlex 5.x.

        :type snapshot_policy_id: str
        :type fields: list|tuple
        :rtype: dict
        """
        LOG.error("Get PowerFlex Snapshot Policy Statistics not supported in PowerFlex 5.x.")

    def query_selected_statistics(self, properties, ids=None):
        """Query PowerFlex snapshot policy statistics not supported in PowerFlex 5.x.

        :type properties: list
        :type ids: list of snapshot policy IDs or None for all snapshot
                   policies
        :rtype: dict
        """
        LOG.error("Query PowerFlex snapshot policy statistics not supported in PowerFlex 5.x.")
