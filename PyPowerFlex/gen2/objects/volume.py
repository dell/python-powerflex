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

"""Module for interacting with volume APIs."""

# pylint: disable=too-few-public-methods,no-member,too-many-arguments,too-many-positional-arguments,duplicate-code

import logging

import requests

from PyPowerFlex import base_client
from PyPowerFlex import exceptions

LOG = logging.getLogger(__name__)


class CompressionMethod:
    """Volume compression methods."""

    invalid = 'Invalid'
    none = 'None'
    normal = 'Normal'


class RemoveMode:
    """Volume remove modes.

    Represents volume deletion strategy. See PowerFlex documentation for more
    information.
    """

    only_me = 'ONLY_ME'
    including_descendants = 'INCLUDING_DESCENDANTS'
    descendants_only = 'DESCENDANTS_ONLY'
    whole_vtree = 'WHOLE_VTREE'


class VolumeType:
    """Volume provisioning types."""

    thick = 'ThickProvisioned'
    thin = 'ThinProvisioned'


class VolumeClass:
    """Volume class types."""

    supported_vol_classes = (
      ['defaultclass', 'replication', 'csi', 'openstack', 'vvol', 'datastore',
       'nasfs', 'nasvdm', 'nascluster', 'nas', 'management', 'snap_mobility',
       'ntnx'])
    for vol_class in supported_vol_classes:
        locals()[vol_class] = vol_class


class Volume(base_client.EntityRequest):
    """
    A class representing Volume client.
    """
    def add_mapped_sdc(self,
                       volume_id,
                       sdc_id=None,
                       sdc_guid=None,
                       allow_multiple_mappings=None,
                       allow_ext_managed=None,
                       access_mode=None,
                       volume_class=VolumeClass.defaultclass):
        """Map PowerFlex volume to SDC.

        :param volume_id: str
        :param sdc_id: str
        :param sdc_guid: str
        :param allow_multiple_mappings: bool
        :param allow_ext_managed: bool
        :type access_mode: str
        :param volume_class: str
        :return: dict
        """

        action = 'addMappedSdc'

        if all([sdc_id, sdc_guid]) or not any([sdc_id, sdc_guid]):
            msg = 'Either sdc_id or sdc_guid must be set.'
            raise exceptions.InvalidInput(msg)
        params = {
            "sdcId": sdc_id,
            "guid": sdc_guid,
            "allowMultipleMappings": allow_multiple_mappings,
            "allowOnExtManagedVol": allow_ext_managed,
            "accessMode": access_mode,
            "volumeClass": volume_class
        }

        r, response = self.send_post_request(self.base_action_url,
                                             action=action,
                                             entity=self.entity,
                                             entity_id=volume_id,
                                             params=params)
        if r.status_code != requests.codes.ok:
            msg = (
                f"Failed to map PowerFlex {self.entity} with id {volume_id} "
                f"to SDC. Error: {response}"
            )
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

        return self.get(entity_id=volume_id)

    def create(self,
               storage_pool_id,
               size_in_gb,
               name=None,
               volume_type=None,
               use_rmcache=None,
               compression_method=None,
               volume_class=VolumeClass.defaultclass):
        """Create PowerFlex volume.

        :param storage_pool_id: str
        :param size_in_gb: int
        :param name: str
        :param volume_type: one of predefined attributes of VolumeType
        :type volume_type: str
        :param use_rmcache: bool
        :param compression_method: one of predefined attributes of
                                   CompressionMethod
        :type compression_method: str
        :param volume_class: str
        :return: dict
        """

        params = {
            'storagePoolId': storage_pool_id,
            'volumeSizeInGb': size_in_gb,
            'name': name,
            'volumeType': volume_type,
            'useRmcache': use_rmcache,
            'compressionMethod': compression_method,
            'volumeClass': volume_class
        }

        return self._create_entity(params)

    def delete(self, volume_id, remove_mode, allow_ext_managed=None,
               volume_class=VolumeClass.defaultclass):
        """Remove PowerFlex volume.

        :param volume_id: str
        :param remove_mode: one of predefined attributes of RemoveMode
        :param allow_ext_managed: bool
        :param volume_class: str
        :return: None
        """

        params = {
            "removeMode": remove_mode,
            "allowOnExtManagedVol": allow_ext_managed,
            "volumeClass": volume_class
        }

        return self._delete_entity(volume_id, params)

    def extend(self, volume_id, size_in_gb, allow_ext_managed=None,
               volume_class=VolumeClass.defaultclass):
        """Extend PowerFlex volume.

        :param volume_id: str
        :param size_in_gb: int
        :param allow_ext_managed: bool
        :param volume_class: str
        :return: dict
        """

        action = 'setVolumeSize'

        params = {"sizeInGB": size_in_gb,
                  "allowOnExtManagedVol": allow_ext_managed,
                  "volumeClass": volume_class}

        r, response = self.send_post_request(self.base_action_url,
                                             action=action,
                                             entity=self.entity,
                                             entity_id=volume_id,
                                             params=params)
        if r.status_code != requests.codes.ok:
            msg = (
                f"Failed to extend PowerFlex {self.entity} with id {volume_id}. "
                f"Error: {response}"
            )
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

        return self.get(entity_id=volume_id)

    def get_statistics(self, volume_id, fields=None):
        """Get related PowerFlex Statistics for volume.

        :type volume_id: str
        :type fields: list|tuple
        :rtype: dict
        """

        return self.get_related(volume_id,
                                'Statistics',
                                fields)

    def lock_auto_snapshot(self, volume_id):
        """Lock auto snapshot of PowerFlex volume.

        :param volume_id: str
        :return: dict
        """

        action = 'lockAutoSnapshot'

        r, response = self.send_post_request(self.base_action_url,
                                             action=action,
                                             entity=self.entity,
                                             entity_id=volume_id)
        if r.status_code != requests.codes.ok:
            msg = (
                f"Failed to lock AutoSnapshot for PowerFlex {self.entity} "
                f"with id {volume_id}. "
                f"Error: {response}"
            )
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

        return self.get(entity_id=volume_id)

    def remove_mapped_sdc(self,
                          volume_id,
                          sdc_id=None,
                          sdc_guid=None,
                          all_sdcs=None,
                          skip_appliance_validation=None,
                          allow_ext_managed=None,
                          volume_class=VolumeClass.defaultclass):
        """Unmap PowerFlex volume from SDC.

        :param volume_id: str
        :param sdc_id: str
        :param sdc_guid: str
        :param all_sdcs: bool
        :param skip_appliance_validation: bool
        :param allow_ext_managed: bool
        :param volume_class: str
        :return: dict
        """

        action = 'removeMappedSdc'

        if (
                all([sdc_id, sdc_guid, all_sdcs]) or
                not any([sdc_id, sdc_guid, all_sdcs])
        ):
            msg = 'Either sdc_id or sdc_guid or all_sdcs must be set.'
            raise exceptions.InvalidInput(msg)

        params = {
            "sdcId": sdc_id,
            "guid": sdc_guid,
            "allSdcs": all_sdcs,
            "skipApplianceValidation": skip_appliance_validation,
            "allowOnExtManagedVol": allow_ext_managed,
            "volumeClass": volume_class
        }

        r, response = self.send_post_request(self.base_action_url,
                                             action=action,
                                             entity=self.entity,
                                             entity_id=volume_id,
                                             params=params)
        if r.status_code != requests.codes.ok:
            msg = (
                f"Failed to unmap PowerFlex {self.entity} with id {volume_id} from "
                f"SDC. Error: {response}"
            )
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

        return self.get(entity_id=volume_id)

    def rename(self, volume_id, name, allow_ext_managed=None,
               volume_class=VolumeClass.defaultclass):
        """Rename PowerFlex volume.

        :param volume_id: str
        :param name: str
        :param allow_ext_managed: bool
        :param volume_class: str
        :return: dict
        """

        action = 'setVolumeName'

        params = {
            "newName": name,
            "allowOnExtManagedVol": allow_ext_managed,
            "volumeClass": volume_class
        }

        return self._rename_entity(action, volume_id, params)

    def unlock_auto_snapshot(self, volume_id, remove_auto_snapshot=None):
        """Unlock auto snapshot of PowerFlex volume.

        :param volume_id: str
        :param remove_auto_snapshot: bool
        :return: dict
        """

        action = 'unlockAutoSnapshot'

        params = {
            "autoSnapshotWillBeRemoved": remove_auto_snapshot
        }

        r, response = self.send_post_request(self.base_action_url,
                                             action=action,
                                             entity=self.entity,
                                             entity_id=volume_id,
                                             params=params)
        if r.status_code != requests.codes.ok:
            msg = (
                f"Failed to unlock AutoSnapshot for PowerFlex {self.entity} "
                f"with id {volume_id}. Error: {response}"
            )
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

        return self.get(entity_id=volume_id)

    def set_mapped_sdc_limits(self, volume_id, sdc_id, bandwidth_limit=None,
                              iops_limit=None):
        """Set the bandwidth limit and IOPS limit for the mapped SDC.

        :param volume_id: ID of the volume
        :type volume_id: str
        :param sdc_id: ID of the SDC
        :type sdc_id: str
        :param bandwidth_limit: Limit for the volume network bandwidth
        :type bandwidth_limit: str
        :param iops_limit: Limit for the volume IOPS
        :type iops_limit: str
        :return: dict
        """

        action = 'setMappedSdcLimits'

        params = {
            "sdcId": sdc_id,
            "bandwidthLimitInKbps": bandwidth_limit,
            "iopsLimit": iops_limit
        }

        r, response = self.send_post_request(self.base_action_url,
                                             action=action,
                                             entity=self.entity,
                                             entity_id=volume_id,
                                             params=params)
        if r.status_code != requests.codes.ok:
            msg = (
                f"Failed to update the SDC limits of PowerFlex "
                f"{self.entity} with id {volume_id}. "
                f"Error: {response}"
            )
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

        return self.get(entity_id=volume_id)

    def set_compression_method(self, volume_id, compression_method):
        """
        Modify the compression method to be used for a Volume, relevant only
        if the volume has a space efficient data layout.

        :param volume_id: ID of the volume
        :type volume_id: str
        :param compression_method: one of predefined attributes of
        CompressionMethod
        :type compression_method: str
        :return: dict
        """

        action = 'modifyCompressionMethod'

        params = {
            'compressionMethod': compression_method,
        }

        r, response = self.send_post_request(self.base_action_url,
                                             action=action,
                                             entity=self.entity,
                                             entity_id=volume_id,
                                             params=params)
        if r.status_code != requests.codes.ok:
            msg = (
                f"Failed to update the compression method of PowerFlex "
                f"{self.entity} with id {volume_id}. Error: {response}"
            )
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

        return self.get(entity_id=volume_id)

    def set_use_rmcache(self, volume_id, use_rmcache):
        """
        Control the use of Read RAM Cache in the specified volume.
        If you want to ensure that all I/O operations for this volume are
        cached, the relevant Storage Pool should be configured to use cache,
        and the relevant SDSs should all have caching enabled.

        :param volume_id: ID of the volume
        :type volume_id: str
        :param use_rmcache: Whether to use Read RAM cache or not
        :type use_rm_cache: bool
        :return: dict
        """

        action = 'setVolumeUseRmcache'

        params = {
            "useRmcache": use_rmcache
        }

        r, response = self.send_post_request(self.base_action_url,
                                             action=action,
                                             entity=self.entity,
                                             entity_id=volume_id,
                                             params=params)
        if r.status_code != requests.codes.ok:
            msg = (
                f"Failed to update the use_rmcache of PowerFlex "
                f"{self.entity} with id {volume_id}. "
                f"Error: {response}"
            )
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

        return self.get(entity_id=volume_id)

    def set_access_mode_for_sdc(self, volume_id, sdc_id, access_mode):
        """
        Set the volume access mode for the specified
        SDC mapped to the volume.

        :param volume_id: ID of the volume
        :type volume_id: str
        :param access_mode: The access mode of the volume for the mapped SDC
        :type access_mode: str
        :param sdc_id: ID of the SDC.
        :type sdc_id: str
        :return: dict
        """

        action = 'setVolumeMappingAccessMode'

        params = {
            "accessMode": access_mode,
            "sdcId": sdc_id
        }

        r, response = self.send_post_request(self.base_action_url,
                                             action=action,
                                             entity=self.entity,
                                             entity_id=volume_id,
                                             params=params)
        if r.status_code != requests.codes.ok:
            msg = (
                f"Failed to set the access mode for the SDC {sdc_id} "
                f"mapped to PowerFlex {self.entity} with id {volume_id}. Error: "
                f"{response}"
            )
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

        return self.get(entity_id=volume_id)

    def set_retention_period(self, snap_id, retention_period):
        """
        Set a new retention period for the given snapshot. If the snapshot
        is already secure, then it can be delayed but not advanced.

        :param snap_id: ID of the volume
        :type snap_id: str
        :param retention_period: Retention period for the specified resource
        :type retention_period: str
        :return: dict
        """

        action = 'setSnapshotSecurity'

        params = {
            "retentionPeriodInMin": retention_period,
        }

        r, response = self.send_post_request(self.base_action_url,
                                             action=action,
                                             entity=self.entity,
                                             entity_id=snap_id,
                                             params=params)
        if r.status_code != requests.codes.ok:
            msg = (
                f"Failed to set the retention period for PowerFlex {self.entity} "
                f"with id {snap_id}. Error: {response}"
            )
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

        return self.get(entity_id=snap_id)

    def set_volume_access_mode_limit(self, volume_id, access_mode_limit):
        """
        Set the highest mapping access mode allowed for a volume.

        :param volume_id: ID of the volume
        :type volume_id: str
        :param access_mode_limit: Define the access mode limit of a volume,
         options are ReadWrite or ReadOnly
        :type access_mode_limit: str
        :return: dict
        """

        action = 'setVolumeAccessModeLimit'

        params = {"accessModeLimit": access_mode_limit}

        r, response = self.send_post_request(self.base_action_url,
                                             action=action,
                                             entity=self.entity,
                                             entity_id=volume_id,
                                             params=params)
        if r.status_code != requests.codes.ok:
            msg = (
                f"Failed to update the Volume Access Mode Limit of PowerFlex "
                f"{self.entity} with id {volume_id}. Error: {response}"
            )
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

        return self.get(entity_id=volume_id)

    def query_selected_statistics(self, properties, ids=None):
        """Query PowerFlex volume statistics.

        :type properties: list
        :type ids: list of volume IDs or None for all volumes
        :rtype: dict
        """

        action = "querySelectedStatistics"

        params = {'properties': properties}

        if ids:
            params["ids"] = ids
        else:
            params["allIds"] = ""

        return self._query_selected_statistics(action, params)
