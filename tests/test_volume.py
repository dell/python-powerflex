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

"""Module for testing volume client."""

# pylint: disable=invalid-name,too-many-public-methods

from PyPowerFlex import exceptions
from PyPowerFlex.objects import volume
import tests


class TestVolumeClient(tests.PyPowerFlexTestCase):
    """
    Test class for the volume client.
    """

    def setUp(self):
        """
        Set up the test case.
        """
        super().setUp()
        self.client.initialize()
        self.fake_sp_id = '1'
        self.fake_volume_id = '1'

        self.MOCK_RESPONSES = {
            self.RESPONSE_MODE.Valid: {
                '/types/Volume/instances':
                    {'id': self.fake_volume_id},
                f'/instances/Volume::{self.fake_volume_id}':
                    {'id': self.fake_volume_id},
                f'/instances/Volume::{self.fake_volume_id}/action/addMappedSdc':
                    {'id': self.fake_volume_id},
                f'/instances/Volume::{self.fake_volume_id}/action/removeVolume':
                    {},
                f'/instances/Volume::{self.fake_volume_id}/action/setVolumeSize':
                    {},
                f'/instances/Volume::{self.fake_volume_id}/relationships/Statistics':
                    {},
                f'/instances/Volume::{self.fake_volume_id}/action/lockAutoSnapshot':
                    {},
                f'/instances/Volume::{self.fake_volume_id}/action/removeMappedSdc':
                    {},
                f'/instances/Volume::{self.fake_volume_id}/action/setVolumeName':
                    {},
                f'/instances/Volume::{self.fake_volume_id}/action/unlockAutoSnapshot':
                    {},
                '/types/Volume'
                '/instances/action/querySelectedStatistics': {
                    self.fake_volume_id: {
                        'userDataSdcReadLatency': {
                            'numSeconds': 0,
                            'totalWeightInKb': 0,
                            'numOccured': 0
                        }
                    }
                },
            },
            self.RESPONSE_MODE.Invalid: {
                '/types/Volume/instances':
                    {},
            }
        }

    def test_volume_add_mapped_sdc_id_and_guid_are_set(self):
        """
        Test if volume add mapped sdc raises an exception
        when both sdc_id and sdc_guid are set.
        """
        with self.assertRaises(exceptions.InvalidInput) as error:
            self.client.volume.add_mapped_sdc(self.fake_volume_id,
                                              sdc_id='1',
                                              sdc_guid='1')
        self.assertEqual('Either sdc_id or sdc_guid must be set.',
                         error.exception.message)

    def test_volume_add_mapped_sdc(self):
        """
        Test if volume add mapped sdc is successful.
        """
        self.client.volume.add_mapped_sdc(self.fake_volume_id,
                                          sdc_id='1')

    def test_volume_add_mapped_sdc_bad_status(self):
        """
        Test if volume add mapped sdc raises an exception when the HTTP status is bad.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexClientException,
                              self.client.volume.add_mapped_sdc,
                              self.fake_volume_id,
                              sdc_id='1')

    def test_volume_create(self):
        """
        Test if volume create is successful.
        """
        self.client.volume.create(size_in_gb=8,
                                  storage_pool_id=self.fake_sp_id,
                                  volume_type=volume.VolumeType.thin)

    def test_volume_create_bad_status(self):
        """
        Test if volume create raises an exception when the HTTP status is bad.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexFailCreating,
                              self.client.volume.create,
                              size_in_gb=8,
                              storage_pool_id=self.fake_sp_id,
                              volume_type=volume.VolumeType.thin)

    def test_volume_create_no_id_in_response(self):
        """
        Test if volume create raises an exception when the response does not contain an id.
        """
        with self.http_response_mode(self.RESPONSE_MODE.Invalid):
            self.assertRaises(KeyError,
                              self.client.volume.create,
                              size_in_gb=8,
                              storage_pool_id=self.fake_sp_id,
                              volume_type=volume.VolumeType.thin)

    def test_volume_get_statistics(self):
        """
        Test if volume get statistics is successful.
        """
        self.client.volume.get_statistics(self.fake_volume_id)

    def test_volume_get_statistics_bad_status(self):
        """
        Test if volume get statistics raises an exception when the HTTP status is bad.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexClientException,
                              self.client.volume.get_statistics,
                              self.fake_volume_id)

    def test_volume_delete(self):
        """
        Test if volume delete is successful.
        """
        self.client.volume.delete(self.fake_volume_id,
                                  remove_mode=volume.RemoveMode.only_me)

    def test_volume_delete_bad_status(self):
        """
        Test if volume delete raises an exception when the HTTP status is bad.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexFailDeleting,
                              self.client.volume.delete,
                              self.fake_volume_id,
                              remove_mode=volume.RemoveMode.only_me)

    def test_volume_extend(self):
        """
        Test if volume extend is successful.
        """
        self.client.volume.extend(self.fake_volume_id,
                                  size_in_gb=16)

    def test_volume_extend_bad_status(self):
        """
        Test if volume extend raises an exception when the HTTP status is bad.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexClientException,
                              self.client.volume.extend,
                              self.fake_volume_id,
                              size_in_gb=16)

    def test_volume_lock_auto_snapshot(self):
        """
        Test the lock_auto_snapshot method of the VolumeClient.
        """
        self.client.volume.lock_auto_snapshot(self.fake_volume_id)

    def test_volume_lock_auto_snapshot_bad_status(self):
        """
        Test the lock_auto_snapshot method of the VolumeClient with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexClientException,
                              self.client.volume.lock_auto_snapshot,
                              self.fake_volume_id)

    def test_volume_remove_mapped_sdc_id_guid_and_all_sdcs_are_set(self):
        """
        Test the remove_mapped_sdc method of the VolumeClient
        when sdc_id, sdc_guid, and all_sdcs are all set.
        """
        with self.assertRaises(exceptions.InvalidInput) as error:
            self.client.volume.remove_mapped_sdc(self.fake_volume_id,
                                                 sdc_id='1',
                                                 sdc_guid='1',
                                                 all_sdcs=True)
        self.assertEqual('Either sdc_id or sdc_guid or all_sdcs must be set.',
                         error.exception.message)

    def test_volume_remove_mapped_sdc(self):
        """
        Test the remove_mapped_sdc method of the VolumeClient.
        """
        self.client.volume.remove_mapped_sdc(self.fake_volume_id,
                                             sdc_id='1')

    def test_volume_remove_mapped_sdc_bad_status(self):
        """
        Test the remove_mapped_sdc method of the VolumeClient with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexClientException,
                              self.client.volume.remove_mapped_sdc,
                              self.fake_volume_id,
                              sdc_id='1')

    def test_volume_rename(self):
        """
        Test the rename method of the VolumeClient.
        """
        self.client.volume.rename(self.fake_volume_id,
                                  name='new_name')

    def test_volume_rename_bad_status(self):
        """
        Test the rename method of the VolumeClient with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexFailRenaming,
                              self.client.volume.rename,
                              self.fake_volume_id,
                              name='new_name')

    def test_volume_unlock_auto_snapshot(self):
        """
        Test the unlock_auto_snapshot method of the VolumeClient.
        """
        self.client.volume.unlock_auto_snapshot(self.fake_volume_id)

    def test_volume_unlock_auto_snapshot_bad_status(self):
        """
        Test the unlock_auto_snapshot method of the VolumeClient with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexClientException,
                              self.client.volume.unlock_auto_snapshot,
                              self.fake_volume_id)

    def test_volume_query_selected_statistics(self):
        """
        Test case for querying selected statistics of a volume.
        """
        ret = self.client.volume.query_selected_statistics(
            properties=["userDataSdcReadLatency"]
        )
        assert ret.get(self.fake_volume_id).get("userDataSdcReadLatency") == {
            "numSeconds": 0,
            "totalWeightInKb": 0,
            "numOccured": 0,
        }

    def test_volume_query_selected_statistics_bad_status(self):
        """
        Test case for querying selected statistics of a volume with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(
                exceptions.PowerFlexFailQuerying,
                self.client.volume.query_selected_statistics,
                properties=["userDataSdcReadLatency"],
            )
