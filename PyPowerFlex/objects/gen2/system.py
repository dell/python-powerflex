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

"""Module for doing system-related operations."""

# pylint: disable=no-member,too-many-arguments,too-many-positional-arguments,duplicate-code

import logging
import requests

from PyPowerFlex import exceptions
from PyPowerFlex.objects.common.system import System as SystemCommon

LOG = logging.getLogger(__name__)


class System(SystemCommon):
    """Client for system operations"""

    def create_snapshot(self,
                        system_id,
                        snapshot_defs,
                        retention_period=None):
        """Create a snapshot in Gen2."""
        action = 'createSnapshot'

        params = {
            'snapshotDefs': snapshot_defs,
            'retentionPeriodInMin': retention_period
        }

        r, response = self.send_post_request(self.base_action_url,
                                             action=action,
                                             entity=self.entity,
                                             entity_id=system_id,
                                             params=params)
        if r.status_code != requests.codes.ok:
            msg = (
                f"Failed to create snapshot on PowerFlex {self.entity} "
                f"with id {system_id}. Error: {response}"
            )
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

        return response

    def create_thin_clone(self,
                        system_id,
                        snapshot_defs):
        """Create a thin clone in Gen2."""
        action = 'createThinClone'

        params = {
            'snapshotDefs': snapshot_defs
        }

        r, response = self.send_post_request(self.base_action_url,
                                             action=action,
                                             entity=self.entity,
                                             entity_id=system_id,
                                             params=params)
        if r.status_code != requests.codes.ok:
            msg = (
                f"Failed to create thin clone on PowerFlex {self.entity} "
                f"with id {system_id}. Error: {response}"
            )
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

        return response
