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

from urllib.parse import parse_qs, urlsplit

from PyPowerFlex import exceptions
from PyPowerFlex import utils
from tests.common import PyPowerFlexTestCase

@PyPowerFlexTestCase.version('4.5')
class TestManagedDeviceClient(PyPowerFlexTestCase):
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

    def test_query_values_round_trip(self):
        """Keep reserved characters inside their original query values."""
        filters = ['eq,name,R&D #1', 'eq,name,A+B%20', 'eq,name,caf\u00e9']
        uri = utils.build_uri_with_params(
            '/V1/ManagedDevice', filter=filters, offset=0, limit=None)
        parsed = urlsplit(uri)
        self.assertEqual(parsed.fragment, '')
        self.assertEqual(parse_qs(parsed.query), {
            'filter': filters, 'offset': ['0']})

    def test_query_omits_none_list_items(self):
        """Keep list ordering and omit unset scalar and list values."""
        uri = utils.build_uri_with_params(
            '/V1/ManagedDevice', filter=[None, 'eq,name,A&B', None],
            sort=None, limit=10)
        self.assertEqual(parse_qs(urlsplit(uri).query), {
            'filter': ['eq,name,A&B'], 'limit': ['10']})
