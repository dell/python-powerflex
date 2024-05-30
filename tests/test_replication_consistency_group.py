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

from PyPowerFlex import exceptions
from PyPowerFlex.objects import replication_consistency_group as rcg
import tests


class TestReplicationConsistencyGroupClient(tests.PyPowerFlexTestCase):
    def setUp(self):
        super(TestReplicationConsistencyGroupClient, self).setUp()
        self.client.initialize()
        self.fake_rcg_id = '1'

        self.MOCK_RESPONSES = {
            self.RESPONSE_MODE.Valid: {
                '/types/ReplicationConsistencyGroup/instances':
                    {'id': self.fake_rcg_id},
                '/instances/ReplicationConsistencyGroup::{}'.format(self.fake_rcg_id):
                    {'id': self.fake_rcg_id},
                '/instances/ReplicationConsistencyGroup::{}'
                '/action/createReplicationConsistencyGroupSnapshots'.format(self.fake_rcg_id):
                    {},
                '/instances/ReplicationConsistencyGroup::{}'.format(self.fake_rcg_id):
                    {'id': self.fake_rcg_id},
                '/instances/ReplicationConsistencyGroup::{}'
                '/action/activateReplicationConsistencyGroup'.format(self.fake_rcg_id):
                    {'id': self.fake_rcg_id},
                '/instances/ReplicationConsistencyGroup::{}'
                '/action/terminateReplicationConsistencyGroup'.format(self.fake_rcg_id):
                    {'id': self.fake_rcg_id},
                '/instances/ReplicationConsistencyGroup::{}'
                '/action/terminateReplicationConsistencyGroup'.format(self.fake_rcg_id):
                    {'id': self.fake_rcg_id},
                '/instances/ReplicationConsistencyGroup::{}'
                '/action/freezeApplyReplicationConsistencyGroup'.format(self.fake_rcg_id):
                    {'id': self.fake_rcg_id},
                '/instances/ReplicationConsistencyGroup::{}'
                '/action/unfreezeApplyReplicationConsistencyGroup'.format(self.fake_rcg_id):
                    {'id': self.fake_rcg_id},
                '/instances/ReplicationConsistencyGroup::{}'
                '/action/pauseReplicationConsistencyGroup'.format(self.fake_rcg_id):
                    {'id': self.fake_rcg_id},
                '/instances/ReplicationConsistencyGroup::{}'
                '/action/resumeReplicationConsistencyGroup'.format(self.fake_rcg_id):
                    {'id': self.fake_rcg_id},
                '/instances/ReplicationConsistencyGroup::{}'
                '/action/ModifyReplicationConsistencyGroupRpo'.format(self.fake_rcg_id):
                    {'id': self.fake_rcg_id},
                '/instances/ReplicationConsistencyGroup::{}'
                '/action/modifyReplicationConsistencyGroupTargetVolumeAccessMode'.format(self.fake_rcg_id):
                    {'id': self.fake_rcg_id},
                '/instances/ReplicationConsistencyGroup::{}'
                '/action/setReplicationConsistencyGroupConsistent'.format(self.fake_rcg_id):
                    {'id': self.fake_rcg_id},
                '/instances/ReplicationConsistencyGroup::{}'
                '/action/setReplicationConsistencyGroupInconsistent'.format(self.fake_rcg_id):
                    {'id': self.fake_rcg_id},
                '/instances/ReplicationConsistencyGroup::{}'
                '/action/renameReplicationConsistencyGroup'.format(self.fake_rcg_id):
                    {'id': self.fake_rcg_id},
                '/instances/ReplicationConsistencyGroup::{}'
                '/action/removeReplicationConsistencyGroup'.format(self.fake_rcg_id):
                    {'id': self.fake_rcg_id},
                '/instances/ReplicationConsistencyGroup::{}'
                '/action/failoverReplicationConsistencyGroup'.format(self.fake_rcg_id):
                    {'id': self.fake_rcg_id},
                '/instances/ReplicationConsistencyGroup::{}'
                '/action/reverseReplicationConsistencyGroup'.format(self.fake_rcg_id):
                    {'id': self.fake_rcg_id},
                '/instances/ReplicationConsistencyGroup::{}'
                '/action/restoreReplicationConsistencyGroup'.format(self.fake_rcg_id):
                    {'id': self.fake_rcg_id},
                '/instances/ReplicationConsistencyGroup::{}'
                '/action/switchoverReplicationConsistencyGroup'.format(self.fake_rcg_id):
                    {'id': self.fake_rcg_id},
                '/instances/ReplicationConsistencyGroup::{}'
                '/action/syncNowReplicationConsistencyGroup'.format(self.fake_rcg_id):
                    {'id': self.fake_rcg_id},
                '/instances/ReplicationConsistencyGroup::{}'
                '/relationships/ReplicationPair'.format(self.fake_rcg_id):
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
        self.client.replication_consistency_group.create_snapshot(self.fake_rcg_id)

    def test_add_rcg(self):
        self.client.replication_consistency_group.create\
            (rpo=20, protection_domain_id='1',
             remote_protection_domain_id='1',
             peer_mdm_id='1', destination_system_id='1',
             name='test', force_ignore_consistency=False,
             activity_mode=None)

    def test_remove_rcg(self):
        self.client.replication_consistency_group.delete(self.fake_rcg_id)

    def test_freeze_rcg(self):
        self.client.replication_consistency_group.freeze(self.fake_rcg_id)

    def test_unfreeze_rcg(self):
        self.client.replication_consistency_group.unfreeze(self.fake_rcg_id)

    def test_activate(self):
        self.client.replication_consistency_group.activate(self.fake_rcg_id)

    def test_inactivate(self):
        self.client.replication_consistency_group.inactivate(self.fake_rcg_id)

    def test_pause(self):
        self.client.replication_consistency_group.pause(self.fake_rcg_id, pause_mode="StopDataTransfer")

    def test_resume(self):
        self.client.replication_consistency_group.resume(self.fake_rcg_id)

    def test_failover(self):
        self.client.replication_consistency_group.failover(self.fake_rcg_id)

    def test_reverse(self):
        self.client.replication_consistency_group.reverse(self.fake_rcg_id)

    def test_restore(self):
        self.client.replication_consistency_group.restore(self.fake_rcg_id)

    def test_sync(self):
        self.client.replication_consistency_group.sync(self.fake_rcg_id)

    def test_switchover(self):
        self.client.replication_consistency_group.switchover(self.fake_rcg_id)

    def test_set_as_consistent(self):
        self.client.replication_consistency_group.set_as_consistent(self.fake_rcg_id)

    def test_set_as_inconsistent(self):
        self.client.replication_consistency_group.set_as_inconsistent(self.fake_rcg_id)

    def test_modify_rpo(self):
        self.client.replication_consistency_group.modify_rpo(self.fake_rcg_id, rpo_in_seconds=30)

    def test_modify_target_volume_access_mode(self):
        self.client.replication_consistency_group.modify_target_volume_access_mode\
            (self.fake_rcg_id, target_volume_access_mode=None)

    def test_rename_rcg(self):
        self.client.replication_consistency_group.rename_rcg(self.fake_rcg_id, new_name="rename")

    def test_get_replication_pairs(self):
        self.client.replication_consistency_group.get_replication_pairs(self.fake_rcg_id)

    def test_get_all_statistics(self):
        self.client.replication_consistency_group.get_all_statistics(True)

    def test_rename_rcg_bad_status(self):
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexFailEntityOperation,
                              self.client.replication_consistency_group.rename_rcg,
                              self.fake_rcg_id,
                              new_name='rename')

    def test_create_rcg_bad_status(self):
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexFailCreating,
                              self.client.replication_consistency_group.create,
                              rpo=20, protection_domain_id='1',
                              remote_protection_domain_id='1',
                              peer_mdm_id='1', destination_system_id='1',
                              name='test', force_ignore_consistency=False,
                              activity_mode=None)

    def test_delete_rcg_bad_status(self):
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexFailDeleting,
                              self.client.replication_consistency_group.delete,
                              self.fake_rcg_id)

    def test_get_all_statistics_bad_status(self):
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexClientException,
                              self.client.replication_consistency_group.get_all_statistics,
                              False)

    def test_replication_consistency_group_query_selected_statistics(self):
        ret = self.client.replication_consistency_group.query_selected_statistics(
            properties=["thinCapacityInUseInKb"]
        )
        assert ret.get(self.fake_rcg_id).get("thinCapacityInUseInKb") == 0

    def test_replication_consistency_group_query_selected_statistics_bad_status(self):
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(
                exceptions.PowerFlexFailQuerying,
                self.client.replication_consistency_group.query_selected_statistics,
                properties=["thinCapacityInUseInKb"],
            )
