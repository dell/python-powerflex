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

"""Module for testing managed device client."""

# pylint: disable=invalid-name

from PyPowerFlex import exceptions
import tests


class TestManagedDeviceClient(tests.PyPowerFlexTestCase):
    """
    Test class for the ManagedDeviceClient.
    """
    def setUp(self):
        """
        Set up the test environment.
        """
        super().setUp()
        self.client.initialize()

        self.MOCK_RESPONSES = {
            self.RESPONSE_MODE.Valid: {
                '/V1/ManagedDevice': {},
                '/V1/ManagedDevice?filter=eq,deviceType,scaleio&sort=state': {}
            }
        }

    def test_managed_device_get(self):
        """
        Test the managed_device.get() method.
        """
        self.client.managed_device.get()

    def test_managed_device_get_with_query_params(self):
        """
        Test the managed_device.get() method with query parameters.
        """
        self.client.managed_device.get(filters=['eq,deviceType,scaleio'], sort="state")

    def test_managed_device_get_bad_status(self):
        """
        Test the managed_device.get() method with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexClientException,
                              self.client.managed_device.get)
