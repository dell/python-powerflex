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

"""Module for testing firmware repository client."""

# pylint: disable=invalid-name

from PyPowerFlex import exceptions
import tests


class TestFirmwareRepositoryClient(tests.PyPowerFlexTestCase):
    """
    Test class for FirmwareRepositoryClient.
    """
    def setUp(self):
        """
        Set up the test environment.
        """
        super().setUp()
        self.client.initialize()

        self.MOCK_RESPONSES = {
            self.RESPONSE_MODE.Valid: {
                '/V1/FirmwareRepository': {},
                '/V1/FirmwareRepository?related=False&bundles=False&components=False': {}
            }
        }

    def test_firmware_repository_get(self):
        """
        Test the get method of the FirmwareRepositoryClient.
        """
        self.client.firmware_repository.get()

    def test_firmware_repository_get_with_query_params(self):
        """
        Test the get method of the FirmwareRepositoryClient with query parameters.
        """
        self.client.firmware_repository.get(related=False, bundles=False, components=False)

    def test_firmware_repository_get_bad_status(self):
        """
        Test the get method of the FirmwareRepositoryClient with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexClientException,
                              self.client.firmware_repository.get)
