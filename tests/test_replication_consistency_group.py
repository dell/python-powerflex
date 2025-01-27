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

"""Module for testing replication consistency group client."""

# pylint: disable=invalid-name,too-many-public-methods

from PyPowerFlex import exceptions
import tests


class TestReplicationConsistencyGroupClient(tests.PyPowerFlexTestCase):
    """
    Tests for the ReplicationConsistencyGroupClient.
    """
    def setUp(self):
        """
        Set up the test environment.
        """
        super().setUp()
        self.client.initialize()
        self.fake_rcg_id = '1'

        self.MOCK_RESPONSES = {
            self.RESPONSE_MODE.Valid: {
                '/types/ReplicationConsistencyGroup/instances':
                    {'id': self.fake_rcg_id},
                f'/instances/ReplicationConsistencyGroup::{self.fake_rcg_id}':
                    {'id': self.fake_rcg_id},
                f'/instances/ReplicationConsistencyGroup::{self.fake_rcg_id}'
                '/action/createReplicationConsistencyGroupSnapshots':
                    {},
                f'/instances/ReplicationConsistencyGroup::{self.fake_rcg_id}':
                    {'id': self.fake_rcg_id},
                f'/instances/ReplicationConsistencyGroup::{self.fake_rcg_id}'
                '/action/activateReplicationConsistencyGroup':
                    {'id': self.fake_rcg_id},
                f'/instances/ReplicationConsistencyGroup::{self.fake_rcg_id}'
                '/action/terminateReplicationConsistencyGroup':
                    {'id': self.fake_rcg_id},
                f'/instances/ReplicationConsistencyGroup::{self.fake_rcg_id}'
                '/action/terminateReplicationConsistencyGroup':
                    {'id': self.fake_rcg_id},
                f'/instances/ReplicationConsistencyGroup::{self.fake_rcg_id}'
                '/action/freezeApplyReplicationConsistencyGroup':
                    {'id': self.fake_rcg_id},
                f'/instances/ReplicationConsistencyGroup::{self.fake_rcg_id}'
                '/action/unfreezeApplyReplicationConsistencyGroup':
                    {'id': self.fake_rcg_id},
                f'/instances/ReplicationConsistencyGroup::{self.fake_rcg_id}'
                '/action/pauseReplicationConsistencyGroup':
                    {'id': self.fake_rcg_id},
                f'/instances/ReplicationConsistencyGroup::{self.fake_rcg_id}'
                '/action/resumeReplicationConsistencyGroup':
                    {'id': self.fake_rcg_id},
                f'/instances/ReplicationConsistencyGroup::{self.fake_rcg_id}'
                '/action/ModifyReplicationConsistencyGroupRpo':
                    {'id': self.fake_rcg_id},
                f'/instances/ReplicationConsistencyGroup::{self.fake_rcg_id}'
                '/action/modifyReplicationConsistencyGroupTargetVolumeAccessMode':
                    {'id': self.fake_rcg_id},
                f'/instances/ReplicationConsistencyGroup::{self.fake_rcg_id}'
                '/action/setReplicationConsistencyGroupConsistent':
                    {'id': self.fake_rcg_id},
                f'/instances/ReplicationConsistencyGroup::{self.fake_rcg_id}'
                '/action/setReplicationConsistencyGroupInconsistent':
                    {'id': self.fake_rcg_id},
                f'/instances/ReplicationConsistencyGroup::{self.fake_rcg_id}'
                '/action/renameReplicationConsistencyGroup':
                    {'id': self.fake_rcg_id},
                f'/instances/ReplicationConsistencyGroup::{self.fake_rcg_id}'
                '/action/removeReplicationConsistencyGroup':
                    {'id': self.fake_rcg_id},
                f'/instances/ReplicationConsistencyGroup::{self.fake_rcg_id}'
                '/action/failoverReplicationConsistencyGroup':
                    {'id': self.fake_rcg_id},
                f'/instances/ReplicationConsistencyGroup::{self.fake_rcg_id}'
                '/action/reverseReplicationConsistencyGroup':
                    {'id': self.fake_rcg_id},
                f'/instances/ReplicationConsistencyGroup::{self.fake_rcg_id}'
                '/action/restoreReplicationConsistencyGroup':
                    {'id': self.fake_rcg_id},
                f'/instances/ReplicationConsistencyGroup::{self.fake_rcg_id}'
                '/action/switchoverReplicationConsistencyGroup':
                    {'id': self.fake_rcg_id},
                f'/instances/ReplicationConsistencyGroup::{self.fake_rcg_id}'
                '/action/syncNowReplicationConsistencyGroup':
                    {'id': self.fake_rcg_id},
                f'/instances/ReplicationConsistencyGroup::{self.fake_rcg_id}'
                '/relationships/ReplicationPair':
                    {'id': self.fake_rcg_id},
                '/types/ReplicationConsistencyGroup'
                '/instances/action/querySelectedStatistics': {
                    self.fake_rcg_id: {'thinCapacityInUseInKb': 0}
                },
            },
            self.RESPONSE_MODE.Invalid: {
                '/types/ReplicationConsistencyGroup/instances':
                    {},
            }
        }


    def test_rcg_create_snapshots(self):
        """
        Test the create_snapshot method.
        """
        self.client.replication_consistency_group.create_snapshot(self.fake_rcg_id)

    def test_add_rcg(self):
        """
        Test the create method.
        """
        self.client.replication_consistency_group.create\
            (rpo=20, protection_domain_id='1',
             remote_protection_domain_id='1',
             peer_mdm_id='1', destination_system_id='1',
             name='test', force_ignore_consistency=False,
             activity_mode=None)

    def test_remove_rcg(self):
        """
        Test the delete method.
        """
        self.client.replication_consistency_group.delete(self.fake_rcg_id)

    def test_freeze_rcg(self):
        """
        Test the freeze method.
        """
        self.client.replication_consistency_group.freeze(self.fake_rcg_id)

    def test_unfreeze_rcg(self):
        """
        Test the unfreeze method.
        """
        self.client.replication_consistency_group.unfreeze(self.fake_rcg_id)

    def test_activate(self):
        """
        Test the activate method.
        """
        self.client.replication_consistency_group.activate(self.fake_rcg_id)

    def test_inactivate(self):
        """
        Test the inactivate method.
        """
        self.client.replication_consistency_group.inactivate(self.fake_rcg_id)

    def test_pause(self):
        """
        Test the pause method.
        """
        self.client.replication_consistency_group.pause(
            self.fake_rcg_id, pause_mode="StopDataTransfer")

    def test_resume(self):
        """
        Test the resume method.
        """
        self.client.replication_consistency_group.resume(self.fake_rcg_id)

    def test_failover(self):
        """
        Test the failover method.
        """
        self.client.replication_consistency_group.failover(self.fake_rcg_id)

    def test_reverse(self):
        """
        Test the reverse method.
        """
        self.client.replication_consistency_group.reverse(self.fake_rcg_id)

    def test_restore(self):
        """
        Test the restore method.
        """
        self.client.replication_consistency_group.restore(self.fake_rcg_id)

    def test_sync(self):
        """
        Test the sync method.
        """
        self.client.replication_consistency_group.sync(self.fake_rcg_id)

    def test_switchover(self):
        """
        Test the switchover method.
        """
        self.client.replication_consistency_group.switchover(self.fake_rcg_id)

    def test_set_as_consistent(self):
        """
        Test the set_as_consistent method.
        """
        self.client.replication_consistency_group.set_as_consistent(self.fake_rcg_id)

    def test_set_as_inconsistent(self):
        """
        Test the set_as_inconsistent method.
        """
        self.client.replication_consistency_group.set_as_inconsistent(self.fake_rcg_id)

    def test_modify_rpo(self):
        """
        Test the modify_rpo method.
        """
        self.client.replication_consistency_group.modify_rpo(self.fake_rcg_id, rpo_in_seconds=30)

    def test_modify_target_volume_access_mode(self):
        """
        Test the modify_target_volume_access_mode method.
        """
        self.client.replication_consistency_group.modify_target_volume_access_mode\
            (self.fake_rcg_id, target_volume_access_mode=None)

    def test_rename_rcg(self):
        """
        Test the rename_rcg method.
        """
        self.client.replication_consistency_group.rename_rcg(self.fake_rcg_id, new_name="rename")

    def test_get_replication_pairs(self):
        """
        Test the get_replication_pairs method.
        """
        self.client.replication_consistency_group.get_replication_pairs(self.fake_rcg_id)

    def test_get_all_statistics(self):
        """
        Test the get_all_statistics method.
        """
        self.client.replication_consistency_group.get_all_statistics(True)

    def test_rename_rcg_bad_status(self):
        """
        Test the rename_rcg method with bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexFailEntityOperation,
                              self.client.replication_consistency_group.rename_rcg,
                              self.fake_rcg_id,
                              new_name='rename')

    def test_create_rcg_bad_status(self):
        """
        Test the create method with bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexFailCreating,
                              self.client.replication_consistency_group.create,
                              rpo=20, protection_domain_id='1',
                              remote_protection_domain_id='1',
                              peer_mdm_id='1', destination_system_id='1',
                              name='test', force_ignore_consistency=False,
                              activity_mode=None)

    def test_delete_rcg_bad_status(self):
        """
        Test the delete method with bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexFailDeleting,
                              self.client.replication_consistency_group.delete,
                              self.fake_rcg_id)

    def test_get_all_statistics_bad_status(self):
        """
        Test the get_all_statistics method with bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexClientException,
                              self.client.replication_consistency_group.get_all_statistics,
                              False)

    def test_replication_consistency_group_query_selected_statistics(self):
        """
        Test the query_selected_statistics method of the ReplicationConsistencyGroupClient.
        """
        ret = self.client.replication_consistency_group.query_selected_statistics(
            properties=["thinCapacityInUseInKb"]
        )
        assert ret.get(self.fake_rcg_id).get("thinCapacityInUseInKb") == 0

    def test_replication_consistency_group_query_selected_statistics_bad_status(self):
        """
        Test the query_selected_statistics method of the ReplicationConsistencyGroupClient
        with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(
                exceptions.PowerFlexFailQuerying,
                self.client.replication_consistency_group.query_selected_statistics,
                properties=["thinCapacityInUseInKb"],
            )
