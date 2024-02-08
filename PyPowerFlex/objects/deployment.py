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


LOG = logging.getLogger(__name__)


class Deployment(base_client.EntityRequest):
    def get(self, filter=None, full=None, include_devices=None, include_template=None,
            limit=None, offset=None, sort=None):
        """
        Retrieve all Deployments with filter, sort, pagination
        :param filter: (Optional) The filter to apply to the results.
        :param full: (Optional) Whether to return full details for each result.
        :param include_devices: (Optional) Whether to include devices in the response.
        :param include_template: (Optional) Whether to include service templates in the response.
        :param limit: (Optional) The maximum number of results to return.
        :param offset: (Optional) The number of results to skip.
        :param sort: (Optional) The field to sort the results by.
        :return: A dictionary containing the retrieved Deployments.
        """
        params = dict(
            filter=filter,
            full=full,
            sort=sort,
            offset=offset,
            limit=limit,
            include_devices=include_devices,
            include_template=include_template
        )
        r, response = self.send_get_request(self.deployment_url, **params)
        if r.status_code != requests.codes.ok:
            LOG.error(self.deployment_url)
            msg = (f'Failed to retrieve deployments. Error: {response}')
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

        return response
