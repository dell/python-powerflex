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

"""Module for doing the deployment."""

# pylint: disable=arguments-renamed,too-many-arguments,too-many-positional-arguments,no-member

import logging
import requests
from PyPowerFlex import base_client
from PyPowerFlex import exceptions
from PyPowerFlex import utils
LOG = logging.getLogger(__name__)


class Deployment(base_client.EntityRequest):
    """
    A class representing Deployment client.
    """
    def get(
            self,
            filters=None,
            full=None,
            include_devices=None,
            include_template=None,
            limit=None,
            offset=None,
            sort=None):
        """
        Retrieve all Deployments with filter, sort, pagination
        :param filters: (Optional) The filters to apply to the results.
        :param full: (Optional) Whether to return full details for each result.
        :param include_devices: (Optional) Whether to include devices in the response.
        :param include_template: (Optional) Whether to include service templates in the response.
        :param limit: (Optional) Page limit.
        :param offset: (Optional) Pagination offset.
        :param sort: (Optional) The field to sort the results by.
        :return: A list of dictionary containing the retrieved Deployments.
        """
        params = {
            'filter': filters,
            'full': full,
            'sort': sort,
            'offset': offset,
            'limit': limit,
            'includeDevices': include_devices,
            'includeTemplate': include_template
        }
        r, response = self.send_get_request(
            utils.build_uri_with_params(
                self.deployment_url, **params))
        if r.status_code != requests.codes.ok:
            msg = f'Failed to retrieve deployments. Error: {response}'
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)
        return response

    def get_by_id(self, deployment_id):
        """
        Retrieve Deployment for specified ID.
        :param deployment_id: Deployment ID.
        :return: A dictionary containing the retrieved Deployment.
        """
        r, response = self.send_get_request(
            f'{self.deployment_url}/{deployment_id}')
        if r.status_code != requests.codes.ok:
            msg = (
                f'Failed to retrieve deployment by id {deployment_id}. Error: {response}')
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)
        return response

    def validate(self, rg_data):
        """
        Validates a new deployment.
        Args:
            rg_data (dict): The resource group data to be deployed.
        Returns:
            dict: The response from the deployment API.
        Raises:
            PowerFlexClientException: If the deployment fails.
        """
        r, response = self.send_post_request(
            f'{self.deployment_url}/validate', rg_data)
        if r.status_code != requests.codes.ok:
            msg = f'Failed to validate the deployment. Error: {response}'
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

        return response

    def create(self, rg_data):
        """
        Creates a new deployment.
        Args:
            rg_data (dict): The resource group data to be deployed.
        Returns:
            dict: The response from the deployment API.
        Raises:
            PowerFlexClientException: If the deployment fails.
        """
        r, response = self.send_post_request(self.deployment_url, rg_data)
        if r.status_code != requests.codes.ok:
            msg = f'Failed to create a new deployment. Error: {response}'
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

        return response

    def edit(self, deployment_id, rg_data):
        """
        Edit a deployment with the given ID using the provided data.
        Args:
            deployment_id (str): The ID of the deployment to edit.
            rg_data (dict): The data to use for editing the deployment.
        Returns:
            dict: The response from the API.
        Raises:
            PowerFlexClientException: If the request fails.
        """
        request_url = f'{self.deployment_url}/{deployment_id}'
        r, response = self.send_put_request(request_url, rg_data)

        if r.status_code != requests.codes.ok:
            msg = f'Failed to edit the deployment. Error: {response}'
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

        return response

    def delete(self, deployment_id):
        """
        Deletes a deployment with the given ID.
        Args:
            deployment_id (str): The ID of the deployment to delete.
        Returns:
            str: The response from the delete request.
        Raises:
            exceptions.PowerFlexClientException: If the delete request fails.
        """
        request_url = f'{self.deployment_url}/{deployment_id}'
        response = self.send_delete_request(request_url)

        if response.status_code != requests.codes.no_content:
            msg = f'Failed to delete deployment. Error: {response}'
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

        return response
