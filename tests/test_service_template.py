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

"""Module for testing service template client."""

# pylint: disable=invalid-name

from PyPowerFlex import exceptions
import tests


class TestServiceTemplateClient(tests.PyPowerFlexTestCase):
    """
    Test class for the ServiceTemplateClient.
    """
    def setUp(self):
        """
        Set up the test environment.
        """
        super().setUp()
        self.client.initialize()
        self.template_id = 1234
        self.MOCK_RESPONSES = {
            self.RESPONSE_MODE.Valid: {
                '/V1/ServiceTemplate': {},
                '/V1/ServiceTemplate?filter=eq,draft,False&limit=10&includeAttachments=False': {},
                f'/V1/ServiceTemplate/{self.template_id}?forDeployment=true': {}
            }
        }

    def test_service_template_get(self):
        """
        Test the get method of the ServiceTemplateClient.
        """
        self.client.service_template.get()

    def test_service_template_get_with_filters(self):
        """
        Test the get method of the ServiceTemplateClient with filters.
        """
        self.client.service_template.get(
            filters=['eq,draft,False'], limit=10, include_attachments=False)

    def test_service_template_get_bad_status(self):
        """
        Test the get method of the ServiceTemplateClient with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexClientException,
                              self.client.service_template.get)

    def test_service_template_get_by_id(self):
        """
        Test the get_by_id method of the ServiceTemplateClient.
        """
        self.client.service_template.get_by_id(self.template_id, for_deployment=True)

    def test_service_template_get_by_id_bad_status(self):
        """
        Test the get_by_id method of the ServiceTemplateClient with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexClientException,
                              self.client.service_template.get_by_id,
                              self.template_id, for_deployment=True)
