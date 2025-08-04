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

"""Module for testing device group client."""

# pylint: disable=invalid-name

from PyPowerFlex import exceptions
from PyPowerFlex.objects.gen2.device_group import MediaType
from tests.common import PyPowerFlexTestCase


@PyPowerFlexTestCase.version('5.0')
class TestDeviceClient(PyPowerFlexTestCase):
    """
    Test class for DeviceGroupClient.
    """
    def setUp(self):
        """
        Set up the test environment.
        """
        super().setUp()
        self.client.initialize()
        self.fake_device_group_id = '1'
        self.fake_device_group_name = '1'
        self.fake_protection_domain_id = '1'

        self.MOCK_RESPONSES = {
            self.RESPONSE_MODE.Valid: {
                '/types/DeviceGroup/instances':
                    {'id': self.fake_device_group_id},
                f'/instances/DeviceGroup::{self.fake_device_group_id}':
                    {'id': self.fake_device_group_id},
                f'/instances/DeviceGroup::{self.fake_device_group_id}'
                '/action/removeDeviceGroup':
                    {},
                f'/instances/DeviceGroup::{self.fake_device_group_id}'
                '/action/modifyDeviceGroup':
                    {},
                f'/instances/DeviceGroup::{self.fake_device_group_id}'
                '/action/queryUsableCapacity':{
                    self.fake_device_group_id: {'numProtectionSlices': 2}
                },
                '/dtapi/rest/v1/metrics/query': {
                    self.fake_device_group_id: {'physical_total': 10995116277760}
                },
            },
            self.RESPONSE_MODE.Invalid: {
                '/types/DeviceGroup/instances':
                    {},
            }
        }

    def test_device_group_create(self):
        """
        Test device creation.
        """
        self.client.device_group.create(name=self.fake_device_group_name,
                                        protection_domain_id=self.fake_protection_domain_id,
                                        media_type=MediaType.ssd,
                                        spare_device_count=1,
                                        spare_node_count=1)

    def test_device_group_create_bad_status(self):
        """
        Test device creation with bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexFailCreating,
                              self.client.device_group.create,
                              name=self.fake_device_group_name,
                              protection_domain_id=self.fake_protection_domain_id,
                              media_type=MediaType.ssd,
                              spare_device_count=1,
                              spare_node_count=1)

    def test_device_group_create_no_id_in_response(self):
        """
        Test device creation with no id in response.
        """
        with self.http_response_mode(self.RESPONSE_MODE.Invalid):
            self.assertRaises(KeyError,
                              self.client.device_group.create,
                              name=self.fake_device_group_name,
                              protection_domain_id=self.fake_protection_domain_id,
                              media_type=MediaType.ssd,
                              spare_device_count=1,
                              spare_node_count=1)

    def test_device_group_create_name_invalid_input(self):
        """
        Test device creation with invalid name set.
        """
        with self.http_response_mode(self.RESPONSE_MODE.Invalid):
            self.assertRaises(exceptions.InvalidInput,
                              self.client.device_group.create,
                              name=None,
                              protection_domain_id=self.fake_protection_domain_id,
                              media_type=MediaType.ssd,
                              spare_device_count=1,
                              spare_node_count=1)

    def test_device_group_delete(self):
        """
        Test device deletion.
        """
        self.client.device_group.delete(self.fake_device_group_id)

    def test_device_group_delete_bad_status(self):
        """
        Test device deletion with bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexFailDeleting,
                              self.client.device_group.delete,
                              self.fake_device_group_id)

    def test_device_group_modify(self):
        """
        Test device modify.
        """
        self.client.device_group.modify(self.fake_device_group_id,
                                        new_name="new_name",
                                        spare_device_count=1,
                                        spare_node_count=1)

    def test_device_group_modify_bad_status(self):
        """
        Test device modify with bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexClientException,
                              self.client.device_group.modify,
                              self.fake_device_group_id,
                              new_name="new_name",
                              spare_device_count=1,
                              spare_node_count=1)

    def test_device_group_query_metrics(self):
        """
        Test device group query selected metrics.
        """
        ret = self.client.device_group.query_metrics(self.fake_device_group_id)
        assert ret.get(self.fake_device_group_id).get("physical_total") == 10995116277760

    def test_device_group_query_metrics_bad_status(self):
        """
        Test device group query selected metrics with bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(
                exceptions.PowerFlexFailQuerying,
                self.client.device_group.query_metrics,
                self.fake_device_group_id)

    def test_device_group_query_usable_capacity(self):
        """
        Test device group query_usable_capacity method.
        """
        ret = self.client.device_group.query_usable_capacity(self.fake_device_group_id)
        assert ret.get(self.fake_device_group_id).get("numProtectionSlices") == 2

    def test_device_group_query_metrics_bad_status(self):
        """
        Test device group query_usable_capacity with bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(
                exceptions.PowerFlexClientException,
                self.client.device_group.query_usable_capacity,
                self.fake_device_group_id)
