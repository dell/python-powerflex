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

"""Module for testing device client."""

# pylint: disable=invalid-name

from PyPowerFlex import exceptions
from PyPowerFlex.objects.device import MediaType
import tests


class TestDeviceClient(tests.PyPowerFlexTestCase):
    """
    Test class for DeviceClient.
    """
    def setUp(self):
        """
        Set up the test environment.
        """
        super().setUp()
        self.client.initialize()
        self.fake_device_id = '1'
        self.fake_sds_id = '1'
        self.fake_sp_id = '1'
        self.fake_accp_id = '1'

        self.MOCK_RESPONSES = {
            self.RESPONSE_MODE.Valid: {
                '/types/Device/instances':
                    {'id': self.fake_device_id},
                f'/instances/Device::{self.fake_device_id}':
                    {'id': self.fake_device_id},
                f'/instances/Device::{self.fake_device_id}'
                '/action/removeDevice':
                    {},
                f'/instances/Device::{self.fake_device_id}'
                '/action/setDeviceName':
                    {},
                f'/instances/Device::{self.fake_device_id}'
                '/action/setMediaType':
                    {},
                '/types/Device'
                '/instances/action/querySelectedStatistics': {
                    self.fake_device_id: {'avgReadLatencyInMicrosec': 0}
                },
            },
            self.RESPONSE_MODE.Invalid: {
                '/types/Device/instances':
                    {},
            }
        }

    def test_device_create(self):
        """
        Test device creation.
        """
        self.client.device.create('/dev/sda',
                                  self.fake_sds_id,
                                  media_type=MediaType.ssd,
                                  storage_pool_id=self.fake_sp_id)

    def test_device_create_bad_status(self):
        """
        Test device creation with bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexFailCreating,
                              self.client.device.create,
                              '/dev/sda',
                              self.fake_sds_id,
                              media_type=MediaType.ssd,
                              storage_pool_id=self.fake_sp_id)

    def test_device_create_no_id_in_response(self):
        """
        Test device creation with no id in response.
        """
        with self.http_response_mode(self.RESPONSE_MODE.Invalid):
            self.assertRaises(KeyError,
                              self.client.device.create,
                              '/dev/sda',
                              self.fake_sds_id,
                              media_type=MediaType.ssd,
                              storage_pool_id=self.fake_sp_id)

    def test_device_create_storage_pool_id_and_acc_pool_id_are_set(self):
        """
        Test device creation with both storage pool id and acceleration pool id set.
        """
        self.assertRaises(exceptions.InvalidInput,
                          self.client.device.create,
                          '/dev/sda',
                          self.fake_sds_id,
                          acceleration_pool_id=self.fake_accp_id,
                          media_type=MediaType.ssd,
                          storage_pool_id=self.fake_sp_id)

    def test_device_delete(self):
        """
        Test device deletion.
        """
        self.client.device.delete(self.fake_device_id)

    def test_device_delete_bad_status(self):
        """
        Test device deletion with bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexFailDeleting,
                              self.client.device.delete,
                              self.fake_device_id)

    def test_device_rename(self):
        """
        Test device renaming.
        """
        self.client.device.rename(self.fake_device_id, name='new_name')

    def test_device_rename_bad_status(self):
        """
        Test device renaming with bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexFailRenaming,
                              self.client.device.rename,
                              self.fake_device_id,
                              name='new_name')

    def test_device_set_media_type(self):
        """
        Test device media type setting.
        """
        self.client.device.set_media_type(
            self.fake_device_id,
            media_type=MediaType.hdd
        )

    def test_device_set_media_type_bad_status(self):
        """
        Test device media type setting with bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(
                exceptions.PowerFlexClientException,
                self.client.device.set_media_type,
                self.fake_device_id,
                media_type=MediaType.hdd
            )

    def test_device_query_selected_statistics(self):
        """
        Test device query selected statistics.
        """
        ret = self.client.device.query_selected_statistics(
            properties=["avgReadLatencyInMicrosec"]
        )
        assert ret.get(self.fake_device_id).get("avgReadLatencyInMicrosec") == 0

    def test_device_query_selected_statistics_bad_status(self):
        """
        Test device query selected statistics with bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(
                exceptions.PowerFlexFailQuerying,
                self.client.device.query_selected_statistics,
                properties=["avgReadLatencyInMicrosec"],
            )
