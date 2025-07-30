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

from marshmallow import fields, validate, ValidationError
from PyPowerFlex import base_client, exceptions
from PyPowerFlex.objects.gen2.protection_domain import ProtectionDomain


LOG = logging.getLogger(__name__)


def validate_over_provisioning_factor(value):
    """Validate over provisioning factor."""
    if value != 0 and (value < 100 or value > 10000):
        raise ValidationError("Not an valid value.")


class StoragePoolSchema(base_client.BaseSchema):
    """Storage Pool Schema."""

    id = fields.Str(
        metadata={
            "description": "Storage Pool Id",
        }
    )
    name = fields.Str(
        allow_none=True,
        metadata={
            "description": "Storage Pool Name",
            "updatable": True,
        },
    )
    protection_domain_id = fields.Str(
        required=True,
        metadata={
            "description": "Protection Domain Id",
            "updatable": False,
        },
    )
    device_group_id = fields.Str(
        required=True,
        metadata={
            "description": "Device Group Id",
            "updatable": False,
        },
    )
    wrc_device_group_id = fields.Str(
        metadata={
            "description": "Device Group Id",
            # TODO:
            # "updatable": False,
        }
    )
    gen_type = fields.Str(
        # required=True,  # 5.0.0 only supports EC type
        metadata={
            "description": "Gen Type, EC or MIRRORING",
        }
    )
    capacity_alert_high_threshold = fields.Integer(
        metadata={
            "description": "Capacity Alert High Threshold, default: 80",
            "updatable": True,
        }
    )
    capacity_alert_critical_threshold = fields.Integer(
        metadata={
            "description": "Capacity Alert Critical Threshold, default: 90",
            "updatable": True,
        }
    )
    fragmentation_enabled = fields.Boolean(
        metadata={
            "description": "Enable Fragmentation, default: False",
            # "updatable": True,
        }
    )
    over_provisioning_factor = fields.Integer(
        validate=validate.And(validate_over_provisioning_factor),
        metadata={
            "description": (
                "Over Provisioning Factor, range: 0, 100-10000, "
                "set 0 to disable over provisioning. Default: 0"
            ),
        },
    )
    physical_size_gb = fields.Integer(
        required=True,
        data_key="physicalSizeGB",
        metadata={
            "description": (
                "Physical Size in GB, set -1 to use all available capacity. "
                "It only accepts larger value during update."
            ),
            "updatable": True,
        },
    )
    raw_size_gb = fields.Integer(
        data_key="rawSizeGB",
        metadata={
            "description": "Raw Size in GB",
        },
    )
    protection_scheme = fields.Str(
        required=True,
        validate=validate.OneOf(["TwoPlusTwo", "EightPlusTwo"]),
        metadata={
            "description": "Protection Scheme: TwoPlusTwo/EightPlusTwo",
            "updatable": False,
        },
    )
    compression_method = fields.Str(
        validate=validate.OneOf(["None", "Normal"]),
        metadata={
            "description": "Compression Method: None/Normal. Default: Normal",
            "updatable": True,
        },
    )
    zero_padding_enabled = fields.Boolean(
        metadata={
            "description": "Zero padding enabled. Default: True",
        }
    )
    # @validates_schema
    # def validate_capacity_alert_threshold(self, data, **kwargs):
    #     if data["capacity_alert_high_threshold"] >= data["capacity_alert_critical_threshold"]:
    #         raise ValidationError(
    #             "capacity_alert_critical_threshold must be greater than "
    #             "capacity_alert_high_threshold"
    #         )

    # class Meta:
    #     unknown = INCLUDE

def load_storage_pool_schema(obj):
    """Load storage pool schema."""
    return StoragePoolSchema().load(obj)


class StoragePool(base_client.EntityRequest):
    """
    A class representing Storage Pool client.
    """

    def list(self):
        """List PowerFlex storage pools.

        :rtype: list[dict]
        """
        return list(map(load_storage_pool_schema, self.get()))

    def get_by_id(self, storage_pool_id):
        """Get PowerFlex storage pool.

        :type storage_pool_id: str
        :rtype: dict
        """
        return load_storage_pool_schema(self.get(entity_id=storage_pool_id))

    def get_by_name(self, protion_domain_id, name):
        """Get PowerFlex storage pool.

        :type protection_domain_id: str
        :type name: str
        :rtype: dict
        """
        pdo = ProtectionDomain(self.token, self.configuration)

        result = pdo.get_storage_pools(protion_domain_id, filter_fields={"name": name})
        if len(result) >= 1:
            return load_storage_pool_schema(result[0])
        return None

    def create(self, sp):
        """Create PowerFlex storage pool.

        :type sp: dict
        :rtype: dict
        """
        sp = load_storage_pool_schema(sp)

        params = {
            "protectionDomainId": sp["protection_domain_id"],
            "deviceGroupId": sp["device_group_id"],
            "gen": "EC",
        }

        if "name" in sp:
            params["name"] = sp["name"]
        if "compression_method" in sp:
            params["compressionMethod"] = sp["compression_method"]

        if sp["protection_scheme"] == "TwoPlusTwo":
            params["numDataSlices"] = 2
            params["numProtectionSlices"] = 2
        else:
            params["numDataSlices"] = 8
            params["numProtectionSlices"] = 2

        if sp["physical_size_gb"] == -1:
            params["useAllAvailableCapacity"] = True
        else:
            params["physicalSizeGB"] = sp["physical_size_gb"]

        new_sp = load_storage_pool_schema(self._create_entity(params))
        sp["id"] = new_sp["id"]
        _, sp = self.update(StoragePoolSchema().dump(sp), new_sp)

        return sp

    def update(self, sp, current_sp=None):
        """Update PowerFlex storage pool.

        :type sp: dict
        :rtype: dict
        """
        current_sp = current_sp if current_sp is not None else self.get_by_id(sp["id"])
        sp = load_storage_pool_schema({**StoragePoolSchema().dump(current_sp), **sp})

        if sp["protection_domain_id"] != current_sp["protection_domain_id"]:
            e = exceptions.nonupdatable_exception(
                "protection_domain_id", self.entity, sp["id"]
            )
            LOG.error(e.message)
            raise e
        if sp["device_group_id"] != current_sp["device_group_id"]:
            e = exceptions.nonupdatable_exception(
                "device_group_id", self.entity, sp["id"]
            )
            LOG.error(e.message)
            raise e
        if sp["protection_scheme"] != current_sp["protection_scheme"]:
            e = exceptions.nonupdatable_exception(
                "protection_scheme", self.entity, sp["id"]
            )
            LOG.error(e.message)
            raise e

        has_update = False

        if sp["name"] != current_sp["name"]:
            has_update = True
            self.rename(sp["id"], sp["name"])

        high_threshold = None
        critical_threshold = None

        if (
            sp["capacity_alert_high_threshold"]
            != current_sp["capacity_alert_high_threshold"]
        ):
            high_threshold = sp["capacity_alert_high_threshold"]

        if (
            sp["capacity_alert_critical_threshold"]
            != current_sp["capacity_alert_critical_threshold"]
        ):
            critical_threshold = sp["capacity_alert_critical_threshold"]

        if high_threshold or critical_threshold:
            has_update = True
            self.set_capacity_alert_thresholds(
                sp["id"], high_threshold, critical_threshold
            )

        if sp["over_provisioning_factor"] != current_sp["over_provisioning_factor"]:
            has_update = True
            self.set_over_provisioning_factor(sp["id"], sp["over_provisioning_factor"])

        if sp["physical_size_gb"] != current_sp["physical_size_gb"]:
            has_update = True
            self.resize(sp["id"], sp["physical_size_gb"])

        if sp["compression_method"] != current_sp["compression_method"]:
            has_update = True
            self.set_compression_method(sp["id"], sp["compression_method"])

        return has_update, self.get_by_id(sp["id"])

    def delete(self, storage_pool_id):
        """Remove PowerFlex storage pool.

        :type storage_pool_id: str
        :rtype: None
        """

        return self._delete_entity(storage_pool_id)

    # def get_devices(self, storage_pool_id, filter_fields=None, fields=None):
    #     """Get related PowerFlex devices for storage pool.

    #     :type storage_pool_id: str
    #     :type filter_fields: dict
    #     :type fields: list|tuple
    #     :rtype: list[dict]
    #     """

    #     return self.get_related(storage_pool_id,
    #                             'Device',
    #                             filter_fields,
    #                             fields)

    # def get_sdss(self, storage_pool_id, filter_fields=None, fields=None):
    #     """Get related PowerFlex SDSs for storage pool.

    #     :type storage_pool_id: str
    #     :type filter_fields: dict
    #     :type fields: list|tuple
    #     :rtype: list[dict]
    #     """

    #     sdss_ids = self.get_related(storage_pool_id,
    #                                 'SpSds',
    #                                 filter_fields,
    #                                 fields=('sdsId',))
    #     sds_id_list = [sds['sdsId'] for sds in sdss_ids]
    #     if filter_fields:
    #         filter_fields.update({'id': sds_id_list})
    #         filter_fields.pop('sdsId', None)
    #     else:
    #         filter_fields = {'id': sds_id_list}
    #     return Sds(self.token, self.configuration).get(
    #         filter_fields=filter_fields, fields=fields)

    # def get_volumes(self, storage_pool_id, filter_fields=None, fields=None):
    #     """Get related PowerFlex volumes for storage pool.

    #     :type storage_pool_id: str
    #     :type filter_fields: dict
    #     :type fields: list|tuple
    #     :rtype: list[dict]
    #     """

    #     return self.get_related(storage_pool_id,
    #                             'Volume',
    #                             filter_fields,
    #                             fields)

    # def get_statistics(self, storage_pool_id, fields=None):
    #     """Get related PowerFlex Statistics for storage pool.

    #     :type storage_pool_id: str
    #     :type fields: list|tuple
    #     :rtype: dict
    #     """

    #     return self.get_related(storage_pool_id,
    #                             'Statistics',
    #                             fields)

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
        """Set the size for PowerFlex storage pool.

        :type storage_pool_id: str
        :type size: int
        :rtype: None
        """

        action = "modifyStoragePoolSize"

        params = {"physicalSizeGB": size_in_gb}

        if size_in_gb == -1:
            params = {"useAllAvailableCapacity": True}

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

    # def query_selected_statistics(self, properties, ids=None):
    #     """Query PowerFlex storage pool statistics.

    #     :type properties: list
    #     :type ids: list of storage pools IDs or None for all storage pools
    #     :rtype: dict
    #     """

    #     action = "querySelectedStatistics"

    #     params = {'properties': properties}

    #     if ids:
    #         params["ids"] = ids
    #     else:
    #         params["allIds"] = ""

    #     return self._query_selected_statistics(action, params)
