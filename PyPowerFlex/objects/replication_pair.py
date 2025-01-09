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

"""Module for interacting with replication pair APIs."""

# pylint: disable=redefined-builtin,no-member,too-many-arguments,too-many-positional-arguments,duplicate-code

import logging

import requests

from PyPowerFlex import base_client
from PyPowerFlex import exceptions


LOG = logging.getLogger(__name__)


class ReplicationPair(base_client.EntityRequest):
    """
    A class representing Replication Pair client.
    """
    def get_statistics(self, id):
        """Retrieve statistics for the specified ReplicationPair object.

        :type id: str
        :rtype: dict
        """

        return self.get_related(id,
                                'Statistics')

    def add(self,
            source_vol_id,
            dest_vol_id,
            rcg_id,
            copy_type,
            name=None):
        """Add replication pair to PowerFlex RCG.

        :param source_vol_id: str
        :param dest_vol_id: str
        :param rcg_id: str
        :param copy_type: str
        :type name: str
        :return: dict
        """

        params = {
            "sourceVolumeId": source_vol_id,
            "destinationVolumeId": dest_vol_id,
            "replicationConsistencyGroupId": rcg_id,
            "copyType": copy_type,
            "name": name
        }

        return self._create_entity(params)

    def remove(self, id):
        """Remove replication pair of PowerFlex RCG.

        :param id: str
        :return: None
        """
        return self._delete_entity(id)

    def pause(self, id):
        """Pause the progress of the specified ReplicationPair's initial copy.

        :param id: str
        :return: dict
        """
        return self._perform_entity_operation_based_on_action(
            id, "pausePairInitialCopy", add_entity=False)

    def resume(self, id):
        """Resume initial copy of the ReplicationPair.

        :param id: str
        :return: dict
        """
        return self._perform_entity_operation_based_on_action(
            id, "resumePairInitialCopy", add_entity=False)

    def get_all_statistics(self):
        """Retrieve statistics for all ReplicationPair objects.
        :return: dict
        """
        r, response = self.send_post_request(self.list_statistics_url,
                                             entity=self.entity,
                                             action="querySelectedStatistics")
        if r.status_code != requests.codes.ok:
            msg = (
                'Failed to list statistics for all ReplicationPair objects. '
                f'Error: {response}'
            )
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

        return response

    def query_selected_statistics(self, properties, ids=None):
        """Query PowerFlex replication pair statistics.

        :type properties: list
        :type ids: list of replication pair IDs or None for all replication
                   pairs
        :rtype: dict
        """

        action = "querySelectedStatistics"

        params = {'properties': properties}

        if ids:
            params["ids"] = ids
        else:
            params["allIds"] = ""

        return self._query_selected_statistics(action, params)
