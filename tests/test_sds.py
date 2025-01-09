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

"""Module for testing SDS client."""

# pylint: disable=invalid-name,too-many-public-methods

from PyPowerFlex import exceptions
from PyPowerFlex.objects import sds
import tests


class TestSdsClient(tests.PyPowerFlexTestCase):
    """
    Tests for the SdsClient class.
    """
    def setUp(self):
        """
        Set up the test environment.
        """
        super().setUp()
        self.client.initialize()
        self.fake_sds_id = '1'
        self.fake_sp_id = '1'
        self.fake_pd_id = '1'
        self.fake_sds_ips = [sds.SdsIp('1.2.3.4', sds.SdsIpRoles.all)]

        self.MOCK_RESPONSES = {
            self.RESPONSE_MODE.Valid: {
                '/types/Sds/instances':
                    {'id': self.fake_sds_id},
                f'/instances/Sds::{self.fake_sds_id}':
                    {'id': self.fake_sds_id},
                f'/instances/Sds::{self.fake_sds_id}/action/addSdsIp':
                    {},
                f'/instances/Sds::{self.fake_sds_id}/action/removeSds':
                    {},
                f'/instances/Sds::{self.fake_sds_id}/relationships/Device':
                    [],
                f'/instances/Sds::{self.fake_sds_id}/action/setSdsName':
                    {},
                f'/instances/Sds::{self.fake_sds_id}/action/removeSdsIp':
                    {},
                f'/instances/Sds::{self.fake_sds_id}/action/setSdsIpRole':
                    {},
                f'/instances/Sds::{self.fake_sds_id}/action/setSdsPort':
                    {},
                f'/instances/Sds::{self.fake_sds_id}/action/enableRfcache':
                    {},
                f'/instances/Sds::{self.fake_sds_id}/action/disableRfcache':
                    {},
                f'/instances/Sds::{self.fake_sds_id}/action/setSdsRmcacheEnabled':
                    {},
                f'/instances/Sds::{self.fake_sds_id}/action/setSdsRmcacheSize':
                    {},
                f'/instances/Sds::{self.fake_sds_id}/action/setSdsPerformanceParameters':
                    {},
                '/types/Sds'
                '/instances/action/querySelectedStatistics': {
                    self.fake_sds_id: {'rfcacheFdReadTimeGreater5Sec': 0}
                        },
            },
            self.RESPONSE_MODE.Invalid: {
                '/types/Sds/instances':
                    {},
            }
        }

    def test_sds_add_ip(self):
        """
        Test the add_ip method of the SdsClient.
        """
        self.client.sds.add_ip(self.fake_sds_id, self.fake_sds_ips[0])

    def test_sds_add_ip_bad_status(self):
        """
        Test the add_ip method of the SdsClient with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexClientException,
                              self.client.sds.add_ip,
                              self.fake_sds_id,
                              self.fake_sds_ips[0])

    def test_sds_create(self):
        """
        Test the create method of the SdsClient.
        """
        self.client.sds.create(protection_domain_id=self.fake_pd_id,
                               sds_ips=self.fake_sds_ips)

    def test_sds_create_bad_status(self):
        """
        Test the create method of the SdsClient with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexFailCreating,
                              self.client.sds.create,
                              protection_domain_id=self.fake_pd_id,
                              sds_ips=self.fake_sds_ips)

    def test_sds_create_no_id_in_response(self):
        """
        Test the create method of the SdsClient with no ID in the response.
        """
        with self.http_response_mode(self.RESPONSE_MODE.Invalid):
            self.assertRaises(KeyError,
                              self.client.sds.create,
                              protection_domain_id=self.fake_pd_id,
                              sds_ips=self.fake_sds_ips)

    def test_sds_delete(self):
        """
        Test the delete method of the SdsClient.
        """
        self.client.sds.delete(self.fake_sds_id)

    def test_sds_delete_bad_status(self):
        """
        Test the delete method of the SdsClient with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexFailDeleting,
                              self.client.sds.delete,
                              self.fake_sds_id)

    def test_sds_get_devices(self):
        """
        Test the get_devices method of the SdsClient.
        """
        self.client.sds.get_devices(self.fake_sds_id)

    def test_sds_get_devices_bad_status(self):
        """
        Test the get_devices method of the SdsClient with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexClientException,
                              self.client.sds.get_devices,
                              self.fake_sds_id)

    def test_sds_rename(self):
        """
        Test the rename method of the SdsClient.
        """
        self.client.sds.rename(self.fake_sds_id, name='new_name')

    def test_sds_rename_bad_status(self):
        """
        Test the rename method of the SdsClient with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexFailRenaming,
                              self.client.sds.rename,
                              self.fake_sds_id,
                              name='new_name')

    def test_sds_remove_ip(self):
        """
        Test the remove_ip method of the SdsClient.
        """
        self.client.sds.remove_ip(self.fake_sds_id, ip='1.2.3.4')

    def test_sds_remove_ip_bad_status(self):
        """
        Test the remove_ip method of the SdsClient with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexClientException,
                              self.client.sds.remove_ip,
                              self.fake_sds_id,
                              ip='1.2.3.4')

    def test_sds_set_ip_role(self):
        """
        Test the set_ip_role method.
        """
        self.client.sds.set_ip_role(self.fake_sds_id,
                                    ip='1.2.3.4',
                                    role=sds.SdsIpRoles.sdc_only,
                                    force=True)

    def test_sds_set_ip_role_bad_status(self):
        """
        Test the set_ip_role method with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexClientException,
                              self.client.sds.set_ip_role,
                              self.fake_sds_id,
                              ip='1.2.3.4',
                              role=sds.SdsIpRoles.sdc_only,
                              force=True)

    def test_sds_set_port(self):
        """
        Test the set_port method.
        """
        self.client.sds.set_port(self.fake_sds_id, sds_port=4443)

    def test_sds_set_port_bad_status(self):
        """
        Test the set_port method with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexClientException,
                              self.client.sds.set_port,
                              self.fake_sds_id,
                              sds_port=4443)

    def test_sds_set_rfcache_enabled(self):
        """
        Test the set_rfcache_enabled method.
        """
        self.client.sds.set_rfcache_enabled(self.fake_sds_id,
                                            rfcache_enabled=True)

    def test_sds_set_rfcache_enabled_bad_status(self):
        """
        Test the set_rfcache_enabled method with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexClientException,
                              self.client.sds.set_rfcache_enabled,
                              self.fake_sds_id,
                              rfcache_enabled=True)

    def test_sds_set_rmcache_enabled(self):
        """
        Test the set_rmcache_enabled method.
        """
        self.client.sds.set_rmcache_enabled(self.fake_sds_id,
                                            rmcache_enabled=True)

    def test_sds_set_rmcache_enabled_bad_status(self):
        """
        Test the set_rmcache_enabled method with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexClientException,
                              self.client.sds.set_rmcache_enabled,
                              self.fake_sds_id,
                              rmcache_enabled=True)

    def test_sds_set_rmcache_size(self):
        """
        Test the set_rmcache_size method.
        """
        self.client.sds.set_rmcache_size(self.fake_sds_id,
                                         rmcache_size=128)

    def test_sds_set_rmcache_size_bad_status(self):
        """
        Test the set_rmcache_size method with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexClientException,
                              self.client.sds.set_rmcache_size,
                              self.fake_sds_id,
                              rmcache_size=128)

    def test_sds_set_performance_parameters(self):
        """
        Test the set_performance_parameters method.
        """
        self.client.sds.set_performance_parameters(
            self.fake_sds_id,
            performance_profile=sds.PerformanceProfile.highperformance)

    def test_sds_set_performance_parameters_bad_status(self):
        """
        Test the set_performance_parameters method with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(
                exceptions.PowerFlexClientException,
                self.client.sds.set_performance_parameters,
                self.fake_sds_id,
                performance_profile=sds.PerformanceProfile.highperformance)

    def test_sds_query_selected_statistics(self):
        """
        Test the query_selected_statistics method.
        """
        ret = self.client.sds.query_selected_statistics(
            properties=["rfcacheFdReadTimeGreater5Sec"]
        )
        assert ret.get(self.fake_sds_id).get(
            "rfcacheFdReadTimeGreater5Sec") == 0

    def test_sds_query_selected_statistics_bad_status(self):
        """
        Test the query_selected_statistics method with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(
                exceptions.PowerFlexFailQuerying,
                self.client.sds.query_selected_statistics,
                properties=["rfcacheFdReadTimeGreater5Sec"],
            )
