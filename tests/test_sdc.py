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

"""Module for testing SDC client."""

# pylint: disable=invalid-name

from PyPowerFlex import exceptions
import tests


class TestSdcClient(tests.PyPowerFlexTestCase):
    """
    Tests for the SdcClient class.
    """
    def setUp(self):
        """
        Set up the test case.
        """
        super().setUp()
        self.client.initialize()
        self.fake_sdc_id = '1'

        self.MOCK_RESPONSES = {
            self.RESPONSE_MODE.Valid: {
                '/types/Sdc/instances':
                    {'id': self.fake_sdc_id},
                f'/instances/Sdc::{self.fake_sdc_id}':
                    {'id': self.fake_sdc_id},
                f'/instances/Sdc::{self.fake_sdc_id}/action/removeSdc':
                    {},
                f'/instances/Sdc::{self.fake_sdc_id}/relationships/Volume':
                    [],
                f'/instances/Sdc::{self.fake_sdc_id}/action/setSdcName':
                    {},
                f'/instances/Sdc::{self.fake_sdc_id}/action/setSdcPerformanceParameters':
                    {},
                '/types/Sdc'
                '/instances/action/querySelectedStatistics': {
                    self.fake_sdc_id: {'numOfMappedVolumes': 1}
                },
            }
        }

    def test_sdc_delete(self):
        """
        Test the delete method of the SdcClient.
        """
        self.client.sdc.delete(self.fake_sdc_id)

    def test_sdc_delete_bad_status(self):
        """
        Test the delete method of the SdcClient with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexFailDeleting,
                              self.client.sdc.delete,
                              self.fake_sdc_id)

    def test_sdc_get_mapped_volumes(self):
        """
        Test the get_mapped_volumes method of the SdcClient.
        """
        self.client.sdc.get_mapped_volumes(self.fake_sdc_id)

    def test_sdc_get_mapped_volumes_bad_status(self):
        """
        Test the get_mapped_volumes method of the SdcClient with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexClientException,
                              self.client.sdc.get_mapped_volumes,
                              self.fake_sdc_id)

    def test_sdc_rename(self):
        """
        Test the rename method of the SdcClient.
        """
        self.client.sdc.rename(self.fake_sdc_id, name='new_name')

    def test_sdc_rename_bad_status(self):
        """
        Test the rename method of the SdcClient with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexFailRenaming,
                              self.client.sdc.rename,
                              self.fake_sdc_id,
                              name='new_name')

    def test_set_performance_profile(self):
        """
        Test the set_performance_profile method of the SdcClient.
        """
        self.client.sdc.set_performance_profile(self.fake_sdc_id, 'Compact')

    def test_set_performance_profile_bad_status(self):
        """
        Test the set_performance_profile method of the SdcClient with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexFailEntityOperation,
                              self.client.sdc.set_performance_profile,
                              self.fake_sdc_id,
                              'Compact')

    def test_sdc_query_selected_statistics(self):
        """
        Test the query_selected_statistics method of the SdcClient.
        """
        ret = self.client.sdc.query_selected_statistics(
            properties=["numOfMappedVolumes"]
        )
        assert ret.get(self.fake_sdc_id).get("numOfMappedVolumes") == 1

    def test_sdc_query_selected_statistics_bad_status(self):
        """
        Test the query_selected_statistics method of the SdcClient with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(
                exceptions.PowerFlexFailQuerying,
                self.client.sdc.query_selected_statistics,
                properties=["numOfMappedVolumes"],
            )
