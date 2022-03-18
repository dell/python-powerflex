# Copyright (c) 2020 Dell Inc. or its subsidiaries.
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
from PyPowerFlex.objects import system
import tests


class TestSystemClient(tests.PyPowerFlexTestCase):
    def setUp(self):
        super(TestSystemClient, self).setUp()
        self.client.initialize()
        self.fake_system_id = '1'
        self.fake_cg_id = '1'
        self.fake_snapshot_defs = [system.SnapshotDef('123', 'snap_1')]

        self.MOCK_RESPONSES = {
            self.RESPONSE_MODE.Valid: {
                '/instances/System::{}'
                '/action'
                '/removeConsistencyGroupSnapshots'.format(self.fake_system_id):
                    {},
                '/instances/System::{}'
                '/action/snapshotVolumes'.format(self.fake_system_id):
                    {},
            },
            self.RESPONSE_MODE.Invalid: {
                '/version': 'invalid_version_format'
            },
        }

    def test_system_api_version(self):
        self.client.system.api_version()
        self.assertEqual(3, self.get_mock.call_count)

    def test_system_api_version_bad_status(self):
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexFailQuerying,
                              self.client.system.api_version,
                              cached=False)

    def test_system_api_version_invalid_format(self):
        with self.http_response_mode(self.RESPONSE_MODE.Invalid):
            self.assertRaises(exceptions.PowerFlexClientException,
                              self.client.system.api_version,
                              cached=False)

    def test_system_api_version_cached(self):
        self.client.system.api_version()
        self.client.system.api_version()
        self.client.system.api_version()
        self.assertEqual(3, self.get_mock.call_count)

    def test_system_remove_cg_snapshots(self):
        self.client.system.remove_cg_snapshots(self.fake_system_id,
                                               self.fake_cg_id)

    def test_system_remove_cg_snapshots_bad_status(self):
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexClientException,
                              self.client.system.remove_cg_snapshots,
                              self.fake_system_id,
                              self.fake_cg_id)

    def test_system_snapshot_volumes(self):
        self.client.system.snapshot_volumes(self.fake_system_id,
                                            self.fake_snapshot_defs)

    def test_system_snapshot_volumes_bad_status(self):
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexClientException,
                              self.client.system.snapshot_volumes,
                              self.fake_system_id,
                              self.fake_snapshot_defs)
