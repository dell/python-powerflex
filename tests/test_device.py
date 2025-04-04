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
from PyPowerFlex.objects.device import MediaType
import tests


class TestDeviceClient(tests.PyPowerFlexTestCase):
    def setUp(self):
        super(TestDeviceClient, self).setUp()
        self.client.initialize()
        self.fake_device_id = '1'
        self.fake_sds_id = '1'
        self.fake_sp_id = '1'
        self.fake_accp_id = '1'

        self.MOCK_RESPONSES = {
            self.RESPONSE_MODE.Valid: {
                '/types/Device/instances':
                    {'id': self.fake_device_id},
                '/instances/Device::{}'.format(self.fake_device_id):
                    {'id': self.fake_device_id},
                '/instances/Device::{}'
                '/action/removeDevice'.format(self.fake_device_id):
                    {},
                '/instances/Device::{}'
                '/action/setDeviceName'.format(self.fake_device_id):
                    {},
                '/instances/Device::{}'
                '/action/setMediaType'.format(self.fake_device_id):
                    {},
            },
            self.RESPONSE_MODE.Invalid: {
                '/types/Device/instances':
                    {},
            }
        }

    def test_device_create(self):
        self.client.device.create('/dev/sda',
                                  self.fake_sds_id,
                                  media_type=MediaType.ssd,
                                  storage_pool_id=self.fake_sp_id)

    def test_device_create_bad_status(self):
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexFailCreating,
                              self.client.device.create,
                              '/dev/sda',
                              self.fake_sds_id,
                              media_type=MediaType.ssd,
                              storage_pool_id=self.fake_sp_id)

    def test_device_create_no_id_in_response(self):
        with self.http_response_mode(self.RESPONSE_MODE.Invalid):
            self.assertRaises(KeyError,
                              self.client.device.create,
                              '/dev/sda',
                              self.fake_sds_id,
                              media_type=MediaType.ssd,
                              storage_pool_id=self.fake_sp_id)

    def test_device_create_storage_pool_id_and_acc_pool_id_are_set(self):
        self.assertRaises(exceptions.InvalidInput,
                          self.client.device.create,
                          '/dev/sda',
                          self.fake_sds_id,
                          acceleration_pool_id=self.fake_accp_id,
                          media_type=MediaType.ssd,
                          storage_pool_id=self.fake_sp_id)

    def test_device_delete(self):
        self.client.device.delete(self.fake_device_id)

    def test_device_delete_bad_status(self):
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexFailDeleting,
                              self.client.device.delete,
                              self.fake_device_id)

    def test_device_rename(self):
        self.client.device.rename(self.fake_device_id, name='new_name')

    def test_device_rename_bad_status(self):
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexFailRenaming,
                              self.client.device.rename,
                              self.fake_device_id,
                              name='new_name')

    def test_device_set_media_type(self):
        self.client.device.set_media_type(
            self.fake_device_id,
            media_type=MediaType.hdd
        )

    def test_device_set_media_type_bad_status(self):
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(
                exceptions.PowerFlexClientException,
                self.client.device.set_media_type,
                self.fake_device_id,
                media_type=MediaType.hdd
            )
