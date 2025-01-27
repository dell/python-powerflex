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

"""Module for interacting with service template APIs."""

# pylint: disable=arguments-renamed,no-member,too-many-arguments,too-many-positional-arguments

import logging
import requests
from PyPowerFlex import base_client
from PyPowerFlex import exceptions
from PyPowerFlex import utils
LOG = logging.getLogger(__name__)


class ServiceTemplate(base_client.EntityRequest):
    """
    A class representing Service Template client.
    """
    def get(
            self,
            filters=None,
            full=None,
            limit=None,
            offset=None,
            sort=None,
            include_attachments=None):
        """
        Retrieve all Service Templates with filter, sort, pagination
        :param filters: (Optional) The filters to apply to the results.
        :param full: (Optional) Whether to return full details for each result.
        :param limit: (Optional) Page limit.
        :param offset: (Optional) Pagination offset.
        :param sort: (Optional) The field to sort the results by.
        :param include_attachments: (Optional) Whether to include attachments.
        :return: A list of dictionary containing the retrieved Service Templates.
        """
        params = {
            "filter": filters,
            "full": full,
            "limit": limit,
            "offset": offset,
            "sort": sort,
            "includeAttachments": include_attachments
        }
        r, response = self.send_get_request(
            utils.build_uri_with_params(
                self.service_template_url, **params))
        if r.status_code != requests.codes.ok:
            msg = f'Failed to retrieve service templates. Error: {response}'
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)
        return response

    def get_by_id(self, service_template_id, for_deployment=False):
        """
        Retrieve a Service Template by its ID.
        :param service_template_id: The ID of the Service Template to retrieve.
        :param for_deployment: (Optional) Whether to retrieve the Service Template for deployment.
        :return: A dictionary containing the retrieved Service Template.
        """
        url = f'{self.service_template_url}/{service_template_id}'
        if for_deployment:
            url += '?forDeployment=true'
        r, response = self.send_get_request(url)
        if r.status_code != requests.codes.ok:
            msg = (
                f'Failed to retrieve service template by id {service_template_id}. '
                f'Error: {response}'
            )
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)
        return response
