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

"""Module for testing SDT client."""

# pylint: disable=invalid-name,too-many-public-methods

from PyPowerFlex import exceptions
from PyPowerFlex.objects import sdt
import tests


class TestSdtClient(tests.PyPowerFlexTestCase):
    """
    Tests for the SdtClient class.
    """
    def setUp(self):
        """
        Set up the test environment.
        """
        super().setUp()
        self.client.initialize()
        self.fake_sdt_id = "1"
        self.fake_sdt_name = "1"
        self.fake_pd_id = "1"
        self.fake_sdt_ips = [sdt.SdtIp("1.2.3.4", sdt.SdtIpRoles.storage_and_host)]

        self.MOCK_RESPONSES = {
            self.RESPONSE_MODE.Valid: {
                "/types/Sdt/instances": {"id": self.fake_sdt_id},
                f"/instances/Sdt::{self.fake_sdt_id}": {"id": self.fake_sdt_id},
                f"/instances/Sdt::{self.fake_sdt_id}/action/addIp": {},
                f"/instances/Sdt::{self.fake_sdt_id}/action/removeIp": {},
                f"/instances/Sdt::{self.fake_sdt_id}/action/renameSdt": {},
                f"/instances/Sdt::{self.fake_sdt_id}/action/modifyIpRole": {},
                f"/instances/Sdt::{self.fake_sdt_id}/action/modifyStoragePort": {},
                f"/instances/Sdt::{self.fake_sdt_id}/action/modifyNvmePort": {},
                f"/instances/Sdt::{self.fake_sdt_id}/action/modifyDiscoveryPort": {},
                f"/instances/Sdt::{self.fake_sdt_id}/action/enterMaintenanceMode": {},
                f"/instances/Sdt::{self.fake_sdt_id}/action/exitMaintenanceMode": {},
                f"/instances/Sdt::{self.fake_sdt_id}/action/removeSdt": {},
            },
            self.RESPONSE_MODE.Invalid: {
                "/types/Sdt/instances": {},
            },
        }

    def test_sdt_create(self):
        """
        Test the create method of the SdtClient.
        """
        self.client.sdt.create(
            protection_domain_id=self.fake_pd_id,
            sdt_ips=self.fake_sdt_ips,
            sdt_name=self.fake_sdt_name,
        )

    def test_sdt_create_bad_status(self):
        """
        Test the create method of the SdtClient with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(
                exceptions.PowerFlexFailCreating,
                self.client.sdt.create,
                protection_domain_id=self.fake_pd_id,
                sdt_ips=self.fake_sdt_ips,
                sdt_name=self.fake_sdt_name,
            )

    def test_sdt_create_no_id_in_response(self):
        """
        Test the create method of the SdtClient with no id in the response.
        """
        with self.http_response_mode(self.RESPONSE_MODE.Invalid):
            self.assertRaises(
                KeyError,
                self.client.sdt.create,
                protection_domain_id=self.fake_pd_id,
                sdt_ips=self.fake_sdt_ips,
                sdt_name=self.fake_sdt_name,
            )

    def test_sdt_rename(self):
        """
        Test the rename method of the SdtClient.
        """
        self.client.sdt.rename(self.fake_sdt_id, name="new_name")

    def test_sdt_rename_bad_status(self):
        """
        Test the rename method of the SdtClient with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(
                exceptions.PowerFlexFailRenaming,
                self.client.sdt.rename,
                self.fake_sdt_id,
                name="new_name",
            )

    def test_sdt_add_ip(self):
        """
        Test the add_ip method of the SdtClient.
        """
        self.client.sdt.add_ip(
            self.fake_sdt_id, ip="1.2.3.4", role=sdt.SdtIpRoles.storage_and_host
        )

    def test_sdt_add_ip_bad_status(self):
        """
        Test the add_ip method of the SdtClient with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(
                exceptions.PowerFlexClientException,
                self.client.sdt.add_ip,
                self.fake_sdt_id,
                ip="1.2.3.4",
                role=sdt.SdtIpRoles.storage_and_host,
            )

    def test_sdt_remove_ip(self):
        """
        Test the remove_ip method of the SdtClient.
        """
        self.client.sdt.remove_ip(self.fake_sdt_id, ip="1.2.3.4")

    def test_sdt_remove_ip_bad_status(self):
        """
        Test the remove_ip method of the SdtClient with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(
                exceptions.PowerFlexClientException,
                self.client.sdt.remove_ip,
                self.fake_sdt_id,
                ip="1.2.3.4",
            )

    def test_sdt_set_ip_role(self):
        """
        Test the set_ip_role method of the SdtClient.
        """
        self.client.sdt.set_ip_role(
            self.fake_sdt_id, ip="1.2.3.4", role=sdt.SdtIpRoles.storage_and_host
        )

    def test_sdt_set_ip_role_bad_status(self):
        """
        Test the set_ip_role method of the SdtClient with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(
                exceptions.PowerFlexClientException,
                self.client.sdt.set_ip_role,
                self.fake_sdt_id,
                ip="1.2.3.4",
                role=sdt.SdtIpRoles.storage_and_host,
            )

    def test_sdt_set_storage_port(self):
        """
        Test the set_storage_port method of the SdtClient.
        """
        self.client.sdt.set_storage_port(self.fake_sdt_id, storage_port=12200)

    def test_sdt_set_storage_port_bad_status(self):
        """
        Test the set_storage_port method of the SdtClient with a bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(
                exceptions.PowerFlexClientException,
                self.client.sdt.set_storage_port,
                self.fake_sdt_id,
                storage_port=12200,
            )

    def test_sdt_set_nvme_port(self):
        """
        Test case for setting NVMe port of a Storage Device Target.
        """
        self.client.sdt.set_nvme_port(self.fake_sdt_id, nvme_port=4420)

    def test_sdt_set_nvme_port_bad_status(self):
        """
        Test case for setting NVMe port of a Storage Device Target with bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(
                exceptions.PowerFlexClientException,
                self.client.sdt.set_nvme_port,
                self.fake_sdt_id,
                nvme_port=4420,
            )

    def test_sdt_set_discovery_port(self):
        """
        Test case for setting discovery port of a Storage Device Target.
        """
        self.client.sdt.set_discovery_port(self.fake_sdt_id, discovery_port=8009)

    def test_sdt_set_discovery_port_bad_status(self):
        """
        Test case for setting discovery port of a Storage Device Target with bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(
                exceptions.PowerFlexClientException,
                self.client.sdt.set_discovery_port,
                self.fake_sdt_id,
                discovery_port=8009,
            )

    def test_sdt_enter_maintenance_mode(self):
        """
        Test case for entering maintenance mode of a Storage Device Target.
        """
        self.client.sdt.enter_maintenance_mode(self.fake_sdt_id)

    def test_sdt_enter_maintenance_mode_bad_status(self):
        """
        Test case for entering maintenance mode of a Storage Device Target with bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(
                exceptions.PowerFlexClientException,
                self.client.sdt.enter_maintenance_mode,
                self.fake_sdt_id,
            )

    def test_sdt_exit_maintenance_mode(self):
        """
        Test case for exiting maintenance mode of a Storage Device Target.
        """
        self.client.sdt.exit_maintenance_mode(self.fake_sdt_id)

    def test_sdt_exit_maintenance_mode_bad_status(self):
        """
        Test case for exiting maintenance mode of a Storage Device Target with bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(
                exceptions.PowerFlexClientException,
                self.client.sdt.exit_maintenance_mode,
                self.fake_sdt_id,
            )

    def test_sdt_delete(self):
        """
        Test case for deleting a Storage Device Target.
        """
        self.client.sdt.delete(self.fake_sdt_id)

    def test_sdt_delete_bad_status(self):
        """
        Test case for deleting a Storage Device Target with bad status.
        """
        with self.http_response_mode(self.RESPONSE_MODE.BadStatus):
            self.assertRaises(
                exceptions.PowerFlexFailDeleting,
                self.client.sdt.delete,
                self.fake_sdt_id,
            )
