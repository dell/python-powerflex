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
from PyPowerFlex.objects import replication_pair
import tests


class TestReplicationPairClient(tests.PyPowerFlexTestCase):
    def setUp(self):
        super(TestReplicationPairClient, self).setUp()
        self.client.initialize()
        self.fake_replication_pair_id = '1'

        self.MOCK_RESPONSES = {
            self.RESPONSE_MODE.Valid: {
                '/types/ReplicationPair/instances':
                    {'id': self.fake_replication_pair_id},
                '/instances/ReplicationPair::{}'.format(self.fake_replication_pair_id):
                    {'id': self.fake_replication_pair_id},
                '/instances/ReplicationPair::{}'
                '/action/removeReplicationPair'.format(self.fake_replication_pair_id):
                    {},
                '/instances/ReplicationPair::{}'
                '/action/pausePairInitialCopy'.format(self.fake_replication_pair_id):
                    {'id': self.fake_replication_pair_id},
                '/instances/ReplicationPair::{}'
                '/action/resumePairInitialCopy'.format(self.fake_replication_pair_id):
                    {'id': self.fake_replication_pair_id},
                '/types/ReplicationPair'
                '/instances/action/querySelectedStatistics': {
                    self.fake_replication_pair_id: {'initialCopyProgress': 0}
                },
            },
            self.RESPONSE_MODE.Invalid: {
                '/types/ReplicationPair/instances':
                    {},
            }
        }

    def test_add_replication_pair(self):
        self.client.replication_pair.add\
            (source_vol_id='1', dest_vol_id='1',
             rcg_id='1', copy_type='OnlineCopy', name='test')

    def test_remove_replication_pair(self):
        self.client.replication_pair.remove(self.fake_replication_pair_id)

    def test_pause_online_copy(self):
        self.client.replication_pair.pause(self.fake_replication_pair_id)

    def test_resume_online_copy(self):
        self.client.replication_pair.resume(self.fake_replication_pair_id)

    def test_get_all_statistics(self):
        self.client.replication_pair.get_all_statistics()

    def test_add_replication_pair_bad_status(self):
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexFailCreating,
                              self.client.replication_pair.add,
                              source_vol_id='1', dest_vol_id='1',
                              rcg_id='1', copy_type='OnlineCopy', name='test')

    def test_remove_replication_pair_bad_status(self):
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexFailDeleting,
                              self.client.replication_pair.remove,
                              self.fake_replication_pair_id)

    def test_get_all_statistics_bad_status(self):
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexClientException,
                              self.client.replication_pair.get_all_statistics)

    def test_replication_pair_query_selected_statistics(self):
        ret = self.client.replication_pair.query_selected_statistics(
            properties=["initialCopyProgress"]
        )
        assert ret.get(self.fake_replication_pair_id).get("initialCopyProgress") == 0

    def test_replication_pair_query_selected_statistics_bad_status(self):
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(
                exceptions.PowerFlexFailQuerying,
                self.client.replication_pair.query_selected_statistics,
                properties=["initialCopyProgress"],
            )
