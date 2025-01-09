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

"""Module for testing host client."""

# pylint: disable=invalid-name

from PyPowerFlex import exceptions
import tests


class TestHostClient(tests.PyPowerFlexTestCase):
    """
    Tests for the HostClient class.
    """
    def setUp(self):
        """
        Set up the test environment.
        """
        super().setUp()
        self.client.initialize()
        self.fake_host_id="1"
        self.fake_nqn = "nqn::"

        self.MOCK_RESPONSES = {
            self.RESPONSE_MODE.Valid: {
                # create
                '/types/Host/instances': {'id': self.fake_host_id},
                f'/instances/Host::{self.fake_host_id}':
                    {'id': self.fake_host_id},
                f'/instances/Host::{self.fake_host_id}/action/modifyMaxNumPaths': {},
                f'/instances/Host::{self.fake_host_id}/action/modifyMaxNumSysPorts': {},
            }
        }

    def test_sdc_host_create(self):
        """
        Test the creation of a new host.
        """
        self.client.host.create(self.fake_nqn, max_num_paths='8', max_num_sys_ports='8')

    def test_sdc_host_create_bad_status(self):
        """
        Test the creation of a new host with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexFailCreating,
                              self.client.host.create, self.fake_nqn)
    def test_sdc_modify_max_num_paths(self):
        """
        Test the modification of the maximum number of paths.
        """
        self.client.host.modify_max_num_paths(self.fake_host_id, max_num_paths='8')

    def test_sdc_modify_max_num_paths_bad_status(self):
        """
        Test the modification of the maximum number of paths with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexFailEntityOperation,
                              self.client.host.modify_max_num_paths,
                              self.fake_host_id,
                              max_num_paths='8')

    def test_sdc_modify_max_num_sys_ports(self):
        """
        Test the modification of the maximum number of system ports.
        """
        self.client.host.modify_max_num_sys_ports(self.fake_host_id, max_num_sys_ports='8')

    def test_sdc_modify_max_num_sys_ports_bad_status(self):
        """
        Test the modification of the maximum number of system ports with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexFailEntityOperation,
                              self.client.host.modify_max_num_sys_ports,
                              self.fake_host_id,
                              max_num_sys_ports='8')
