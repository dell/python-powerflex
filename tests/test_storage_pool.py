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

from PyPowerFlex import exceptions
from PyPowerFlex.objects.storage_pool import CompressionMethod
from PyPowerFlex.objects.storage_pool import ExternalAccelerationType
from PyPowerFlex.objects.storage_pool import MediaType
import tests


class TestStoragePoolClient(tests.PyPowerFlexTestCase):
    def setUp(self):
        super(TestStoragePoolClient, self).setUp()
        self.client.initialize()
        self.fake_pd_id = '1'
        self.fake_sp_id = '1'

        self.MOCK_RESPONSES = {
            self.RESPONSE_MODE.Valid: {
                '/types/Sds/instances':
                    [],
                '/types/StoragePool/instances':
                    {'id': self.fake_sp_id},
                '/instances/StoragePool::{}'.format(self.fake_sp_id):
                    {'id': self.fake_sp_id},
                '/instances/StoragePool::{}'
                '/action/removeStoragePool'.format(self.fake_sp_id):
                    {},
                '/instances/StoragePool::{}'
                '/relationships/Device'.format(self.fake_sp_id):
                    [],
                '/instances/StoragePool::{}'
                '/relationships/SpSds'.format(self.fake_sp_id):
                    [],
                '/instances/StoragePool::{}'
                '/relationships/Volume'.format(self.fake_sp_id):
                    [],
                '/instances/StoragePool::{}'
                '/relationships/Statistics'.format(self.fake_sp_id):
                    {},
                '/instances/StoragePool::{}'
                '/action/setStoragePoolName'.format(self.fake_sp_id):
                    {},
                '/instances/StoragePool::{}'
                '/action/setChecksumEnabled'.format(self.fake_sp_id):
                    {},
                '/instances/StoragePool::{}'
                '/action/modifyCompressionMethod'.format(self.fake_sp_id):
                    {},
                '/instances/StoragePool::{}'
                '/action/setExternalAccelerationType'.format(self.fake_sp_id):
                    {},
                '/instances/StoragePool::{}'
                '/action/setMediaType'.format(self.fake_sp_id):
                    {},
                '/instances/StoragePool::{}'
                '/action/setRebalanceEnabled'.format(self.fake_sp_id):
                    {},
                '/instances/StoragePool::{}'
                '/action/setRebuildEnabled'.format(self.fake_sp_id):
                    {},
                '/instances/StoragePool::{}'
                '/action/setSparePercentage'.format(self.fake_sp_id):
                    {},
                '/instances/StoragePool::{}'
                '/action/enableRfcache'.format(self.fake_sp_id):
                    {},
                '/instances/StoragePool::{}'
                '/action/disableRfcache'.format(self.fake_sp_id):
                    {},
                '/instances/StoragePool::{}'
                '/action/setUseRmcache'.format(self.fake_sp_id):
                    {},
                '/instances/StoragePool::{}'
                '/action/setZeroPaddingPolicy'.format(self.fake_sp_id):
                    {},


                '/instances/StoragePool::{}'
                '/action/setReplicationJournalCapacity'.format(self.fake_sp_id):
                    {},
                '/instances/StoragePool::{}'
                '/action/setCapacityAlertThresholds'.format(self.fake_sp_id):
                    {},
                '/instances/StoragePool::{}'
                '/action/setProtectedMaintenanceModeIoPriorityPolicy'.format(self.fake_sp_id):
                    {},
                '/instances/StoragePool::{}'
                '/action/setVTreeMigrationIoPriorityPolicy'.format(self.fake_sp_id):
                    {},
                '/instances/StoragePool::{}'
                '/action/setRebalanceIoPriorityPolicy'.format(self.fake_sp_id):
                    {},
                '/instances/StoragePool::{}'
                '/action/setRmcacheWriteHandlingMode'.format(self.fake_sp_id):
                    {},
                '/instances/StoragePool::{}'
                '/action/setRebuildRebalanceParallelism'.format(self.fake_sp_id):
                    {},
                '/instances/StoragePool::{}'
                '/action/disablePersistentChecksum'.format(self.fake_sp_id):
                    {},
                '/instances/StoragePool::{}'
                '/action/enablePersistentChecksum'.format(self.fake_sp_id):
                    {},
                '/instances/StoragePool::{}'
                '/action/disableFragmentation'.format(self.fake_sp_id):
                    {},
                '/instances/StoragePool::{}'
                '/action/enableFragmentation'.format(self.fake_sp_id):
                    {},
                '/types/StoragePool'
                '/instances/action/querySelectedStatistics': {
                    self.fake_sp_id: {'rfcacheWritesSkippedCacheMiss': 0}
                },
            },
            self.RESPONSE_MODE.Invalid: {
                '/types/StoragePool/instances':
                    {},
            }
        }

    def test_storage_pool_create(self):
        self.client.storage_pool.create(media_type=MediaType.hdd,
                                        protection_domain_id=self.fake_pd_id)

    def test_storage_pool_create_bad_status(self):
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexFailCreating,
                              self.client.storage_pool.create,
                              media_type=MediaType.hdd,
                              protection_domain_id=self.fake_pd_id)

    def test_storage_pool_create_no_id_in_response(self):
        with self.http_response_mode(self.RESPONSE_MODE.Invalid):
            self.assertRaises(KeyError,
                              self.client.storage_pool.create,
                              media_type=MediaType.hdd,
                              protection_domain_id=self.fake_pd_id)

    def test_storage_pool_delete(self):
        self.client.storage_pool.delete(self.fake_sp_id)

    def test_storage_pool_delete_bad_status(self):
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexFailDeleting,
                              self.client.storage_pool.delete,
                              self.fake_sp_id)

    def test_storage_pool_get_devices(self):
        self.client.storage_pool.get_devices(self.fake_sp_id)

    def test_storage_pool_get_devices_bad_status(self):
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexClientException,
                              self.client.storage_pool.get_devices,
                              self.fake_sp_id)

    def test_storage_pool_get_sdss(self):
        self.client.storage_pool.get_sdss(self.fake_sp_id)

    def test_storage_pool_get_sdss_bad_status(self):
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexClientException,
                              self.client.storage_pool.get_sdss,
                              self.fake_sp_id)

    def test_storage_pool_get_volumes(self):
        self.client.storage_pool.get_volumes(self.fake_sp_id)

    def test_storage_pool_get_volumes_bad_status(self):
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexClientException,
                              self.client.storage_pool.get_volumes,
                              self.fake_sp_id)

    def test_storage_pool_get_statistics(self):
        self.client.storage_pool.get_statistics(self.fake_sp_id)

    def test_storage_pool_get_statistics_bad_status(self):
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexClientException,
                              self.client.storage_pool.get_statistics,
                              self.fake_sp_id)

    def test_storage_pool_rename(self):
        self.client.storage_pool.rename(self.fake_sp_id, name='new_name')

    def test_storage_pool_rename_bad_status(self):
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexFailRenaming,
                              self.client.storage_pool.rename,
                              self.fake_sp_id,
                              name='new_name')

    def test_storage_pool_set_checksum_enabled(self):
        self.client.storage_pool.set_checksum_enabled(self.fake_sp_id,
                                                      checksum_enabled=True)

    def test_storage_pool_set_checksum_enabled_bad_status(self):
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexClientException,
                              self.client.storage_pool.set_checksum_enabled,
                              self.fake_sp_id,
                              checksum_enabled=True)

    def test_storage_pool_set_compression_method(self):
        self.client.storage_pool.set_compression_method(
            self.fake_sp_id,
            compression_method=CompressionMethod.normal
        )

    def test_storage_pool_set_compression_method_bad_status(self):
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(
                exceptions.PowerFlexClientException,
                self.client.storage_pool.set_compression_method,
                self.fake_sp_id,
                compression_method=CompressionMethod.normal
            )

    def test_storage_pool_set_external_acceleration_type(self):
        self.client.storage_pool.set_external_acceleration_type(
            self.fake_sp_id,
            external_acceleration_type=ExternalAccelerationType.read
        )

    def test_storage_pool_set_external_acceleration_type_bad_status(self):
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(
                exceptions.PowerFlexClientException,
                self.client.storage_pool.set_external_acceleration_type,
                self.fake_sp_id,
                external_acceleration_type=ExternalAccelerationType.read
            )

    def test_storage_pool_set_external_acceleration_type_invalid_input(self):
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(
                exceptions.InvalidInput,
                self.client.storage_pool.set_external_acceleration_type,
                self.fake_sp_id,
                external_acceleration_type=ExternalAccelerationType.read,
                override_device_configuration=True,
                keep_device_ext_acceleration=True
            )

    def test_storage_pool_set_media_type(self):
        self.client.storage_pool.set_media_type(
            self.fake_sp_id,
            media_type=MediaType.hdd
        )

    def test_storage_pool_set_media_type_bad_status(self):
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(
                exceptions.PowerFlexClientException,
                self.client.storage_pool.set_media_type,
                self.fake_sp_id,
                media_type=MediaType.hdd
            )

    def test_storage_pool_set_rebalance_enabled(self):
        self.client.storage_pool.set_rebalance_enabled(
            self.fake_sp_id,
            rebalance_enabled=True
        )

    def test_storage_pool_set_rebalance_enabled_bad_status(self):
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(
                exceptions.PowerFlexClientException,
                self.client.storage_pool.set_rebalance_enabled,
                self.fake_sp_id,
                rebalance_enabled=True
            )

    def test_storage_pool_set_rebuild_enabled(self):
        self.client.storage_pool.set_rebuild_enabled(
            self.fake_sp_id,
            rebuild_enabled=True
        )

    def test_storage_pool_set_rebuild_enabled_bad_status(self):
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(
                exceptions.PowerFlexClientException,
                self.client.storage_pool.set_rebuild_enabled,
                self.fake_sp_id,
                rebuild_enabled=True
            )

    def test_storage_pool_set_spare_percentage(self):
        self.client.storage_pool.set_spare_percentage(
            self.fake_sp_id,
            spare_percentage=25
        )

    def test_storage_pool_set_spare_percentage_bad_status(self):
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(
                exceptions.PowerFlexClientException,
                self.client.storage_pool.set_spare_percentage,
                self.fake_sp_id,
                spare_percentage=25
            )

    def test_storage_pool_set_use_rfcache_enabled(self):
        self.client.storage_pool.set_use_rfcache(
            self.fake_sp_id,
            use_rfcache=True
        )

    def test_storage_pool_set_use_rfcache_disabled(self):
        self.client.storage_pool.set_use_rfcache(
            self.fake_sp_id,
            use_rfcache=False
        )

    def test_storage_pool_set_use_rfcache_bad_status(self):
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(
                exceptions.PowerFlexClientException,
                self.client.storage_pool.set_use_rfcache,
                self.fake_sp_id,
                use_rfcache=True
            )

    def test_storage_pool_set_use_rmcache(self):
        self.client.storage_pool.set_use_rmcache(
            self.fake_sp_id,
            use_rmcache=True
        )

    def test_storage_pool_set_use_rmcache_bad_status(self):
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(
                exceptions.PowerFlexClientException,
                self.client.storage_pool.set_use_rmcache,
                self.fake_sp_id,
                use_rmcache=True
            )

    def test_storage_pool_set_zero_padding_policy(self):
        self.client.storage_pool.set_zero_padding_policy(
            self.fake_sp_id,
            zero_padding_enabled=True
        )

    def test_storage_pool_set_zero_padding_policy_bad_status(self):
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(
                exceptions.PowerFlexClientException,
                self.client.storage_pool.set_zero_padding_policy,
                self.fake_sp_id,
                zero_padding_enabled=True
            )

    def test_storage_pool_set_rep_cap_max_ratio(self):
        self.client.storage_pool.set_rep_cap_max_ratio(
            self.fake_sp_id,
            rep_cap_max_ratio=60
        )

    def test_storage_pool_set_rep_cap_max_ratio_bad_status(self):
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(
                exceptions.PowerFlexClientException,
                self.client.storage_pool.set_rep_cap_max_ratio,
                self.fake_sp_id,
                rep_cap_max_ratio=60
            )

    def test_storage_pool_set_cap_alert_thresholds(self):
        self.client.storage_pool.set_cap_alert_thresholds(
            self.fake_sp_id,
            cap_alert_high_threshold=20,
            cap_alert_critical_threshold=60
        )

    def test_storage_pool_set_cap_alert_thresholds_bad_status(self):
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(
                exceptions.PowerFlexClientException,
                self.client.storage_pool.set_cap_alert_thresholds,
                self.fake_sp_id,
                cap_alert_high_threshold=20,
                cap_alert_critical_threshold=60
            )

    def test_storage_pool_set_protected_maintenance_mode_io_priority_policy(self):
        self.client.storage_pool.set_protected_maintenance_mode_io_priority_policy(
            self.fake_sp_id,
            policy='unlimited',
            concurrent_ios_per_device='4',
            bw_limit_per_device="2048"
        )

    def test_storage_pool_set_protected_maintenance_mode_io_priority_policy(self):
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(
                exceptions.PowerFlexClientException,
                self.client.storage_pool.set_protected_maintenance_mode_io_priority_policy,
                self.fake_sp_id,
                policy='unlimited',
                concurrent_ios_per_device='4',
                bw_limit_per_device="2048"
            )

    def test_storage_pool_set_vtree_migration_io_priority_policy(self):
        self.client.storage_pool.set_vtree_migration_io_priority_policy(
            self.fake_sp_id,
            policy='unlimited',
            concurrent_ios_per_device='4',
            bw_limit_per_device="2048"
        )

    def test_storage_pool_set_vtree_migration_io_priority_policy_bad_status(self):
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(
                exceptions.PowerFlexClientException,
                self.client.storage_pool.set_vtree_migration_io_priority_policy,
                self.fake_sp_id,
                policy='unlimited',
                concurrent_ios_per_device='4',
                bw_limit_per_device="2048"
        )

    def test_storage_pool_set_rmcache_write_handling_mode(self):
        self.client.storage_pool.set_rmcache_write_handling_mode(
            self.fake_sp_id,
            rmcache_write_handling_mode="Passthrough"
        )

    def test_storage_pool_set_rmcache_write_handling_mode_bad_status(self):
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(
                exceptions.PowerFlexClientException,
                self.client.storage_pool.set_rmcache_write_handling_mode,
                self.fake_sp_id,
                rmcache_write_handling_mode="Passthrough"
        )

    def test_storage_pool_set_rebuild_rebalance_parallelism_limit(self):
        self.client.storage_pool.set_rebuild_rebalance_parallelism_limit(
            self.fake_sp_id,
            no_of_parallel_rebuild_rebalance_jobs_per_device="3"
        )

    def test_storage_pool_set_rebuild_rebalance_parallelism_limit_bad_status(self):
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(
                exceptions.PowerFlexClientException,
                self.client.storage_pool.set_rebuild_rebalance_parallelism_limit,
                self.fake_sp_id,
                no_of_parallel_rebuild_rebalance_jobs_per_device="3"
        )

    def test_storage_pool_set_persistent_checksum(self):
        self.client.storage_pool.set_persistent_checksum(
            self.fake_sp_id,
            enable=True,
            validate=True,
            builder_limit="2048"
        )

    def test_storage_pool_set_persistent_checksum_bad_status(self):
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(
                exceptions.PowerFlexClientException,
                self.client.storage_pool.set_persistent_checksum,
                self.fake_sp_id,
                enable=True,
                validate=True,
                builder_limit="2048"
        )

    def test_storage_pool_set_fragmentation_enabled(self):
        self.client.storage_pool.set_fragmentation_enabled(
            self.fake_sp_id,
            enable_fragmentation=True
        )

    def test_storage_pool_set_fragmentation_enabled_bad_status(self):
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(
                exceptions.PowerFlexClientException,
                self.client.storage_pool.set_fragmentation_enabled,
                self.fake_sp_id,
                enable_fragmentation=True
        )

    def test_storage_pool_query_selected_statistics(self):
        ret = self.client.storage_pool.query_selected_statistics(
            properties=["rfcacheWritesSkippedCacheMiss"]
        )
        assert ret.get(self.fake_sp_id).get("rfcacheWritesSkippedCacheMiss") == 0

    def test_storage_pool_query_selected_statistics_bad_status(self):
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(
                exceptions.PowerFlexFailQuerying,
                self.client.storage_pool.query_selected_statistics,
                properties=["rfcacheWritesSkippedCacheMiss"],
            )
