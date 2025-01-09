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

"""Module for testing fault set client."""

# pylint: disable=invalid-name

from PyPowerFlex import exceptions
import tests


class TestFaultSetClient(tests.PyPowerFlexTestCase):
    """
    Test class for the PowerFlex FaultSetClient.
    """

    def setUp(self):
        """
        Set up the test environment.
        """
        super().setUp()
        self.client.initialize()
        self.fake_fault_set_id = '1'
        self.fake_pd_id = '1'

        self.MOCK_RESPONSES = {
            self.RESPONSE_MODE.Valid: {
                '/types/FaultSet/instances':
                    {'id': self.fake_fault_set_id},
                f'/instances/FaultSet::{self.fake_fault_set_id}':
                    {'id': self.fake_fault_set_id},
                f'/instances/FaultSet::{self.fake_fault_set_id}/action/clearFaultSet':
                    {},
                f'/instances/FaultSet::{self.fake_fault_set_id}/relationships/Sds':
                    [],
                f'/instances/FaultSet::{self.fake_fault_set_id}/action/removeFaultSet':
                    {},
                f'/instances/FaultSet::{self.fake_fault_set_id}/action/setFaultSetName':
                    {},
                '/types/FaultSet'
                '/instances/action/querySelectedStatistics': {
                    self.fake_fault_set_id: {'rfcacheFdReadTimeGreater5Sec': 0}
                },
            },
            self.RESPONSE_MODE.Invalid: {
                '/types/FaultSet/instances':
                    {},
            }
        }

    def test_fault_set_clear(self):
        """
        Test clearing a fault set.
        """
        self.client.fault_set.clear(self.fake_fault_set_id)

    def test_fault_set_clear_bad_status(self):
        """
        Test clearing a fault set with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexClientException,
                              self.client.fault_set.clear,
                              self.fake_fault_set_id)

    def test_fault_set_create(self):
        """
        Test creating a fault set.
        """
        self.client.fault_set.create(self.fake_pd_id, name='fake_name')

    def test_fault_set_create_bad_status(self):
        """
        Test creating a fault set with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexFailCreating,
                              self.client.fault_set.create,
                              self.fake_pd_id,
                              name='fake_name')

    def test_fault_set_create_no_id_in_response(self):
        """
        Test creating a fault set with no ID in the response.
        """
        with self.http_response_mode(self.RESPONSE_MODE.Invalid):
            self.assertRaises(KeyError,
                              self.client.fault_set.create,
                              self.fake_pd_id,
                              name='fake_name')

    def test_fault_set_get_sdss(self):
        """
        Test getting the SDS for a fault set.
        """
        self.client.fault_set.get_sdss(self.fake_fault_set_id)

    def test_fault_set_get_sdss_bad_status(self):
        """
        Test getting the SDS for a fault set with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexClientException,
                              self.client.fault_set.get_sdss,
                              self.fake_fault_set_id)

    def test_fault_set_delete(self):
        """
        Test deleting a fault set.
        """
        self.client.fault_set.delete(self.fake_fault_set_id)

    def test_fault_set_delete_bad_status(self):
        """
        Test deleting a fault set with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexFailDeleting,
                              self.client.fault_set.delete,
                              self.fake_fault_set_id)

    def test_fault_set_rename(self):
        """
        Test renaming a fault set.
        """
        self.client.fault_set.rename(self.fake_fault_set_id, name='new_name')

    def test_fault_set_rename_bad_status(self):
        """
        Test renaming a fault set with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexFailRenaming,
                              self.client.fault_set.rename,
                              self.fake_fault_set_id,
                              name='new_name')

    def test_fault_set_query_selected_statistics(self):
        """
        Test querying selected statistics for a fault set.
        """
        ret = self.client.fault_set.query_selected_statistics(
            properties=["rfcacheFdReadTimeGreater5Sec"]
        )
        assert ret.get(self.fake_fault_set_id).get("rfcacheFdReadTimeGreater5Sec") == 0

    def test_fault_set_query_selected_statistics_bad_status(self):
        """
        Test querying selected statistics for a fault set with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(
                exceptions.PowerFlexFailQuerying,
                self.client.fault_set.query_selected_statistics,
                properties=["rfcacheFdReadTimeGreater5Sec"],
            )
