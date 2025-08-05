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

"""Module for testing volume client in Gen2."""

# pylint: disable=invalid-name,too-many-public-methods,duplicate-code

from PyPowerFlex import exceptions
from PyPowerFlex.objects.gen2 import volume
from tests.common import PyPowerFlexTestCase

@PyPowerFlexTestCase.version('5.0')
class TestVolumeClient(PyPowerFlexTestCase):
    """
    Test class for the volume client in Gen2.
    """

    def setUp(self):
        """
        Set up the test case.
        """
        super().setUp()
        self.client.initialize()
        self.fake_sp_id = '1'
        self.fake_volume_id = '1'
        self.fake_snapshot_id = '1'

        self.MOCK_RESPONSES = {
            self.RESPONSE_MODE.Valid: {
                '/types/Volume/instances':
                    {'id': self.fake_volume_id},
                f'/instances/Volume::{self.fake_volume_id}':
                    {'id': self.fake_volume_id},
                f'/instances/Volume::{self.fake_volume_id}/action/removeVolume':
                    {},
                f'/instances/Volume::{self.fake_volume_id}/action/setVolumeSize':
                    {},
                f'/instances/Volume::{self.fake_volume_id}/action/addMappedHost':
                    {},
                f'/instances/Volume::{self.fake_volume_id}/action/removeMappedHost':
                    {},
                f'/instances/Volume::{self.fake_volume_id}/action/setMappedSdcLimits':
                    {},
                f'/instances/Volume::{self.fake_volume_id}/action/setVolumeMappingAccessMode':
                    {},
                f'/instances/Volume::{self.fake_volume_id}/action/setVolumeName':
                    {},
                f'/instances/Volume::{self.fake_volume_id}/action/refresh':
                    {},
                f'/instances/Volume::{self.fake_volume_id}/action/restore':
                    {},
                f'/instances/Volume::{self.fake_volume_id}/action/setSnapshotSecurity':
                    {},
                '/dtapi/rest/v1/metrics/query':
                    {},
            },
            self.RESPONSE_MODE.Invalid: {
                '/types/Volume/instances':
                    {},
            }
        }

    def test_volume_add_mapped_sdc(self):
        """
        Test if volume add mapped sdc is successful.
        """
        self.client.volume.add_mapped_host(self.fake_volume_id,
                                          host_id='1')

    def test_volume_add_mapped_sdc_bad_status(self):
        """
        Test if volume add mapped sdc raises an exception when the HTTP status is bad.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexClientException,
                              self.client.volume.add_mapped_host,
                              self.fake_volume_id,
                              host_id='1')

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

    def test_volume_remove_mapped_sdc(self):
        """
        Test the remove_mapped_sdc method.
        """
        self.client.volume.remove_mapped_host(self.fake_volume_id,
                                             host_id='1')

    def test_volume_remove_mapped_sdc_bad_status(self):
        """
        Test the remove_mapped_sdc method with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexClientException,
                              self.client.volume.remove_mapped_host,
                              self.fake_volume_id,
                              host_id='1')

    def test_volume_rename(self):
        """
        Test the rename method.
        """
        self.client.volume.rename(self.fake_volume_id,
                                  name='new_name')

    def test_volume_rename_bad_status(self):
        """
        Test the rename method with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexFailRenaming,
                              self.client.volume.rename,
                              self.fake_volume_id,
                              name='new_name')

    def test_volume_set_mapped_sdc_limits(self):
        """
        Test the set_mapped_sdc_limits method.
        """
        self.client.volume.set_mapped_sdc_limits(self.fake_volume_id,
                                                 sdc_id='1',
                                                 bandwidth_limit='1')

    def test_volume_set_mapped_sdc_limits_bad_status(self):
        """
        Test the set_mapped_sdc_limits method with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexClientException,
                              self.client.volume.set_mapped_sdc_limits,
                              self.fake_volume_id,
                              sdc_id='1',
                              bandwidth_limit='1')

    def test_volume_set_access_mode_for_sdc(self):
        """
        Test the set_access_mode_for_sdc method.
        """
        self.client.volume.set_access_mode_for_sdc(self.fake_volume_id,
                                                 sdc_id='1',
                                                 access_mode='ReadWrite')

    def test_volume_set_access_mode_for_sdc_bad_status(self):
        """
        Test the set_access_mode_for_sdc method with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexClientException,
                              self.client.volume.set_access_mode_for_sdc,
                              self.fake_volume_id,
                              sdc_id='1',
                              access_mode='ReadWrite')

    def test_set_retention_period(self):
        """
        Test the set_retention_period method.
        """
        self.client.volume.set_retention_period(self.fake_snapshot_id,
                                                retention_period='1')

    def test_set_retention_period_bad_status(self):
        """
        Test the set_retention_period method with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexClientException,
                              self.client.volume.set_retention_period,
                              self.fake_snapshot_id,
                              retention_period='1')

    def test_volume_refresh(self):
        """
        Test the refresh method.
        """
        self.client.volume.refresh(dest_vol_id=self.fake_volume_id,
                                  src_vol_id='1')

    def test_volume_refresh_bad_status(self):
        """
        Test the refresh method with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexClientException,
                              self.client.volume.refresh,
                              dest_vol_id=self.fake_volume_id,
                              src_vol_id='1')

    def test_volume_restore(self):
        """
        Test the restore method.
        """
        self.client.volume.restore(dest_vol_id=self.fake_volume_id,
                                  src_vol_id='1')

    def test_volume_restore_bad_status(self):
        """
        Test the restore method with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexClientException,
                              self.client.volume.restore,
                              dest_vol_id=self.fake_volume_id,
                              src_vol_id='1')
