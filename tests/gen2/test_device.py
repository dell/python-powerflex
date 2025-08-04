# Copyright (c) 2025 Dell Inc. or its subsidiaries.
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

# pylint: disable=invalid-name,duplicate-code

from PyPowerFlex import exceptions
from PyPowerFlex.objects.gen2.device import MediaType
from tests.common import PyPowerFlexTestCase


@PyPowerFlexTestCase.version('5.0')
class TestDeviceClient(PyPowerFlexTestCase):
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
        self.fake_device_name = '1'
        self.fake_device_group_id = '1'
        self.fake_node_id = '1'

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
                '/action/setDeviceCapacityLimit':
                    {},
                f'/instances/Device::{self.fake_device_id}'
                '/action/updateDeviceOriginalPathname':
                    {},
                f'/instances/Device::{self.fake_device_id}'
                '/action/clearDeviceError':
                    {},
                f'/instances/Device::{self.fake_device_id}'
                '/action/activateDevice':
                    {},
                '/dtapi/rest/v1/metrics/query': {
                    self.fake_device_id: {'raw_total': 1099511627776}
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
        self.client.device.create(current_pathname='/dev/sda',
                                  device_group_id=self.fake_device_group_id,
                                  node_id=self.fake_node_id,
                                  media_type=MediaType.ssd,
                                  name=self.fake_device_name)

    def test_device_create_bad_status(self):
        """
        Test device creation with bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexFailCreating,
                              self.client.device.create,
                              current_pathname='/dev/sda',
                              device_group_id=self.fake_device_group_id,
                              node_id=self.fake_node_id,
                              media_type=MediaType.ssd,
                              name=self.fake_device_name)

    def test_device_create_no_id_in_response(self):
        """
        Test device creation with no id in response.
        """
        with self.http_response_mode(self.RESPONSE_MODE.Invalid):
            self.assertRaises(KeyError,
                              self.client.device.create,
                              current_pathname='/dev/sda',
                              device_group_id=self.fake_device_group_id,
                              node_id=self.fake_node_id,
                              media_type=MediaType.ssd,
                              name=self.fake_device_name)

    def test_device_create_node_id_invalid_input(self):
        """
        Test device creation with invalid node id set.
        """
        with self.http_response_mode(self.RESPONSE_MODE.Invalid):
            self.assertRaises(exceptions.InvalidInput,
                              self.client.device.create,
                              current_pathname='/dev/sda',
                              device_group_id=self.fake_device_group_id,
                              media_type=MediaType.ssd,
                              node_id=None,
                              name=self.fake_device_name)

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

    def test_device_update_pathname(self):
        """
        Test device update_pathname.
        """
        self.client.device.update_pathname(
            self.fake_device_id,
            new_pathname='/dev/sdb')

    def test_device_update_pathname_bad_status(self):
        """
        Test device update_pathname with bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(
                exceptions.PowerFlexClientException,
                self.client.device.update_pathname,
                self.fake_device_id,
                new_pathname='/dev/sdb')

    def test_device_set_capacity_limit(self):
        """
        Test device set_capacity_limit.
        """
        self.client.device.set_capacity_limit(
            self.fake_device_id,
            capacity_limit_gb=500)

    def test_device_set_capacity_limit_bad_status(self):
        """
        Test device set_capacity_limit with bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(
                exceptions.PowerFlexClientException,
                self.client.device.set_capacity_limit,
                self.fake_device_id,
                capacity_limit_gb=500)

    def test_device_clear_errors(self):
        """
        Test device clear_errors.
        """
        self.client.device.clear_errors(self.fake_device_id)

    def test_device_clear_errors_bad_status(self):
        """
        Test device clear_errors with bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(
                exceptions.PowerFlexClientException,
                self.client.device.clear_errors,
                self.fake_device_id)

    def test_device_activate(self):
        """
        Test device activate.
        """
        self.client.device.activate(self.fake_device_id, self.fake_node_id)

    def test_device_activate_bad_status(self):
        """
        Test device activate with bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(
                exceptions.PowerFlexClientException,
                self.client.device.clear_errors,
                self.fake_device_id,
                self.fake_node_id)

    def test_device_query_metrics(self):
        """
        Test device query selected metrics.
        """
        ret = self.client.device.query_device_metrics(self.fake_device_id)
        assert ret.get(self.fake_device_id).get("raw_total") == 1099511627776

    def test_device_query_metrics_bad_status(self):
        """
        Test device query selected metrics with bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(
                exceptions.PowerFlexClientException,
                self.client.device.query_device_metrics,
                self.fake_device_id)
