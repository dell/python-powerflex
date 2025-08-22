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

"""Module for interacting with storage pool APIs."""

# pylint: disable=too-few-public-methods,too-many-public-methods,no-member,too-many-arguments,too-many-positional-arguments,too-many-locals,cyclic-import,duplicate-code

import logging
import requests

from PyPowerFlex import base_client, exceptions
from PyPowerFlex.objects.gen2.protection_domain import ProtectionDomain

LOG = logging.getLogger(__name__)


class StoragePool(base_client.EntityRequest):
    """
    A class representing Storage Pool client.
    """

    def list(self):
        """List PowerFlex storage pools.

        :rtype: list[dict]
        """
        return list(self.get())

    def get_by_id(self, storage_pool_id):
        """Get PowerFlex storage pool.

        :type storage_pool_id: str
        :rtype: dict
        """
        return self.get(entity_id=storage_pool_id)

    def get_by_name(self, protion_domain_id, name):
        """Get PowerFlex storage pool.

        :type protection_domain_id: str
        :type name: str
        :rtype: dict
        """
        pdo = ProtectionDomain(self.token, self.configuration)

        result = pdo.get_storage_pools(
            protion_domain_id, filter_fields={"name": name})
        return result[0] if len(result) > 0 else None

    def check_create_params(self, sp):
        """Check create parameters."""
        required_fields = ["name", "protectionDomainId", "deviceGroupId", "protectionScheme"]
        missing_fields = [field for field in required_fields if field not in sp]

        if missing_fields:
            msg = ("name, protection_domain_id, device_group_id, protection_scheme are required "
                   "for creating a storage pool.")
            raise exceptions.InvalidInput(msg)

        if "useAllAvailableCapacity" not in sp and "physicalSizeGB" not in sp:
            msg = (
                'use_all_available_capacity or physical_size_gb is required '
                'for creating a storage pool.'
            )
            raise exceptions.InvalidInput(msg)

    def create(self, sp):
        """Create PowerFlex storage pool.

        :type sp: dict
        :rtype: dict
        """
        self.check_create_params(sp)

        params = {
            "protectionDomainId": sp["protectionDomainId"],
            "deviceGroupId": sp["deviceGroupId"],
            "gen": "EC",
        }

        if "name" in sp:
            params["name"] = sp["name"]
        if "compressionMethod" in sp:
            params["compressionMethod"] = sp["compressionMethod"]

        if sp["protectionScheme"] == "TwoPlusTwo":
            params["numDataSlices"] = 2
            params["numProtectionSlices"] = 2
        else:
            params["numDataSlices"] = 8
            params["numProtectionSlices"] = 2

        if sp.get("useAllAvailableCapacity"):
            params["useAllAvailableCapacity"] = sp["useAllAvailableCapacity"]
        else:
            params["physicalSizeGB"] = sp["physicalSizeGB"]

        new_sp = self._create_entity(params)
        _, sp = self.update(sp, new_sp)

        return sp

    def check_update_params(self, sp_params, current_sp):
        """Check update parameters."""
        protection_domain_id = sp_params.get("protectionDomainId")
        if protection_domain_id and protection_domain_id != current_sp["protectionDomainId"]:
            e = exceptions.nonupdatable_exception(
                "protection domain ID", self.entity, sp_params["id"]
            )
            LOG.error(e.message)
            raise e
        device_group_id = sp_params.get("deviceGroupId")
        if device_group_id and device_group_id != current_sp["deviceGroupId"]:
            e = exceptions.nonupdatable_exception(
                "device group ID", self.entity, sp_params["id"]
            )
            LOG.error(e.message)
            raise e
        protection_scheme = sp_params.get("protectionScheme")
        if protection_scheme and protection_scheme != current_sp["protectionScheme"]:
            e = exceptions.nonupdatable_exception(
                "protection scheme", self.entity, sp_params["id"]
            )
            LOG.error(e.message)
            raise e

    def _compare_update_params(self, sp_params, current_sp):
        """Compare parameters and determine if an update is needed.

        :type sp_params: dict
        :type current_sp: dict
        :rtype: tuple[bool, dict]
        """
        need_update = False
        changes = {}  # Store the changes to be applied

        new_name = sp_params.get("storage_pool_new_name")
        if new_name and new_name != current_sp["name"]:
            need_update = True
            changes["name"] = new_name

        high_threshold = sp_params.get("capacityAlertHighThreshold", None)
        if high_threshold and high_threshold != current_sp["capacityAlertHighThreshold"]:
            need_update = True
            changes["capacityAlertHighThreshold"] = high_threshold

        critical_threshold = sp_params.get("capacityAlertCriticalThreshold", None)
        current_critical = current_sp["capacityAlertCriticalThreshold"]
        if critical_threshold and critical_threshold != current_critical:
            need_update = True
            changes["capacityAlertCriticalThreshold"] = critical_threshold

        over_provisioning_factor = sp_params.get("overProvisioningFactor", None)
        current_over_provisioning = current_sp["overProvisioningFactor"]
        if over_provisioning_factor and over_provisioning_factor != current_over_provisioning:
            need_update = True
            changes["overProvisioningFactor"] = sp_params["overProvisioningFactor"]

        physical_size_gb = sp_params.get("physicalSizeGB", None)
        if physical_size_gb and physical_size_gb != current_sp["physicalSizeGB"]:
            need_update = True
            changes["physicalSizeGB"] = sp_params["physicalSizeGB"]

        compression_method = sp_params.get("compressionMethod", None)
        if compression_method and compression_method != current_sp["compressionMethod"]:
            need_update = True
            changes["compressionMethod"] = sp_params["compressionMethod"]

        return need_update, changes

    def need_update(self, sp_params, current_sp=None):
        """Check if PowerFlex storage pool needs to be updated.

        :type sp_params: dict
        :type current_sp: dict
        :rtype: bool, dict
        """
        current_sp = current_sp if current_sp is not None else self.get_by_id(sp_params["id"])
        need_update, changes = self._compare_update_params(sp_params, current_sp)
        return need_update, changes

    def update(self, sp_params, current_sp):
        """Update PowerFlex storage pool.

        :type sp_params: dict
        :rtype: dict
        :type current_sp: dict
        :rtype: dict
        """
        need_update, changes = self._compare_update_params(sp_params, current_sp)

        if need_update:
            has_update = False
            if "name" in changes:
                self.rename(sp_params["id"], changes["name"])
                has_update = True
            if ("capacityAlertHighThreshold" in changes or
                    "capacityAlertCriticalThreshold" in changes):
                high_threshold = changes.get("capacityAlertHighThreshold",
                                             current_sp["capacityAlertHighThreshold"])
                critical_threshold = changes.get("capacityAlertCriticalThreshold",
                                                 current_sp["capacityAlertCriticalThreshold"])
                self.set_capacity_alert_thresholds(
                    current_sp["id"], high_threshold, critical_threshold
                )
                has_update = True
            if "overProvisioningFactor" in changes:
                self.set_over_provisioning_factor(
                    current_sp["id"],
                    changes["overProvisioningFactor"]
                )
                has_update = True
            if "physicalSizeGB" in changes:
                self.resize(current_sp["id"], changes["physicalSizeGB"])
                has_update = True
            if "compressionMethod" in changes:
                self.set_compression_method(current_sp["id"], changes["compressionMethod"])
                has_update = True

            sp = self.get_by_id(current_sp["id"])
            return has_update, sp
        return False, current_sp

    def delete(self, storage_pool_id):
        """Remove PowerFlex storage pool.

        :type storage_pool_id: str
        :rtype: None
        """

        return self._delete_entity(storage_pool_id)

    def rename(self, storage_pool_id, name):
        """Rename PowerFlex storage pool.

        :type storage_pool_id: str
        :type name: str
        :rtype: None
        """

        action = "renameStoragePool"

        params = {"newName": name}
        self._rename_entity(action, storage_pool_id, params)

    def set_capacity_alert_thresholds(
            self, storage_pool_id, high_threshold, critical_threshold
    ):
        """Set the capacity alert thresholds for the specified Storage Pool.

        :type high_threshold: int
        :type critical_threshold: int
        :rtype: None
        """

        action = "setCapacityAlertThresholds"

        params = {
            "capacityAlertHighThresholdPercent": high_threshold,
            "capacityAlertCriticalThresholdPercent": critical_threshold,
        }

        r, response = self.send_post_request(
            self.base_action_url,
            action=action,
            entity=self.entity,
            entity_id=storage_pool_id,
            params=params,
        )
        if r.status_code != requests.codes.ok:
            msg = (
                f"Failed to set the capacity alert thresholds for PowerFlex {self.entity}"
                f"with id {storage_pool_id}. Error: {response}"
            )
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

    def set_over_provisioning_factor(self, storage_pool_id, over_provisioning_factor):
        """Set the over provisioning factor for PowerFlex storage pool.

        :type storage_pool_id: str
        :type over_provisioning_factor: int
        :rtype: None
        """

        action = "setOverProvisioningFactor"

        params = {"overProvisioningFactor": over_provisioning_factor}

        r, response = self.send_post_request(
            self.base_action_url,
            action=action,
            entity=self.entity,
            entity_id=storage_pool_id,
            params=params,
        )
        if r.status_code != requests.codes.ok:
            msg = (
                f"Failed to set the over provisioning factor for PowerFlex {self.entity}"
                f" with id {storage_pool_id}. Error: {response}"
            )
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

    def resize(self, storage_pool_id, size_in_gb):
        """
        Set the size for PowerFlex storage pool.

        :param storage_pool_id: The ID of the storage pool.
        :type storage_pool_id: str
        :param size_in_gb: Size in GB to set.
                          If set to -1, it means to use all available capacity
                          (equivalent to setting 'useAllAvailableCapacity' to true).
        :type size_in_gb: int
        :rtype: None
        """

        action = "modifyStoragePoolSize"

        if size_in_gb == -1:
            params = {"useAllAvailableCapacity": True}
        else:
            params = {"physicalSizeGB": size_in_gb}

        r, response = self.send_post_request(
            self.base_action_url,
            action=action,
            entity=self.entity,
            entity_id=storage_pool_id,
            params=params,
        )
        if r.status_code != requests.codes.ok:
            msg = (
                f"Failed to modify the size for PowerFlex {self.entity}"
                f" with id {storage_pool_id}. Error: {response}"
            )
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

    def set_compression_method(self, storage_pool_id, compression_method):
        """Set compression method for PowerFlex storage pool.

        :type storage_pool_id: str
        :type compression_method: str
        :rtype: dict
        """

        action = "modifyCompressionMethod"

        params = {"compressionMethod": compression_method}

        r, response = self.send_post_request(
            self.base_action_url,
            action=action,
            entity=self.entity,
            entity_id=storage_pool_id,
            params=params,
        )
        if r.status_code != requests.codes.ok:
            msg = (
                f"Failed to set compression method for PowerFlex {self.entity} "
                f"with id {storage_pool_id}. Error: {response}"
            )
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

    def set_zero_padding_policy(self, storage_pool_id, zero_padding_enabled):
        """Enable/disable zero padding for PowerFlex storage pool.

        :type storage_pool_id: str
        :type zero_padding_enabled: bool
        :rtype: None
        """

        action = "setZeroPaddingPolicy"

        params = {"zeroPadEnabled": zero_padding_enabled}

        r, response = self.send_post_request(
            self.base_action_url,
            action=action,
            entity=self.entity,
            entity_id=storage_pool_id,
            params=params,
        )
        if r.status_code != requests.codes.ok:
            msg = (
                f"Failed to set Zero Padding policy for PowerFlex {self.entity} "
                f"with id {storage_pool_id}. Error: {response}"
            )
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)
