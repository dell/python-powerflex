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

"""Module for testing storage pool client."""

# pylint: disable=invalid-name,too-many-public-methods

from unittest import mock

from PyPowerFlex import exceptions
from tests.common import PyPowerFlexTestCase


@PyPowerFlexTestCase.version('5.0')
class TestStoragePoolClient(PyPowerFlexTestCase):
    """
    Tests for the StoragePoolClient class.
    """

    # pylint: disable=R0801
    def setUp(self):
        """
        Set up the test environment.
        """
        super().setUp()
        self.client.initialize()
        self.fake_pd_id = '1'
        self.fake_sp_id = '1'
        self.fake_sp_name = "sp-1"

        sp = {
            'id': self.fake_sp_id,
            'name': self.fake_sp_name,
            'protectionDomainId': self.fake_pd_id,
            'deviceGroupId': "1",
            'wrcDeviceGroupId': "1",
            'genType': 'EC',
            'capacityAlertHighThreshold': 70,
            'capacityAlertCriticalThreshold': 90,
            'fragmentationEnabled': False,
            'overProvisioningFactor': 0,
            'physicalSizeGB': 10,
            'protectionScheme': 'TwoPlusTwo',
            'compressionMethod': 'None',
            'zeroPaddingEnabled': True,
        }

        self.MOCK_RESPONSES = {
            self.RESPONSE_MODE.Valid: {
                '/types/StoragePool/instances':
                    sp,
                f"/instances/StoragePool::{self.fake_sp_id}":
                    sp,
                f'/instances/ProtectionDomain::{self.fake_pd_id}/relationships/StoragePool':
                    [sp],
                f'/instances/StoragePool::{self.fake_sp_id}/action/removeStoragePool':
                    {},
                f'/instances/StoragePool::{self.fake_sp_id}/action/renameStoragePool':
                    {},
                f'/instances/StoragePool::{self.fake_sp_id}/action/setCapacityAlertThresholds':
                    {},
                f'/instances/StoragePool::{self.fake_sp_id}/action/setOverProvisioningFactor':
                    {},
                f'/instances/StoragePool::{self.fake_sp_id}/action/modifyStoragePoolSize':
                    {},
                f'/instances/StoragePool::{self.fake_sp_id}/action/modifyCompressionMethod':
                    {},
                f'/instances/StoragePool::{self.fake_sp_id}/action/setZeroPaddingPolicy':
                    {},
            },
            self.RESPONSE_MODE.Invalid: {
                '/types/StoragePool/instances':
                    {},
            }
        }

    def test_storage_pool_get_by_id(self):
        """
        Test the get_by_id of a storage pool.
        """
        self.client.storage_pool.get_by_id(self.fake_sp_id)

    def test_storage_pool_get_by_name(self):
        """
        Test the get_by_name of a storage pool.
        """
        self.client.storage_pool.get_by_name(
            self.fake_pd_id, self.fake_sp_name)

    def test_storage_pool_need_update(self):
        """
        Test the update of a storage pool.
        """
        sp_params = {
            'id': self.fake_sp_id,
            'name': "name",
            'capacityAlertHighThreshold': 80,
            'capacityAlertCriticalThreshold': 95,
            'fragmentationEnabled': True,
            'overProvisioningFactor': 1000,
            'physicalSizeGB': 2,
            'protectionScheme': 'TwoPlusEight',
            'compressionMethod': 'Normal',
            'zeroPaddingEnabled': False,
        }
        self.client.storage_pool.need_update(sp_params, None)

    def test_storage_pool_update(self):
        """
        Test the update of a storage pool.
        """
        sp_params = {
            'id': self.fake_sp_id,
            'name': "name",
            'capacityAlertHighThreshold': 70,
            'capacityAlertCriticalThreshold': 85,
            'fragmentationEnabled': True,
            'overProvisioningFactor': 100,
            'physicalSizeGB': 1,
            'compressionMethod': 'None',
            'zeroPaddingEnabled': True,
        }
        sp = {
            'id': self.fake_sp_id,
            'name': "new_name",
            'capacityAlertHighThreshold': 80,
            'capacityAlertCriticalThreshold': 95,
            'fragmentationEnabled': True,
            'overProvisioningFactor': 1000,
            'physicalSizeGB': 2,
            'protectionScheme': 'TwoPlusEight',
            'compressionMethod': 'Normal',
            'zeroPaddingEnabled': False,
        }
        self.client.storage_pool.update(sp_params, sp)

    def test_storage_pool_update_bad_status(self):
        """
        Test the update of a storage pool with a bad status.
        """
        sp_params = {
            'id': self.fake_sp_id,
            'name': self.fake_sp_name,
            'protectionDomainId': "pd_id",
            'deviceGroupId': "1",
            'protectionScheme': 'TwoPlusTwo',
            'wrcDeviceGroupId': "1",
            'genType': 'EC',
            'capacityAlertHighThreshold': 70,
            'capacityAlertCriticalThreshold': 90,
            'fragmentationEnabled': False,
            'overProvisioningFactor': 0,
            'physicalSizeGB': 10,
            'compressionMethod': 'None',
            'zeroPaddingEnabled': True,
        }
        sp = {
            'id': self.fake_sp_id,
            'name': self.fake_sp_name,
            'protectionDomainId': "new_pd_id",
            'deviceGroupId': "1",
            'protectionScheme': 'TwoPlusTwo',
            'wrcDeviceGroupId': "1",
            'genType': 'EC',
            'capacityAlertHighThreshold': 70,
            'capacityAlertCriticalThreshold': 90,
            'fragmentationEnabled': False,
            'overProvisioningFactor': 0,
            'physicalSizeGB': 10,
            'compressionMethod': 'None',
            'zeroPaddingEnabled': True,
        }
        self.assertRaises(exceptions.PowerFlexClientException,
                          self.client.storage_pool.check_update_params,
                          sp_params,
                          sp)

    def test_storage_pool_update_bad_status_1(self):
        """
        Test the update of a storage pool with a bad status.
        """
        sp_params = {
            'id': self.fake_sp_id,
            'name': self.fake_sp_name,
            'protectionDomainId': self.fake_pd_id,
            'deviceGroupId': "1",
            'protectionScheme': 'TwoPlusTwo',
            'wrcDeviceGroupId': "1",
            'genType': 'EC',
            'capacityAlertHighThreshold': 70,
            'capacityAlertCriticalThreshold': 90,
            'fragmentationEnabled': False,
            'overProvisioningFactor': 0,
            'physicalSizeGB': 10,
            'compressionMethod': 'None',
            'zeroPaddingEnabled': True,
        }
        sp = {
            'id': self.fake_sp_id,
            'name': self.fake_sp_name,
            'protectionDomainId': self.fake_pd_id,
            'deviceGroupId': "2",
            'protectionScheme': 'TwoPlusTwo',
            'wrcDeviceGroupId': "1",
            'genType': 'EC',
            'capacityAlertHighThreshold': 70,
            'capacityAlertCriticalThreshold': 90,
            'fragmentationEnabled': False,
            'overProvisioningFactor': 0,
            'physicalSizeGB': 10,
            'compressionMethod': 'None',
            'zeroPaddingEnabled': True,
        }
        self.assertRaises(exceptions.PowerFlexClientException,
                          self.client.storage_pool.check_update_params,
                          sp_params,
                          sp)

    def test_storage_pool_update_bad_status_2(self):
        """
        Test the update of a storage pool with a bad status.
        """
        sp_params = {
            'id': self.fake_sp_id,
            'name': self.fake_sp_name,
            'protectionDomainId': self.fake_pd_id,
            'deviceGroupId': "1",
            'protectionScheme': 'TwoPlusTwo',
            'wrcDeviceGroupId': "1",
            'genType': 'EC',
            'capacityAlertHighThreshold': 70,
            'capacityAlertCriticalThreshold': 90,
            'fragmentationEnabled': False,
            'overProvisioningFactor': 0,
            'physicalSizeGB': 10,
            'compressionMethod': 'None',
            'zeroPaddingEnabled': True,
        }
        sp = {
            'id': self.fake_sp_id,
            'name': self.fake_sp_name,
            'protectionDomainId': self.fake_pd_id,
            'deviceGroupId': "1",
            'protectionScheme': 'EightPlusTwo',
            'wrcDeviceGroupId': "1",
            'genType': 'EC',
            'capacityAlertHighThreshold': 70,
            'capacityAlertCriticalThreshold': 90,
            'fragmentationEnabled': False,
            'overProvisioningFactor': 0,
            'physicalSizeGB': 10,
            'compressionMethod': 'None',
            'zeroPaddingEnabled': True,
        }
        self.assertRaises(exceptions.PowerFlexClientException,
                          self.client.storage_pool.check_update_params,
                          sp_params,
                          sp)

    def test_storage_pool_create(self):
        """
        Test the creation of a storage pool.
        """
        sp = {
            'id': self.fake_sp_id,
            'name': self.fake_sp_name,
            'protectionDomainId': self.fake_pd_id,
            'deviceGroupId': "1",
            'wrcDeviceGroupId': "1",
            'genType': 'EC',
            'capacityAlertHighThreshold': 70,
            'capacityAlertCriticalThreshold': 90,
            'fragmentationEnabled': False,
            'overProvisioningFactor': 0,
            'physicalSizeGB': 10,
            'protectionScheme': 'TwoPlusTwo',
            'compressionMethod': 'None',
            'zeroPaddingEnabled': True,
        }
        self.client.storage_pool.create(sp)

    def test_storage_pool_create_bad_status(self):
        """
        Test the creation of a storage pool with a bad status.
        """
        sp = {
            'id': self.fake_sp_id,
            'name': self.fake_sp_name,
            'protectionDomainId': self.fake_pd_id,
            'deviceGroupId': "1",
            'wrcDeviceGroupId': "1",
            'genType': 'EC',
            'capacityAlertHighThreshold': 70,
            'capacityAlertCriticalThreshold': 90,
            'fragmentationEnabled': False,
            'overProvisioningFactor': 0,
            'physicalSizeGB': 10,
            'protectionScheme': 'TwoPlusTwo',
            'compressionMethod': 'None',
            'zeroPaddingEnabled': True,
        }
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexFailCreating,
                              self.client.storage_pool.create,
                              sp)

    def test_storage_pool_create_bad_status_1(self):
        """
        Test the creation of a storage pool with a bad status.
        """
        sp = {
            'deviceGroupId': "1",
            'wrcDeviceGroupId': "1",
            'genType': 'EC',
            'capacityAlertHighThreshold': 70,
            'capacityAlertCriticalThreshold': 90,
            'fragmentationEnabled': False,
            'overProvisioningFactor': 0,
            'physicalSizeGB': 10,
            'protectionScheme': 'TwoPlusTwo',
            'compressionMethod': 'None',
            'zeroPaddingEnabled': True,
        }
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexClientException,
                              self.client.storage_pool.check_create_params,
                              sp)

    def test_storage_pool_create_bad_status_2(self):
        """
        Test the creation of a storage pool with a bad status.
        """
        sp = {
            'name': self.fake_sp_name,
            'protection_domain_id': self.fake_sp_id,
            'deviceGroupId': "1",
            'wrcDeviceGroupId': "1",
            'genType': 'EC',
            'capacityAlertHighThreshold': 70,
            'capacityAlertCriticalThreshold': 90,
            'fragmentationEnabled': False,
            'overProvisioningFactor': 0,
            'protectionScheme': 'TwoPlusTwo',
            'compressionMethod': 'None',
            'zeroPaddingEnabled': True,
        }
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexClientException,
                              self.client.storage_pool.check_create_params,
                              sp)

    # pylint: disable=R0801
    def test_storage_pool_delete(self):
        """
        Test the deletion of a storage pool.
        """
        self.client.storage_pool.delete(self.fake_sp_id)

    def test_storage_pool_delete_bad_status(self):
        """
        Test the deletion of a storage pool with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexFailDeleting,
                              self.client.storage_pool.delete,
                              self.fake_sp_id)

    def test_storage_pool_set_capacity_alert_thresholds(self):
        """
        Test the set_capacity_alert_thresholds of a storage pool.
        """
        self.client.storage_pool.set_capacity_alert_thresholds(
            self.fake_sp_id, 1, 2)

    def test_storage_pool_set_capacity_alert_thresholds_bad_status(self):
        """
        Test the set_capacity_alert_thresholds of a storage pool with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexClientException,
                              self.client.storage_pool.set_capacity_alert_thresholds,
                              self.fake_sp_id, 1, 2)

    def test_storage_pool_set_over_provisioning_factor(self):
        """
        Test the set_over_provisioning_factor of a storage pool.
        """
        self.client.storage_pool.set_over_provisioning_factor(
            self.fake_sp_id, 0)

    def test_storage_pool_set_over_provisioning_factor_bad_status(self):
        """
        Test the set_over_provisioning_factor of a storage pool with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexClientException,
                              self.client.storage_pool.set_over_provisioning_factor,
                              self.fake_sp_id, 0)

    def test_storage_pool_resize(self):
        """
        Test the resize of a storage pool.
        """
        self.client.storage_pool.resize(self.fake_sp_id, 1)

    def test_storage_pool_resize_bad_status(self):
        """
        Test the resize of a storage pool with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexClientException,
                              self.client.storage_pool.resize,
                              self.fake_sp_id, 1)

    def test_storage_pool_set_compression_method(self):
        """
        Test the set_compression_method of a storage pool.
        """
        self.client.storage_pool.set_compression_method(
            self.fake_sp_id, "None")

    def test_storage_pool_set_compression_method_bad_status(self):
        """
        Test the set_compression_method of a storage pool with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexClientException,
                              self.client.storage_pool.set_compression_method,
                              self.fake_sp_id, "None")

    def test_storage_pool_set_zero_padding_policy(self):
        """
        Test the set_zero_padding_policy of a storage pool.
        """
        self.client.storage_pool.set_zero_padding_policy(
            self.fake_sp_id, False)

    def test_storage_pool_set_zero_padding_policy_bad_status(self):
        """
        Test the set_zero_padding_policy of a storage pool with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexClientException,
                              self.client.storage_pool.set_zero_padding_policy,
                              self.fake_sp_id, False)

    # pylint: disable=R0801
    def test_storage_pool_rename(self):
        """
        Test the rename method of a storage pool.
        """
        self.client.storage_pool.rename(self.fake_sp_id, name='new_name')

    def test_storage_pool_rename_bad_status(self):
        """
        Test the rename method of a storage pool with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexFailRenaming,
                              self.client.storage_pool.rename,
                              self.fake_sp_id,
                              name='new_name')

    # ------------------------------------------------------------------
    # Flexible data slices (FEAT-23070) — added by TDD Writer (Stage 07)
    # ------------------------------------------------------------------

    def _capture_create_payload(self, sp):
        """Call create() while capturing the payload sent to _create_entity."""
        captured = {}

        def fake_create_entity(params=None):
            captured.update(params or {})
            return {'id': self.fake_sp_id}

        with mock.patch.object(self.client.storage_pool, '_create_entity',
                               side_effect=fake_create_entity), \
                mock.patch.object(self.client.storage_pool, 'update',
                                  return_value=(False, {'id': self.fake_sp_id})):
            self.client.storage_pool.create(sp)
        return captured

    def test_storage_pool_create_with_num_data_slices(self):
        """U-001: explicit num_data_slices is sent verbatim in the create payload."""
        sp = {
            'name': self.fake_sp_name,
            'protectionDomainId': self.fake_pd_id,
            'deviceGroupId': '1',
            'numDataSlices': 4,
            'physicalSizeGB': 10,
            'compressionMethod': 'None',
        }
        captured = self._capture_create_payload(sp)
        self.assertEqual(captured.get('numDataSlices'), 4)
        self.assertEqual(captured.get('numProtectionSlices'), 2)

    def test_storage_pool_create_with_explicit_protection_slices(self):
        """U-004: explicit numProtectionSlices is honored."""
        sp = {
            'name': self.fake_sp_name,
            'protectionDomainId': self.fake_pd_id,
            'deviceGroupId': '1',
            'numDataSlices': 6,
            'numProtectionSlices': 3,
            'physicalSizeGB': 10,
        }
        captured = self._capture_create_payload(sp)
        self.assertEqual(captured.get('numDataSlices'), 6)
        self.assertEqual(captured.get('numProtectionSlices'), 3)

    def test_storage_pool_create_preset_twoplustwo(self):
        """U-002: backward-compat preset TwoPlusTwo -> 2/2."""
        sp = {
            'name': self.fake_sp_name,
            'protectionDomainId': self.fake_pd_id,
            'deviceGroupId': '1',
            'protectionScheme': 'TwoPlusTwo',
            'physicalSizeGB': 10,
        }
        captured = self._capture_create_payload(sp)
        self.assertEqual(captured.get('numDataSlices'), 2)
        self.assertEqual(captured.get('numProtectionSlices'), 2)

    def test_storage_pool_create_preset_eightplustwo(self):
        """U-003: backward-compat preset EightPlusTwo -> 8/2."""
        sp = {
            'name': self.fake_sp_name,
            'protectionDomainId': self.fake_pd_id,
            'deviceGroupId': '1',
            'protectionScheme': 'EightPlusTwo',
            'physicalSizeGB': 10,
        }
        captured = self._capture_create_payload(sp)
        self.assertEqual(captured.get('numDataSlices'), 8)
        self.assertEqual(captured.get('numProtectionSlices'), 2)

    def test_check_create_params_invalid_num_data_slices(self):
        """U-005: num_data_slices <= 0 raises InvalidInput."""
        sp = {
            'name': self.fake_sp_name,
            'protectionDomainId': self.fake_pd_id,
            'deviceGroupId': '1',
            'protectionScheme': 'TwoPlusTwo',
            'numDataSlices': 0,
            'useAllAvailableCapacity': True,
        }
        self.assertRaises(exceptions.InvalidInput,
                          self.client.storage_pool.check_create_params,
                          sp)

    def test_check_create_params_requires_slices_or_scheme(self):
        """U-006: neither num_data_slices nor protectionScheme raises InvalidInput."""
        sp = {
            'name': self.fake_sp_name,
            'protectionDomainId': self.fake_pd_id,
            'deviceGroupId': '1',
            'useAllAvailableCapacity': True,
        }
        self.assertRaises(exceptions.InvalidInput,
                          self.client.storage_pool.check_create_params,
                          sp)

    def test_check_create_params_num_data_slices_only(self):
        """U-007: num_data_slices without protectionScheme is valid (one-of)."""
        sp = {
            'name': self.fake_sp_name,
            'protectionDomainId': self.fake_pd_id,
            'deviceGroupId': '1',
            'numDataSlices': 4,
            'useAllAvailableCapacity': True,
        }
        # Should not raise once one-of validation is implemented.
        self.client.storage_pool.check_create_params(sp)
