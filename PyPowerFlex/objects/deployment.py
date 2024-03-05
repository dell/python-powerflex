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

import logging
import requests
from PyPowerFlex import base_client
from PyPowerFlex import exceptions
from PyPowerFlex import utils
LOG = logging.getLogger(__name__)


class Deployment(base_client.EntityRequest):
    def get(self, filters=None, full=None, include_devices=None, include_template=None,
            limit=None, offset=None, sort=None):
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
        params = dict(
            filter=filters,
            full=full,
            sort=sort,
            offset=offset,
            limit=limit,
            includeDevices=include_devices,
            includeTemplate=include_template
        )
        r, response = self.send_get_request(utils.build_uri_with_params(self.deployment_url, **params))
        if r.status_code != requests.codes.ok:
            msg = (f'Failed to retrieve deployments. Error: {response}')
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)
        return response

    def deploy(self, rg_data):
        r, response = self.send_post_request(self.deployment_url, rg_data)
        if r.status_code != requests.codes.ok:
            msg = (f'Failed to deploy resource group. Error: {response}')
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

        return response 

    def edit(self, deployment_id, rg_data):
        request_url = f'{self.deployment_url}/{deployment_id}'
        r, response = self.send_put_request(request_url, rg_data)
        
        if r.status_code != requests.codes.ok:
            msg = (f'Failed to edit resource group. Error: {response}')
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

        return response

    def delete(self, deployment_id):
        request_url = f'{self.deployment_url}/{deployment_id}'
        response = self.send_delete_request(request_url)

        if response.status_code != requests.codes.no_content:
            msg = (f'Failed to delete resource group. Error: {response}')
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

        return response
