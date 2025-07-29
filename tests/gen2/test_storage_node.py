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

"""Module for testing Storage Node client."""

# pylint: disable=invalid-name,too-many-public-methods

from PyPowerFlex import exceptions
from PyPowerFlex.objects.gen2.storage_node import StorageNode, StorageNodeIp, StorageNodeIpRoles
from tests.common import PyPowerFlexTestCase


@PyPowerFlexTestCase.version('5.0')
class TestStorageNodeClient(PyPowerFlexTestCase):
    """
    Tests for the StorageNodeClient class.
    """

    def setUp(self):
        """
        Set up the test environment.
        """
        super().setUp()
        self.client.initialize()
        self.fake_node_id = '1'
        self.fake_sp_id = '1'
        self.fake_pd_id = '1'
        self.fake_node_ips = [StorageNodeIp(
            '1.2.3.4', StorageNodeIpRoles.storage_and_app)]

        self.MOCK_RESPONSES = {
            self.RESPONSE_MODE.Valid: {
                '/types/Node/instances':
                    {'id': self.fake_node_id},
                f'/instances/Node::{self.fake_node_id}':
                    {'id': self.fake_node_id},
                f'/instances/Node::{self.fake_node_id}/action/addIp':
                    {},
                f'/instances/Node::{self.fake_node_id}/action/removeNode':
                    {},
                f'/instances/Node::{self.fake_node_id}/action/removeIp':
                    {},
                f'/instances/Node::{self.fake_node_id}/action/renameStorageNode':
                    {},
                f'/instances/Node::{self.fake_node_id}/action/modifyIpRole':
                    {},
            },
            self.RESPONSE_MODE.Invalid: {
                '/types/Node/instances':
                    {},
            }
        }

    def test_storage_node_add_ip(self):
        """
        Test the add_ip method of the storage_node client.
        """
        self.client.storage_node.add_ip(
            self.fake_node_id, self.fake_node_ips[0])

    def test_storage_node_add_ip_bad_status(self):
        """
        Test the add_ip method of the storage_node client with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexClientException,
                              self.client.storage_node.add_ip,
                              self.fake_node_id,
                              self.fake_node_ips[0])

    def test_storage_node_create(self):
        """
        Test the create method of the storage_node client.
        """
        self.client.storage_node.create(
            name='fake_node_name',
            node_ips=self.fake_node_ips,
            protection_domain_id=self.fake_pd_id
        )

    def test_storage_node_create_bad_status(self):
        """
        Test the create method of the storage_node client with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexFailCreating,
                              self.client.storage_node.create,
                              name='fake_node_name',
                              node_ips=self.fake_node_ips,
                              protection_domain_id=self.fake_pd_id
                              )

    def test_storage_node_create_no_id_in_response(self):
        """
        Test the create method of the storage_node client with no ID in the response.
        """
        with self.http_response_mode(self.RESPONSE_MODE.Invalid):
            self.assertRaises(KeyError,
                              self.client.storage_node.create,
                              name='fake_node_name',
                              node_ips=[],
                              protection_domain_id=self.fake_pd_id)

    def test_storage_node_delete(self):
        """
        Test the delete method of the storage_node client.
        """
        self.client.storage_node.delete(self.fake_node_id)

    def test_storage_node_delete_bad_status(self):
        """
        Test the delete method of the storage_node client with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexFailDeleting,
                              self.client.storage_node.delete,
                              self.fake_node_id)

    def test_storage_node_rename(self):
        """
        Test the rename method of the storage_node client.
        """
        self.client.storage_node.rename(self.fake_node_id, name='new_name')

    def test_storage_node_rename_bad_status(self):
        """
        Test the rename method of the storage_node client with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexFailRenaming,
                              self.client.storage_node.rename,
                              self.fake_node_id,
                              name='new_name')

    def test_storage_node_remove_ip(self):
        """
        Test the remove_ip method of the storage_node client.
        """
        self.client.storage_node.remove_ip(self.fake_node_id, ip='1.2.3.4')

    def test_storage_node_remove_ip_bad_status(self):
        """
        Test the remove_ip method of the storage_node client with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexClientException,
                              self.client.storage_node.remove_ip,
                              self.fake_node_id,
                              ip='1.2.3.4')

    def test_storage_node_set_ip_role(self):
        """
        Test the set_ip_role method.
        """
        self.client.storage_node.set_ip_role(self.fake_node_id,
                                             ip='1.2.3.4',
                                             role=StorageNodeIpRoles.storage)

    def test_storage_node_set_ip_role_bad_status(self):
        """
        Test the set_ip_role method with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(exceptions.PowerFlexClientException,
                              self.client.storage_node.set_ip_role,
                              self.fake_node_id,
                              ip='1.2.3.4',
                              role=StorageNodeIpRoles.storage_and_app)
