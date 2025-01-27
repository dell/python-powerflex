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

"""Module for testing protection domain client."""

# pylint: disable=invalid-name,too-many-public-methods,duplicate-code

from PyPowerFlex import exceptions
from PyPowerFlex.objects import protection_domain
import tests


class TestProtectionDomainClient(tests.PyPowerFlexTestCase):
    """
    Test class for the ProtectionDomainClient.
    """
    def setUp(self):
        """
        Set up the test environment.
        """
        super().setUp()
        self.client.initialize()
        self.fake_pd_id = '1'

        self.MOCK_RESPONSES = {
            self.RESPONSE_MODE.Valid: {
                '/types/ProtectionDomain/instances':
                    {'id': self.fake_pd_id},
                f'/instances/ProtectionDomain::{self.fake_pd_id}':
                    {'id': self.fake_pd_id},
                f'/instances/ProtectionDomain::{self.fake_pd_id}/action/activateProtectionDomain':
                    {'id': self.fake_pd_id},
                f'/instances/ProtectionDomain::{self.fake_pd_id}/relationships/Sds':
                    [],
                f'/instances/ProtectionDomain::{self.fake_pd_id}/relationships/StoragePool':
                    [],
                f'/instances/ProtectionDomain::{self.fake_pd_id}/action/removeProtectionDomain':
                    {},
                f'/instances/ProtectionDomain::{self.fake_pd_id}/action/inactivateProtectionDomain':
                    {'id': self.fake_pd_id},
                f'/instances/ProtectionDomain::{self.fake_pd_id}/action/setProtectionDomainName':
                    {},
                f'/instances/ProtectionDomain::{self.fake_pd_id}/action/setSdsNetworkLimits':
                    {},
                f'/instances/ProtectionDomain::{self.fake_pd_id}/action/enableSdsRfcache':
                    {},
                f'/instances/ProtectionDomain::{self.fake_pd_id}/action/disableSdsRfcache':
                    {},
                f'/instances/ProtectionDomain::{self.fake_pd_id}/action/setRfcacheParameters':
                    {},
                '/types/ProtectionDomain'
                '/instances/action/querySelectedStatistics': {
                    self.fake_pd_id: {
                        'rplTransmitBwc': {
                            'numSeconds': 0,
                            'totalWeightInKb': 0,
                            'numOccured': 0
                        }
                    }
                },
            },
            self.RESPONSE_MODE.Invalid: {
                '/types/ProtectionDomain/instances':
                    {},
            }
        }

    def test_protection_domain_activate(self):
        """
        Test the activation of a protection domain.
        """
        self.client.protection_domain.activate(self.fake_pd_id)

    def test_protection_domain_activate_bad_status(self):
        """
        Test the activation of a protection domain with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexClientException,
                              self.client.protection_domain.activate,
                              self.fake_pd_id)

    def test_protection_domain_create(self):
        """
        Test the creation of a protection domain.
        """
        self.client.protection_domain.create(name='fake_name')

    def test_protection_domain_create_bad_status(self):
        """
        Test the creation of a protection domain with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexFailCreating,
                              self.client.protection_domain.create,
                              name='fake_name')

    def test_protection_domain_create_no_id_in_response(self):
        """
        Test the creation of a protection domain with no ID in the response.
        """
        with self.http_response_mode(self.RESPONSE_MODE.Invalid):
            self.assertRaises(KeyError,
                              self.client.protection_domain.create,
                              name='fake_name')

    def test_protection_domain_get_sdss(self):
        """
        Test the retrieval of SDS for a protection domain.
        """
        self.client.protection_domain.get_sdss(self.fake_pd_id)

    def test_protection_domain_get_sdss_bad_status(self):
        """
        Test the retrieval of SDS for a protection domain with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexClientException,
                              self.client.protection_domain.get_sdss,
                              self.fake_pd_id)

    def test_protection_domain_get_storage_pools(self):
        """
        Test the retrieval of storage pools for a protection domain.
        """
        self.client.protection_domain.get_storage_pools(self.fake_pd_id)

    def test_protection_domain_get_storage_pools_bad_status(self):
        """
        Test the retrieval of storage pools for a protection domain with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexClientException,
                              self.client.protection_domain.get_storage_pools,
                              self.fake_pd_id)

    def test_protection_domain_delete(self):
        """
        Test the deletion of a protection domain.
        """
        self.client.protection_domain.delete(self.fake_pd_id)

    def test_protection_domain_delete_bad_status(self):
        """
        Test the deletion of a protection domain with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexFailDeleting,
                              self.client.protection_domain.delete,
                              self.fake_pd_id)

    def test_protection_domain_inactivate(self):
        """
        Test the inactivation of a protection domain.
        """
        self.client.protection_domain.inactivate(self.fake_pd_id)

    def test_protection_domain_inactivate_bad_status(self):
        """
        Test the inactivation of a protection domain with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexClientException,
                              self.client.protection_domain.inactivate,
                              self.fake_pd_id)

    def test_protection_domain_rename(self):
        """
        Test the rename method of the ProtectionDomainClient.
        """
        self.client.protection_domain.rename(self.fake_pd_id, name='new_name')

    def test_protection_domain_rename_bad_status(self):
        """
        Test the rename method of the ProtectionDomainClient with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexFailRenaming,
                              self.client.protection_domain.rename,
                              self.fake_pd_id,
                              name='new_name')

    def test_protection_domain_network_limits(self):
        """
        Test the network_limits method of the ProtectionDomainClient.
        """
        self.client.protection_domain.network_limits(self.fake_pd_id,
                                                     rebuild_limit=10240,
                                                     rebalance_limit=10240,
                                                     vtree_migration_limit=
                                                     10240,
                                                     overall_limit=10240)

    def test_protection_domain_network_limits_bad_status(self):
        """
        Test the network_limits method of the ProtectionDomainClient with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexClientException,
                              self.client.protection_domain.network_limits,
                              self.fake_pd_id)

    def test_protection_domain_set_rfcache_enabled(self):
        """
        Test the set_rfcache_enabled method of the ProtectionDomainClient.
        """
        self.client.protection_domain.set_rfcache_enabled(self.fake_pd_id,
                                                          enable_rfcache=True)

    def test_protection_domain_set_rfcache_enabled_bad_status(self):
        """
        Test the set_rfcache_enabled method of the ProtectionDomainClient with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexClientException,
                              self.client.protection_domain.set_rfcache_enabled,
                              self.fake_pd_id)

    def test_protection_domain_rfcache_parameters(self):
        """
        Test the rfcache_parameters method of the ProtectionDomainClient.
        """
        self.client.protection_domain.rfcache_parameters(self.fake_pd_id,
                                                         page_size=16,
                                                         max_io_limit=128,
                                                         pass_through_mode=
                                                         protection_domain.
                                                         RFCacheOperationMode.
                                                         write)

    def test_protection_domain_rfcache_parameters_bad_status(self):
        """
        Test the rfcache_parameters method of the ProtectionDomainClient with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexClientException,
                              self.client.protection_domain.
                              rfcache_parameters, self.fake_pd_id)

    def test_protection_domain_query_selected_statistics(self):
        """
        Test the query_selected_statistics method of the ProtectionDomainClient.
        """
        ret = self.client.protection_domain.query_selected_statistics(
            properties=["rplTransmitBwc"]
        )
        assert ret.get(self.fake_pd_id).get("rplTransmitBwc") == {
            "numSeconds": 0,
            "totalWeightInKb": 0,
            "numOccured": 0,
        }

    def test_protection_domain_query_selected_statistics_bad_status(self):
        """
        Test the query_selected_statistics method of the ProtectionDomainClient with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(
                exceptions.PowerFlexFailQuerying,
                self.client.protection_domain.query_selected_statistics,
                properties=["rplTransmitBwc"],
            )
