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

"""Module for testing snapshot policy client."""

# pylint: disable=invalid-name

from PyPowerFlex import exceptions
from PyPowerFlex.objects import snapshot_policy as sp
import tests


class TestSnapshotPolicyClient(tests.PyPowerFlexTestCase):
    """
    Test class for snapshot policy client.
    """
    def setUp(self):
        """
        Set up the test case.
        """
        super().setUp()
        self.client.initialize()
        self.fake_policy_id = '1'
        self.fake_volume_id = '1'

        self.MOCK_RESPONSES = {
            self.RESPONSE_MODE.Valid: {
                '/types/SnapshotPolicy/instances':
                    {'id': self.fake_policy_id},
                f'/instances/SnapshotPolicy::{self.fake_policy_id}':
                    {'id': self.fake_policy_id},
                f'/instances/SnapshotPolicy::{self.fake_policy_id}/action/removeSnapshotPolicy':
                    {},
                f'/instances/SnapshotPolicy::{self.fake_policy_id}'
                '/action/addSourceVolumeToSnapshotPolicy':
                    {},
                f'/instances/SnapshotPolicy::{self.fake_policy_id}/action/modifySnapshotPolicy':
                    {},
                f'/instances/SnapshotPolicy::{self.fake_policy_id}/action/pauseSnapshotPolicy':
                    {},
                f'/instances/SnapshotPolicy::{self.fake_policy_id}'
                '/action/removeSourceVolumeFromSnapshotPolicy':
                    {},
                f'/instances/SnapshotPolicy::{self.fake_policy_id}/action/renameSnapshotPolicy':
                    {},
                f'/instances/SnapshotPolicy::{self.fake_policy_id}/action/resumeSnapshotPolicy':
                    {},
                '/types/SnapshotPolicy'
                '/instances/action/querySelectedStatistics': {
                    self.fake_policy_id: {'numOfSrcVols': 1}
                },
            },
            self.RESPONSE_MODE.Invalid: {
                '/types/SnapshotPolicy/instances':
                    {},
            }
        }

    def test_snapshot_policy_add_source_volume(self):
        """
        Test adding a source volume to a snapshot policy.
        """
        self.client.snapshot_policy.add_source_volume(self.fake_policy_id,
                                                      self.fake_volume_id)

    def test_snapshot_policy_add_source_volume_bad_status(self):
        """
        Test adding a source volume to a snapshot policy with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexClientException,
                              self.client.snapshot_policy.add_source_volume,
                              self.fake_policy_id,
                              self.fake_volume_id)

    def test_snapshot_policy_create(self):
        """
        Test creating a snapshot policy.
        """
        self.client.snapshot_policy.create(
            auto_snap_creation_cadence_in_min=15,
            retained_snaps_per_level=[1, 2, 3],
            name='policy_1',
            paused=False
        )

    def test_snapshot_policy_create_bad_status(self):
        """
        Test creating a snapshot policy with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexFailCreating,
                              self.client.snapshot_policy.create,
                              auto_snap_creation_cadence_in_min=15,
                              retained_snaps_per_level=[1, 2, 3],
                              name='policy_1',
                              paused=False)

    def test_snapshot_policy_create_no_id_in_response(self):
        """
        Test creating a snapshot policy with no id in the response.
        """
        with self.http_response_mode(self.RESPONSE_MODE.Invalid):
            self.assertRaises(KeyError,
                              self.client.snapshot_policy.create,
                              auto_snap_creation_cadence_in_min=15,
                              retained_snaps_per_level=[1, 2, 3],
                              name='policy_1',
                              paused=False)

    def test_snapshot_policy_delete(self):
        """
        Test deleting a snapshot policy.
        """
        self.client.snapshot_policy.delete(self.fake_policy_id)

    def test_snapshot_policy_delete_bad_status(self):
        """
        Test deleting a snapshot policy with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexFailDeleting,
                              self.client.snapshot_policy.delete,
                              self.fake_policy_id)

    def test_snapshot_policy_modify(self):
        """
        Test modifying a snapshot policy.
        """
        self.client.snapshot_policy.modify(
            self.fake_policy_id,
            auto_snap_creation_cadence_in_min=25,
            retained_snaps_per_level=[1, 2, 4]
        )

    def test_snapshot_policy_modify_bad_status(self):
        """
        Test modifying a snapshot policy with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexClientException,
                              self.client.snapshot_policy.modify,
                              self.fake_policy_id,
                              auto_snap_creation_cadence_in_min=25,
                              retained_snaps_per_level=[1, 2, 4])

    def test_snapshot_policy_pause(self):
        """
        Test pausing a snapshot policy.
        """
        self.client.snapshot_policy.pause(self.fake_policy_id)

    def test_snapshot_policy_pause_bad_status(self):
        """
        Test pausing a snapshot policy with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexClientException,
                              self.client.snapshot_policy.pause,
                              self.fake_policy_id)

    def test_snapshot_policy_remove_source_volume(self):
        """
        Test removing a source volume from a snapshot policy.
        """
        self.client.snapshot_policy.remove_source_volume(
            self.fake_policy_id,
            self.fake_volume_id,
            auto_snap_removal_action=sp.AutoSnapshotRemovalAction.detach,
            detach_locked_auto_snaps=True
        )

    def test_snapshot_policy_remove_source_volume_bad_status(self):
        """
        Test removing a source volume from a snapshot policy with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexClientException,
                              self.client.snapshot_policy.remove_source_volume,
                              self.fake_policy_id,
                              self.fake_volume_id,
                              sp.AutoSnapshotRemovalAction.remove,
                              False)

    def test_snapshot_policy_rename(self):
        """
        Test renaming a snapshot policy.
        """
        self.client.snapshot_policy.rename(self.fake_policy_id,
                                           name='new_name')

    def test_snapshot_policy_rename_bad_status(self):
        """
        Tests the behavior of the rename method when the HTTP response has a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexFailRenaming,
                              self.client.snapshot_policy.rename,
                              self.fake_policy_id,
                              name='new_name')

    def test_snapshot_policy_resume(self):
        """
        Tests the behavior of the resume method.
        """
        self.client.snapshot_policy.resume(self.fake_policy_id)

    def test_snapshot_policy_resume_bad_status(self):
        """
        Tests the behavior of the resume method when the HTTP response has a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexClientException,
                              self.client.snapshot_policy.resume,
                              self.fake_policy_id)

    def test_snapshot_policy_query_selected_statistics(self):
        """
        Tests the behavior of the query_selected_statistics method.
        """
        ret = self.client.snapshot_policy.query_selected_statistics(
            properties=["numOfSrcVols"]
        )
        assert ret.get(self.fake_policy_id).get("numOfSrcVols") == 1

    def test_snapshot_policy_query_selected_statistics_bad_status(self):
        """
        Tests the behavior of the query_selected_statistics method
        when the HTTP response has a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(
                exceptions.PowerFlexFailQuerying,
                self.client.snapshot_policy.query_selected_statistics,
                properties=["numOfSrcVols"],
            )
