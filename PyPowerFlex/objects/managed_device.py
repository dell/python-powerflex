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

"""Module for interacting with managed device APIs."""

# pylint: disable=arguments-renamed,no-member

import logging
import requests
from PyPowerFlex import base_client
from PyPowerFlex import exceptions
from PyPowerFlex import utils
LOG = logging.getLogger(__name__)


class ManagedDevice(base_client.EntityRequest):
    """
    A class representing Managed Device client.
    """
    def get(self, filters=None, limit=None, offset=None, sort=None):
        """
        Retrieve all devices from inventory with filter, sort, pagination
        :param filters: (Optional) The filters to apply to the results.
        :param limit: (Optional) Page limit.
        :param offset: (Optional) Pagination offset.
        :param sort: (Optional) The field to sort the results by.
        :return: A list of dictionary containing the retrieved devices from inventory.
        """
        params = {
            "filter": filters,
            "limit": limit,
            "offset": offset,
            "sort": sort
        }
        r, response = self.send_get_request(
            utils.build_uri_with_params(
                self.managed_device_url, **params))
        if r.status_code != requests.codes.ok:
            msg = f'Failed to retrieve managed devices. Error: {response}'
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)
        return response
