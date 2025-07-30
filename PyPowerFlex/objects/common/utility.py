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

"""Utility module for PowerFlex."""

# pylint: disable=no-member,useless-parent-delegation
import logging

import requests

from PyPowerFlex import base_client
from PyPowerFlex import exceptions

from PyPowerFlex.constants import (
    StoragePoolConstants,
    VolumeConstants,
    VolumeConstantsGen2,
    SnapshotPolicyConstants,
    StorageNodeConstants
)


LOG = logging.getLogger(__name__)


class PowerFlexUtility(base_client.EntityRequest):
    "Utility class for PowerFlex"

    def __init__(self, token, configuration):
        super().__init__(token, configuration)

    def get_statistics_for_all_storagepools(self, ids=None, properties=None):
        """list storagepool statistics for PowerFlex.

        :param ids: list
        :param properties: list
        :return: dict
        """

        action = 'querySelectedStatistics'
        version = self.get_api_version()
        default_properties = StoragePoolConstants.DEFAULT_STATISTICS_PROPERTIES
        if version != '3.5':
            default_properties = default_properties + \
                StoragePoolConstants.DEFAULT_STATISTICS_PROPERTIES_ABOVE_3_5
        params = {
            'properties': default_properties if properties is None else properties}
        if ids is None:
            params['allIds'] = ""
        else:
            params['ids'] = ids

        r, response = self.send_post_request(self.list_statistics_url,
                                             entity='StoragePool',
                                             action=action,
                                             params=params)
        if r.status_code != requests.codes.ok:
            msg = (
                f"Failed to list storage pool statistics for PowerFlex. "
                f"Error: {response}"
            )
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

        return response

    def get_statistics_for_all_volumes(self, ids=None, properties=None):
        """list volume statistics for PowerFlex.

        :param ids: list
        :param properties: list
        :return: dict
        """

        action = 'querySelectedStatistics'

        params = {
            'properties': (
                VolumeConstants.DEFAULT_STATISTICS_PROPERTIES
                if properties is None
                else properties
            )
        }
        if ids is None:
            params['allIds'] = ""
        else:
            params['ids'] = ids

        r, response = self.send_post_request(self.list_statistics_url,
                                             entity='Volume',
                                             action=action,
                                             params=params)
        if r.status_code != requests.codes.ok:
            msg = (
                'Failed to list volume statistics for PowerFlex. '
                f'Error: {response}'
            )
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

        return response

    def query_metrics_for_all_volumes_gen2(self, ids=None, metrics=None):
        """list volume statistics for PowerFlex 5.0+.

        :param ids: list
        :param metrics: list
        :return: dict
        """
        metrics = metrics or VolumeConstantsGen2.DEFAULT_STATISTICS_METRICS
        return self.query_metrics('volume', ids, metrics)

    def get_statistics_for_all_snapshot_policies(
            self, ids=None, properties=None):
        """list snapshot policy statistics for PowerFlex.

        :param ids: list
        :param properties: list
        :return: dict
        """

        action = 'querySelectedStatistics'

        params = {}
        if properties is None:
            params['properties'] = SnapshotPolicyConstants.DEFAULT_STATISTICS_PROPERTIES
        else:
            params['properties'] = properties
        if ids is None:
            params['allIds'] = ""
        else:
            params['ids'] = ids

        r, response = self.send_post_request(self.list_statistics_url,
                                             entity='SnapshotPolicy',
                                             action=action,
                                             params=params)
        if r.status_code != requests.codes.ok:
            msg = (
                f"Failed to list snapshot policy statistics for PowerFlex. "
                f"Error: {response}"
            )
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

        return response

    def query_metrics_for_all_storage_nodes(self, ids=None, metrics=None):
        """list storage node statistics for PowerFlex 5.0+.

        :param ids: list
        :param metrics: list
        :return: dict
        """
        metrics = metrics or StorageNodeConstants.DEFAULT_STATISTICS_METRICS
        return self.query_metrics('storage_node', ids, metrics)
