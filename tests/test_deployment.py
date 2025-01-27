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

"""Module for testing deployment client."""

# pylint: disable=invalid-name

from PyPowerFlex import exceptions
import tests


class TestDeploymentClient(tests.PyPowerFlexTestCase):
    """
    Test class for the DeploymentClient.
    """
    def setUp(self):
        """
        Set up the test environment.
        """
        super().setUp()
        self.client.initialize()
        self.RESPONSE_204 = "<Response 204>"
        self.deployment_id = '8aaa03a88de961fa018de9c882d20301'
        self.rg_data = {}
        self.MOCK_RESPONSES = {
            self.RESPONSE_MODE.Valid: {
                '/V1/Deployment': {},
                '/V1/Deployment?filter=co,name,Partial&includeDevices=False': {},
                f'/V1/Deployment/{self.deployment_id}': {},
                '/V1/Deployment/validate': {}
            }
        }

    def test_deployment_get(self):
        """
        Test the get method of the DeploymentClient.
        """
        self.client.deployment.get()

    def test_deployment_get_with_query_params(self):
        """
        Test the get method of the DeploymentClient with query parameters.
        """
        self.client.deployment.get(filters=['co,name,Partial'], include_devices=False)

    def test_deployment_get_by_id(self):
        """
        Test the get_by_id method of the DeploymentClient.
        """
        self.client.deployment.get_by_id(self.deployment_id)

    def test_deployment_get_bad_status(self):
        """
        Test the get method of the DeploymentClient with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexClientException,
                              self.client.deployment.get)

    def test_deployment_get_by_id_bad_status(self):
        """
        Test the get_by_id method of the DeploymentClient with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexClientException,
                              self.client.deployment.get_by_id,
                              self.deployment_id)

    def test_deployment_create(self):
        """
        Test the create method of the DeploymentClient.
        """
        self.client.deployment.create(self.rg_data)

    def test_deployment_create_bad_status(self):
        """
        Test the create method of the DeploymentClient with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexClientException,
                              self.client.deployment.create,
                              self.rg_data)

    def test_deployment_edit(self):
        """
        Test the edit method of the DeploymentClient.
        """
        self.client.deployment.edit(self.deployment_id, self.rg_data)

    def test_deployment_edit_bad_status(self):
        """
        Test the edit method of the DeploymentClient with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexClientException,
                              self.client.deployment.edit,
                              self.deployment_id,
                              self.rg_data)

    def test_deployment_delete(self):
        """
        Test the delete method of the DeploymentClient.
        """
        url = f'/V1/Deployment/{self.deployment_id}'
        self.MOCK_RESPONSES[self.RESPONSE_MODE.Valid][url] = self.RESPONSE_204
        self.client.deployment.delete(self.deployment_id)

    def test_deployment_delete_bad_status(self):
        """
        Test the delete method of the DeploymentClient with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexClientException,
                              self.client.deployment.delete,
                              self.deployment_id)

    def test_deployment_validate(self):
        """
        Test the validate method of the DeploymentClient.
        """
        self.client.deployment.validate(self.rg_data)

    def test_deployment_validate_bad_status(self):
        """
        Test the validate method of the DeploymentClient with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexClientException,
                              self.client.deployment.validate,
                              self.rg_data)
