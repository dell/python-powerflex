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

"""Module for interacting with accelaration pool APIs."""

# pylint: disable=too-few-public-methods,duplicate-code

import logging
from PyPowerFlex import base_client
from PyPowerFlex import exceptions


LOG = logging.getLogger(__name__)


class MediaType:
    """Acceleration pool media types."""

    ssd = 'SSD'
    nvdimm = 'NVDIMM'


class AccelerationPool(base_client.EntityRequest):
    """
    A class representing a PowerFlex acceleration pool.

    This class provides methods to create, delete, and query acceleration pools.
    """
    def create(self,
               media_type,
               protection_domain_id,
               name=None,
               is_rfcache=None):
        """Create PowerFlex acceleration pool.

        :param media_type: one of predefined attributes of MediaType
        :type media_type: str
        :type protection_domain_id: str
        :type name: str
        :type is_rfcache: bool
        :rtype: dict
        """

        if media_type == MediaType.ssd and not is_rfcache:
            msg = 'is_rfcache must be set for media_type SSD.'
            raise exceptions.InvalidInput(msg)
        params = {
            'mediaType': media_type,
            'protectionDomainId': protection_domain_id,
            'name': name,
            'isRfcache': is_rfcache
        }

        return self._create_entity(params)

    def delete(self, acceleration_pool_id):
        """Delete PowerFlex acceleration pool.

        :type acceleration_pool_id: str
        :rtype: None
        """

        return self._delete_entity(acceleration_pool_id)

    def query_selected_statistics(self, properties, ids=None):
        """Query PowerFlex acceleration pool statistics.

        :type properties: list
        :type ids: list of acceleration pool IDs or None for all acceleration
                   pools
        :rtype: dict
        """

        action = "querySelectedStatistics"

        params = {'properties': properties}

        if ids:
            params["ids"] = ids
        else:
            params["allIds"] = ""

        return self._query_selected_statistics(action, params)
