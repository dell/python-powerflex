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

"""Module for interacting with firmware repository APIs."""

# pylint: disable=arguments-renamed,no-member,too-many-arguments,too-many-positional-arguments

import logging
import requests
from PyPowerFlex import base_client
from PyPowerFlex import exceptions
from PyPowerFlex import utils
LOG = logging.getLogger(__name__)


class FirmwareRepository(base_client.EntityRequest):
    """
    A class representing Firmware Repository client.
    """
    def get(self, filters=None, limit=None, offset=None, sort=None,
            related=False, bundles=False, components=False):
        """
        Retrieve all firmware repository with filter, sort, pagination
        :param filters: (Optional) The filters to apply to the results.
        :param limit: (Optional) Page limit.
        :param offset: (Optional) Pagination offset.
        :param sort: (Optional) The field to sort the results by.
        :param related: Whether to include related entities in the response.
        :param bundles: Whether to include bundles in the response.
        :param components: Whether to include components in the response.
        :return: A list of dictionary containing the retrieved firmware repository.
        """
        params = {
            'filter': filters,
            'sort': sort,
            'offset': offset,
            'limit': limit,
            'related': related,
            'bundles': bundles,
            'components': components
        }
        r, response = self.send_get_request(
            utils.build_uri_with_params(
                self.firmware_repository_url, **params))
        if r.status_code != requests.codes.ok:
            msg = (
                f'Failed to retrieve firmware repository. Error: {response}')
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)
        return response
