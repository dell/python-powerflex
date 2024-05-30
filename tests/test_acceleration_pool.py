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
from PyPowerFlex.objects import acceleration_pool
import tests


class TestAccelerationPoolClient(tests.PyPowerFlexTestCase):
    def setUp(self):
        super(TestAccelerationPoolClient, self).setUp()
        self.client.initialize()
        self.fake_pd_id = '1'
        self.fake_ap_id = '1'
        self.fake_device_id = '1'

        self.MOCK_RESPONSES = {
            self.RESPONSE_MODE.Valid: {
                '/types/AccelerationPool/instances':
                    {'id': self.fake_ap_id},
                '/instances/AccelerationPool::{}'.format(self.fake_ap_id):
                    {'id': self.fake_ap_id},
                '/instances/AccelerationPool::{}'
                '/action/removeAccelerationPool'.format(self.fake_ap_id):
                    {},
                '/types/AccelerationPool'
                '/instances/action/querySelectedStatistics': {
                    self.fake_ap_id: {'accelerationDeviceIds': [self.fake_device_id]}
                },
            },
            self.RESPONSE_MODE.Invalid: {
                '/types/AccelerationPool/instances':
                    {},
            }
        }

    def test_acceleration_pool_create(self):
        self.client.acceleration_pool.create(
            media_type=acceleration_pool.MediaType.ssd,
            protection_domain_id=self.fake_pd_id,
            isRfcache=True)

    def test_acceleration_pool_create_bad_status(self):
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexFailCreating,
                              self.client.acceleration_pool.create,
                              media_type=acceleration_pool.MediaType.ssd,
                              protection_domain_id=self.fake_pd_id,
                              isRfcache=True)

    def test_acceleration_pool_create_no_id_in_response(self):
        with self.http_response_mode(self.RESPONSE_MODE.Invalid):
            self.assertRaises(KeyError,
                              self.client.acceleration_pool.create,
                              media_type=acceleration_pool.MediaType.ssd,
                              protection_domain_id=self.fake_pd_id,
                              isRfcache=True)

    def test_acceleration_pool_delete(self):
        self.client.acceleration_pool.delete(self.fake_ap_id)

    def test_acceleration_pool_delete_bad_status(self):
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexFailDeleting,
                              self.client.acceleration_pool.delete,
                              self.fake_ap_id)

    def test_acceleration_pool_query_selected_statistics(self):
        ret = self.client.acceleration_pool.query_selected_statistics(
            properties=["accelerationDeviceIds"]
        )
        assert ret.get(self.fake_ap_id).get("accelerationDeviceIds") == [
            self.fake_device_id
        ]

    def test_acceleration_pool_query_selected_statistics_bad_status(self):
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(
                exceptions.PowerFlexFailQuerying,
                self.client.acceleration_pool.query_selected_statistics,
                properties=["accelerationDeviceIds"],
            )
