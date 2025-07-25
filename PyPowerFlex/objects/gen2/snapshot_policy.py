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

"""Module for interacting with snapshot policy APIs."""

# pylint: disable=too-few-public-methods,no-member,too-many-arguments,too-many-positional-arguments,duplicate-code

import logging

import requests

from PyPowerFlex import base_client
from PyPowerFlex import exceptions


LOG = logging.getLogger(__name__)


class AutoSnapshotRemovalAction:
    """Auto snapshot deletion strategy."""

    detach = 'Detach'
    remove = 'Remove'


class SnapshotPolicy(base_client.EntityRequest):
    """
    A class representing Snapshot Policy client.
    """
    def add_source_volume(self, snapshot_policy_id, volume_id):
        """Add source volume to PowerFlex snapshot policy.

        :type snapshot_policy_id: str
        :type volume_id: str
        :rtype: dict
        """

        action = 'addSourceVolumeToSnapshotPolicy'

        params = {"sourceVolumeId": volume_id}

        r, response = self.send_post_request(self.base_action_url,
                                             action=action,
                                             entity=self.entity,
                                             entity_id=snapshot_policy_id,
                                             params=params)
        if r.status_code != requests.codes.ok:
            msg = (
                f"Failed to add source volume to PowerFlex {self.entity} "
                f"with id {snapshot_policy_id}. "
                f"Error: {response}"
            )
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

        return self.get(entity_id=snapshot_policy_id)

    def create(self,
               auto_snap_creation_cadence_in_min,
               retained_snaps_per_level,
               name=None,
               paused=None,
               snapshot_access_mode=None,
               secure_snapshots=None):
        """Create PowerFlex snapshot policy.

        :type auto_snap_creation_cadence_in_min: int
        :type retained_snaps_per_level: list[int]
        :type name: str
        :type paused: bool
        :rtype: dict
        """

        params = {
            "autoSnapshotCreationCadenceInMin": auto_snap_creation_cadence_in_min,
            "numOfRetainedSnapshotsPerLevel": retained_snaps_per_level,
            "name": name,
            "paused": paused,
            "snapshotAccessMode": snapshot_access_mode,
            "secureSnapshots": secure_snapshots
        }

        return self._create_entity(params)

    def delete(self, snapshot_policy_id):
        """Remove PowerFlex snapshot policy.

        :type snapshot_policy_id: str
        :rtype: None
        """

        return self._delete_entity(snapshot_policy_id)

    def modify(self,
               snapshot_policy_id,
               auto_snap_creation_cadence_in_min,
               retained_snaps_per_level):
        """Modify PowerFlex snapshot policy.

        :type snapshot_policy_id: str
        :type auto_snap_creation_cadence_in_min: int
        :type retained_snaps_per_level: list[int]
        :rtype: dict
        """

        action = 'modifySnapshotPolicy'

        params = {
            "autoSnapshotCreationCadenceInMin": auto_snap_creation_cadence_in_min,
            "numOfRetainedSnapshotsPerLevel": retained_snaps_per_level
        }

        r, response = self.send_post_request(self.base_action_url,
                                             action=action,
                                             entity=self.entity,
                                             entity_id=snapshot_policy_id,
                                             params=params)
        if r.status_code != requests.codes.ok:
            msg = (
                f"Failed to modify PowerFlex {self.entity} with id {snapshot_policy_id}. "
                f"Error: {response}"
            )
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

        return self.get(entity_id=snapshot_policy_id)

    def pause(self, snapshot_policy_id):
        """Pause PowerFlex snapshot policy.

        :type snapshot_policy_id: str
        :rtype: dict
        """

        action = 'pauseSnapshotPolicy'

        r, response = self.send_post_request(self.base_action_url,
                                             action=action,
                                             entity=self.entity,
                                             entity_id=snapshot_policy_id)
        if r.status_code != requests.codes.ok:
            msg = (
                f"Failed to pause PowerFlex {self.entity} with id {snapshot_policy_id}. "
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
        """Remove source volume from PowerFlex snapshot policy.

        :type snapshot_policy_id: str
        :type volume_id: str
        :param auto_snap_removal_action: one of predefined attributes of
                                         AutoSnapshotRemovalAction
        :type auto_snap_removal_action: str
        :type detach_locked_auto_snaps: bool
        :rtype: dict
        """

        action = 'removeSourceVolumeFromSnapshotPolicy'

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
                f"Failed to remove source volume from PowerFlex {self.entity} "
                f"with id {snapshot_policy_id}. "
                f"Error: {response}"
            )
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

        return self.get(entity_id=snapshot_policy_id)

    def rename(self, snapshot_policy_id, name):
        """Rename PowerFlex snapshot policy.

        :type snapshot_policy_id: str
        :type name: str
        :rtype: dict
        """

        action = 'renameSnapshotPolicy'

        params = {
            "newName": name
        }

        return self._rename_entity(action, snapshot_policy_id, params)

    def resume(self, snapshot_policy_id):
        """Resume PowerFlex snapshot policy.

        :type snapshot_policy_id: str
        :rtype: dict
        """

        action = 'resumeSnapshotPolicy'

        r, response = self.send_post_request(self.base_action_url,
                                             action=action,
                                             entity=self.entity,
                                             entity_id=snapshot_policy_id)
        if r.status_code != requests.codes.ok:
            msg = (
                f"Failed to resume PowerFlex {self.entity} with id {snapshot_policy_id}. "
                f"Error: {response}"
            )
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

        return self.get(entity_id=snapshot_policy_id)

    def get_statistics(self, snapshot_policy_id, fields=None):
        """Get related PowerFlex Statistics for snapshot policy.

        :type snapshot_policy_id: str
        :type fields: list|tuple
        :rtype: dict
        """

        return self.get_related(snapshot_policy_id,
                                'Statistics',
                                fields)

    def query_selected_statistics(self, properties, ids=None):
        """Query PowerFlex snapshot policy statistics.

        :type properties: list
        :type ids: list of snapshot policy IDs or None for all snapshot
                   policies
        :rtype: dict
        """

        action = "querySelectedStatistics"

        params = {'properties': properties}

        if ids:
            params["ids"] = ids
        else:
            params["allIds"] = ""

        return self._query_selected_statistics(action, params)
