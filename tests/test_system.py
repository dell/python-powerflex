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

"""Module for testing system client."""

# pylint: disable=invalid-name,too-many-public-methods,duplicate-code

from PyPowerFlex import exceptions
from PyPowerFlex.objects import system
import tests


class TestSystemClient(tests.PyPowerFlexTestCase):
    """
    Test class for the SystemClient.
    """
    def setUp(self):
        """
        Set up the test environment.
        """
        super().setUp()
        self.client.initialize()
        self.fake_system_id = '1'
        self.fake_cg_id = '1'
        self.fake_snapshot_defs = [system.SnapshotDef('123', 'snap_1')]
        self.fake_mdm_id = '1'

        self.MOCK_RESPONSES = {
            self.RESPONSE_MODE.Valid: {
                f'/instances/System::{self.fake_system_id}'
                '/action/removeConsistencyGroupSnapshots':
                    {},
                f'/instances/System::{self.fake_system_id}'
                '/action/snapshotVolumes':
                    {},
                '/instances/System'
                '/action'
                '/addStandbyMdm':
                    {},
                '/instances/System'
                '/action'
                '/removeStandbyMdm':
                    {},
                '/instances/System'
                '/action'
                '/changeMdmOwnership':
                    {},
                '/instances/System'
                '/action'
                '/setMdmPerformanceParameters':
                    {},
                '/instances/System'
                '/action'
                '/renameMdm':
                    {},
                '/instances/System'
                '/action'
                '/modifyVirtualIpInterfaces':
                    {},
                '/instances/System'
                '/action'
                '/switchClusterMode':
                    {},
                '/instances/System'
                '/queryMdmCluster':
                    {},
                '/Configuration':
                    {},
                '/types/System'
                '/instances/action/querySelectedStatistics': {
                    'rplTransmitBwc': {'numSeconds': 0, 'totalWeightInKb': 0, 'numOccured': 0}
                },
            },
            self.RESPONSE_MODE.Invalid: {
                '/version': 'invalid_version_format'
            },
        }

    def test_system_api_version(self):
        """
        Test the API version.
        """
        self.client.system.api_version()
        self.assertEqual(4, self.get_mock.call_count)

    def test_system_api_version_bad_status(self):
        """
        Test the API version with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexFailQuerying,
                              self.client.system.api_version,
                              cached=False)

    def test_system_api_version_invalid_format(self):
        """
        Test the API version with an invalid format.
        """
        with self.http_response_mode(self.RESPONSE_MODE.Invalid):
            self.assertRaises(exceptions.PowerFlexClientException,
                              self.client.system.api_version,
                              cached=False)

    def test_system_api_version_cached(self):
        """
        Test the API version with caching.
        """
        self.client.system.api_version()
        self.client.system.api_version()
        self.client.system.api_version()
        self.assertEqual(4, self.get_mock.call_count)

    def test_system_remove_cg_snapshots(self):
        """
        Test removing consistency group snapshots.
        """
        self.client.system.remove_cg_snapshots(self.fake_system_id,
                                               self.fake_cg_id)

    def test_system_remove_cg_snapshots_bad_status(self):
        """
        Test removing consistency group snapshots with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexClientException,
                              self.client.system.remove_cg_snapshots,
                              self.fake_system_id,
                              self.fake_cg_id)

    def test_system_snapshot_volumes(self):
        """
        Test snapshotting volumes.
        """
        self.client.system.snapshot_volumes(self.fake_system_id,
                                            self.fake_snapshot_defs)

    def test_system_snapshot_volumes_bad_status(self):
        """
        Test snapshotting volumes with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexClientException,
                              self.client.system.snapshot_volumes,
                              self.fake_system_id,
                              self.fake_snapshot_defs)

    def test_add_standby_mdm(self):
        """
        Test the add_standby_mdm method.
        """
        self.client.system.add_standby_mdm(mdm_ips=["10.x.x.x"],
                                           role="Manager")

    def test_add_standby_mdm_bad_status(self):
        """
        Test the add_standby_mdm method with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexClientException,
                              self.client.system.add_standby_mdm,
                              mdm_ips=["10.x.x.x"], role="Manager")

    def test_remove_standby_mdm(self):
        """
        Test the remove_standby_mdm method.
        """
        self.client.system.remove_standby_mdm(self.fake_mdm_id)

    def test_remove_standby_mdm_bad_status(self):
        """
        Test the remove_standby_mdm method with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexClientException,
                              self.client.system.remove_standby_mdm,
                              self.fake_mdm_id)

    def test_get_mdm_cluster(self):
        """
        Test the get_mdm_cluster_details method.
        """
        self.client.system.get_mdm_cluster_details()

    def test_get_mdm_cluster_bad_status(self):
        """
        Test the get_mdm_cluster_details method with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexClientException,
                              self.client.system.get_mdm_cluster_details)

    def test_change_mdm_ownership(self):
        """
        Test the change_mdm_ownership method.
        """
        self.client.system.change_mdm_ownership(self.fake_mdm_id)

    def test_change_mdm_ownership_bad_status(self):
        """
        Test the change_mdm_ownership method with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexClientException,
                              self.client.system.change_mdm_ownership,
                              self.fake_mdm_id)

    def test_change_performance_profile(self):
        """
        Test the set_cluster_mdm_performance_profile method.
        """
        self.client.system.\
            set_cluster_mdm_performance_profile(performance_profile="Compact")

    def test_change_performance_profile_bad_status(self):
        """
        Test the set_cluster_mdm_performance_profile method with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexClientException,
                              self.client.system.
                              set_cluster_mdm_performance_profile,
                              performance_profile="Compact")

    def test_rename_mdm(self):
        """
        Test the rename_mdm method.
        """
        self.client.system.rename_mdm(self.fake_mdm_id, mdm_new_name="fake")

    def test_rename_mdm_bad_status(self):
        """
        Test the rename_mdm method with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexClientException,
                              self.client.system.rename_mdm,
                              self.fake_mdm_id, mdm_new_name="fake")

    def test_modify_virtual_ip_interface(self):
        """
        Test the modify_virtual_ip_interface method.
        """
        self.client.system.\
            modify_virtual_ip_interface(self.fake_mdm_id,
                                        virtual_ip_interfaces=["interface"])

    def test_modify_virtual_ip_interface_bad_status(self):
        """
        Test the modify_virtual_ip_interface method with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexClientException,
                              self.client.system.modify_virtual_ip_interface,
                              self.fake_mdm_id,
                              virtual_ip_interfaces=["interface"])

    def test_clear_virtual_ip_interface(self):
        """
        Test the modify_virtual_ip_interface method with no arguments.
        """
        self.client.system.modify_virtual_ip_interface(self.fake_mdm_id)

    def test_clear_virtual_ip_interface_bad_status(self):
        """
        Test the modify_virtual_ip_interface method with no arguments and a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexClientException,
                              self.client.system.modify_virtual_ip_interface,
                              self.fake_mdm_id)

    def test_switch_cluster_mode(self):
        """
        Test the switch_cluster_mode method.
        """
        self.client.system.switch_cluster_mode(self.fake_mdm_id)

    def test_switch_cluster_mode_bad_status(self):
        """
        Test the switch_cluster_mode method with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexClientException,
                              self.client.system.switch_cluster_mode,
                              self.fake_mdm_id)

    def test_get_gateway_configuration_details(self):
        """
        Test the get_gateway_configuration_details method.
        """
        self.client.system.get_gateway_configuration_details()

    def test_get_gateway_configuration_details_bad_status(self):
        """
        Test the get_gateway_configuration_details method with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexClientException,
                              self.client.system.get_gateway_configuration_details)

    def test_system_query_selected_statistics(self):
        """
        Test the query_selected_statistics method.
        """
        ret = self.client.system.query_selected_statistics(
            properties=["rplTransmitBwc"]
        )
        assert ret.get("rplTransmitBwc") == {
            "numSeconds": 0,
            "totalWeightInKb": 0,
            "numOccured": 0,
        }

    def test_system_query_selected_statistics_bad_status(self):
        """
        Test the query_selected_statistics method with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(
                exceptions.PowerFlexFailQuerying,
                self.client.system.query_selected_statistics,
                properties=["rplTransmitBwc"],
            )
