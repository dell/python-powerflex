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

# pylint: disable=invalid-name,too-many-public-methods

from PyPowerFlex import exceptions
from PyPowerFlex.objects.gen2.protection_domain import ProtectionDomain
from tests.common import PyPowerFlexTestCase


@PyPowerFlexTestCase.version('5.0')
class TestProtectionDomainClient(PyPowerFlexTestCase):
    """
    Tests for the ProtectionDomainClient class.
    """

    def setUp(self):
        """
        Set up the test environment.
        """
        super().setUp()
        self.client.initialize()
        self.fake_pd_id = '1'
        self.fake_pd_name = "pd-1"
        pd = {
            'id': self.fake_pd_id,
            'name': self.fake_pd_name,
            'protectionDomainState': 'Active',
            'rebuildEnabled': False,
            'rebalanceEnabled': False,
            'overallConcurrentIoLimit': 0,
            'bandwidthLimitOverallIos': 0,
            'bandwidthLimitBgDevScanner': 0,
            'bandwidthLimitGarbageCollector': 0,
            'bandwidthLimitSinglyImpactedRebuild': 0,
            'bandwidthLimitDoublyImpactedRebuild': 0,
            'bandwidthLimitRebalance': 0,
            'bandwidthLimitOther': 0,
            'bandwidthLimitNodeNetwork': 0,
        }

        self.MOCK_RESPONSES = {
            self.RESPONSE_MODE.Valid: {
                '/types/ProtectionDomain/instances':
                    pd,
                f'/instances/ProtectionDomain::{self.fake_pd_id}':
                    pd,
                f'/instances/ProtectionDomain::{self.fake_pd_id}/action/removeProtectionDomain':
                    {},
                f'/instances/ProtectionDomain::{self.fake_pd_id}/action/activateProtectionDomain':
                    {'id': self.fake_pd_id},
                f'/instances/ProtectionDomain::{self.fake_pd_id}/action/inactivateProtectionDomain':
                    {'id': self.fake_pd_id},
                f'/instances/ProtectionDomain::{self.fake_pd_id}/action/setProtectionDomainName':
                    {},
                f'/instances/ProtectionDomain::{self.fake_pd_id}/action/setRebuildEnabled':
                    {},
                f'/instances/ProtectionDomain::{self.fake_pd_id}/action/setRebalanceEnabled':
                    {},
                f'/instances/ProtectionDomain::{self.fake_pd_id}/action/setSecondaryIoPolicy':
                    {},
                f'/instances/ProtectionDomain::{self.fake_pd_id}/relationships/StoragePool':
                    [],
            },
            self.RESPONSE_MODE.Invalid: {
                '/types/ProtectionDomain/instances':
                    {},
            }
        }

    def test_protection_domain_get_by_id(self):
        """
        Test the get_by_id of a protection domain.
        """
        self.client.protection_domain.get_by_id(self.fake_pd_id)

    def test_protection_domain_get_by_name(self):
        """
        Test the get_by_name of a protection domain.
        """
        self.client.protection_domain.get_by_name(self.fake_pd_name)

    def test_protection_domain_update(self):
        """
        Test the update of a protection domain.
        """
        pd = {
            'id': self.fake_pd_id,
            'name': "new_name",
            'protectionDomainState': 'Inactive',
            'rebuildEnabled': True,
            'rebalanceEnabled': True,
            'overallConcurrentIoLimit': 1,
            'bandwidthLimitOverallIos': 1,
            'bandwidthLimitBgDevScanner': 1,
            'bandwidthLimitGarbageCollector': 1,
            'bandwidthLimitSinglyImpactedRebuild': 1,
            'bandwidthLimitDoublyImpactedRebuild': 1,
            'bandwidthLimitRebalance': 1,
            'bandwidthLimitOther': 1,
            'bandwidthLimitNodeNetwork': 1,
        }
        self.client.protection_domain.update(pd)

    def test_protection_domain_create(self):
        """
        Test the creation of a protection domain.
        """
        self.client.protection_domain.create({"name": self.fake_pd_name})

    def test_protection_domain_create_bad_status(self):
        """
        Test the creation of a protection domain with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexFailCreating,
                              self.client.protection_domain.create,
                              {"name": self.fake_pd_name})

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

    def test_protection_domain_rebuild(self):
        """
        Test the rebuild of a protection domain.
        """
        self.client.protection_domain.set_rebuild_enabled(self.fake_pd_id, False)

    def test_protection_domain_rebuild_bad_status(self):
        """
        Test the rebuild of a protection domain with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexClientException,
                              self.client.protection_domain.set_rebuild_enabled,
                              self.fake_pd_id, False)
    
    def test_protection_domain_rebalance(self):
        """
        Test the rebalance of a protection domain.
        """
        self.client.protection_domain.set_rebalance_enabled(self.fake_pd_id, False)

    def test_protection_domain_rebalance_bad_status(self):
        """
        Test the rebalance of a protection domain with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexClientException,
                              self.client.protection_domain.set_rebalance_enabled,
                              self.fake_pd_id, False)
    
    def test_protection_domain_set_secondary_io_policy(self):
        """
        Test the set_secondary_io_policy of a protection domain.
        """
        self.client.protection_domain.set_secondary_io_policy(self.fake_pd_id, {
            'policy': 'favorApplication',
            'overallConcurrentIoLimit': 0,
            'bandwidthLimitOverallIos': 0,
            'bandwidthLimitBgDevScanner': 0,
            'bandwidthLimitGarbageCollector': 0,
            'bandwidthLimitSinglyImpactedRebuild': 0,
            'bandwidthLimitDoublyImpactedRebuild': 0,
            'bandwidthLimitRebalance': 0,
            'bandwidthLimitOther': 0,
            'bandwidthLimitNodeNetwork': 0,
        })

    def test_protection_domain_set_secondary_io_policy_bad_status(self):
        """
        Test the set_secondary_io_policy of a protection domain with a bad status.
        """
        policy = {
            'policy': 'favorApplication',
            'overallConcurrentIoLimit': 0,
            'bandwidthLimitOverallIos': 0,
            'bandwidthLimitBgDevScanner': 0,
            'bandwidthLimitGarbageCollector': 0,
            'bandwidthLimitSinglyImpactedRebuild': 0,
            'bandwidthLimitDoublyImpactedRebuild': 0,
            'bandwidthLimitRebalance': 0,
            'bandwidthLimitOther': 0,
            'bandwidthLimitNodeNetwork': 0,
        }
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexClientException,
                              self.client.protection_domain.set_secondary_io_policy,
                              self.fake_pd_id, policy)

    def test_protection_domain_rename(self):
        """
        Test the rename method of a protection domain.
        """
        self.client.protection_domain.rename(self.fake_pd_id, name='new_name')

    def test_protection_domain_rename_bad_status(self):
        """
        Test the rename method of a protection domain with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexFailRenaming,
                              self.client.protection_domain.rename,
                              self.fake_pd_id,
                              name='new_name')

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
