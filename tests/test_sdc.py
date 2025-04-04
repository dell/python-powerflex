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
import tests


class TestSdcClient(tests.PyPowerFlexTestCase):
    def setUp(self):
        super(TestSdcClient, self).setUp()
        self.client.initialize()
        self.fake_sdc_id = '1'

        self.MOCK_RESPONSES = {
            self.RESPONSE_MODE.Valid: {
                '/types/Sdc/instances':
                    {'id': self.fake_sdc_id},
                '/instances/Sdc::{}'.format(self.fake_sdc_id):
                    {'id': self.fake_sdc_id},
                '/instances/Sdc::{}'
                '/action/removeSdc'.format(self.fake_sdc_id):
                    {},
                '/instances/Sdc::{}'
                '/relationships/Volume'.format(self.fake_sdc_id):
                    [],
                '/instances/Sdc::{}'
                '/action/setSdcName'.format(self.fake_sdc_id):
                    {},
                '/instances/Sdc::{}'
                '/action/setSdcPerformanceParameters'.format(self.fake_sdc_id):
                    {},
            }
        }

    def test_sdc_delete(self):
        self.client.sdc.delete(self.fake_sdc_id)

    def test_sdc_delete_bad_status(self):
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexFailDeleting,
                              self.client.sdc.delete,
                              self.fake_sdc_id)

    def test_sdc_get_mapped_volumes(self):
        self.client.sdc.get_mapped_volumes(self.fake_sdc_id)

    def test_sdc_get_mapped_volumes_bad_status(self):
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexClientException,
                              self.client.sdc.get_mapped_volumes,
                              self.fake_sdc_id)

    def test_sdc_rename(self):
        self.client.sdc.rename(self.fake_sdc_id, name='new_name')

    def test_sdc_rename_bad_status(self):
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexFailRenaming,
                              self.client.sdc.rename,
                              self.fake_sdc_id,
                              name='new_name')

    def test_set_performance_profile(self):
        self.client.sdc.set_performance_profile(self.fake_sdc_id, 'Compact')

    def test_set_performance_profile_bad_status(self):
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexFailEntityOperation,
                              self.client.sdc.set_performance_profile,
                              self.fake_sdc_id,
                              'Compact')
