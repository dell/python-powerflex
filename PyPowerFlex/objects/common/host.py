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

"""Module for interacting with host APIs."""

import logging
from PyPowerFlex import base_client


LOG = logging.getLogger(__name__)

class Host(base_client.EntityRequest):
    """
    A class representing Host client.
    """
    def create(self,
               nqn,
               name=None,
               max_num_paths=None,
               max_num_sys_ports=None):
        """Create a new NVMe host.

        :param nqn: NQN of the NVMe host
        :type nqn: str
        :param name: Name of the NVMe Host
        :type name: str
        :param maxNumPaths: Maximum Number of Paths Per Volume.
        :type maxNumPaths: str
        :param maxNumSysPorts: Maximum Number of Ports Per Protection Domain
        :type maxNumSysPorts: str
        :return: Created host
        :rtype: dict
        """

        params = {
            "nqn": nqn,
            "name": name,
            "maxNumPaths": max_num_paths,
            "maxNumSysPorts": max_num_sys_ports
        }

        return self._create_entity(params)

    def modify_max_num_paths(self, host_id, max_num_paths):
        """Modify Maximum Number of Paths Per Volume.

        :param host_id: ID of the SDC
        :type host_id: str
        :param max_num_paths: Maximum Number of Paths Per Volume.
        :type max_num_paths: str
        :return: result
        :rtype: dict
        """

        action = 'modifyMaxNumPaths'

        params = {"newMaxNumPaths": max_num_paths}

        return self._perform_entity_operation_based_on_action(
            action=action, entity_id=host_id, params=params, add_entity=False)

    def modify_max_num_sys_ports(self, host_id, max_num_sys_ports):
        """Modify Maximum Number of Ports Per Protection Domain.

        :param host_id: ID of the SDC
        :type host_id: str
        :param max_num_sys_ports: Maximum Number of Ports Per Protection Domain.
        :type max_num_sys_ports: str
        :return: result
        :rtype: dict
        """

        action = 'modifyMaxNumSysPorts'

        params = {"newMaxNumSysPorts": max_num_sys_ports}

        return self._perform_entity_operation_based_on_action(
            action=action, entity_id=host_id, params=params, add_entity=False)
