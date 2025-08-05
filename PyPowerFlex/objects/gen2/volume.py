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

"""Module for interacting with volume APIs for Gen2."""

# pylint: disable=too-few-public-methods,no-member,too-many-arguments,too-many-positional-arguments,duplicate-code

import logging

import requests

from PyPowerFlex import base_client
from PyPowerFlex import exceptions
from PyPowerFlex.constants import VolumeConstantsGen2

LOG = logging.getLogger(__name__)


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
       'nasfs', 'nasvdm', 'nascluster', 'nas'])
    for vol_class in supported_vol_classes:
        locals()[vol_class] = vol_class


class Volume(base_client.EntityRequest):
    """
    A class representing Volume client.
    Note that this class could also be used for snapshot and thin clone.
    """
    def add_mapped_host(self,
                       volume_id,
                       host_id=None,
                       guid=None,
                       nqn=None,
                       allow_multiple_mappings=None,
                       access_mode=None,
                       volume_class=VolumeClass.defaultclass):
        """Map PowerFlex volume to host.

        :param volume_id: str
        :param host_id: str
        :param guid: str
        :param nqn: str
        :param allow_multiple_mappings: bool
        :type access_mode: str
        :param volume_class: str
        :return: dict
        """

        action = 'addMappedHost'

        params = {
            "hostId": host_id,
            "guid": guid,
            "nqn": nqn,
            "allowMultipleMappings": allow_multiple_mappings,
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
                f"to host. Error: {response}"
            )
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

    def create(self,
               storage_pool_id,
               size_in_gb,
               name=None,
               volume_type=None,
               use_rmcache=None,
               volume_class=VolumeClass.defaultclass):
        """Create PowerFlex volume.

        :param storage_pool_id: str
        :param size_in_gb: int
        :param name: str
        :param volume_type: one of predefined attributes of VolumeType
        :type volume_type: str
        :param use_rmcache: bool
        :param volume_class: str
        :return: dict
        """

        params = {
            'storagePoolId': storage_pool_id,
            'volumeSizeInGb': size_in_gb,
            'name': name,
            'volumeType': volume_type,
            'useRmcache': use_rmcache,
            'volumeClass': volume_class
        }

        return self._create_entity(params)

    def delete(self, volume_id, remove_mode,
               volume_class=VolumeClass.defaultclass):
        """Remove PowerFlex volume/snapshot/thin clone.

        :param volume_id: str
        :param remove_mode: one of predefined attributes of RemoveMode
        :param volume_class: str
        :return: None
        """

        params = {
            "removeMode": remove_mode,
            "volumeClass": volume_class
        }

        return self._delete_entity(volume_id, params)

    def extend(self, volume_id, size_in_gb,
               volume_class=VolumeClass.defaultclass):
        """Extend PowerFlex volume/thin clone.

        :param volume_id: str
        :param size_in_gb: int
        :param volume_class: str
        :return: dict
        """

        action = 'setVolumeSize'

        params = {"sizeInGB": size_in_gb,
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

    def get_statistics(self, volume_id, metrics=None):
        """Get related PowerFlex Statistics for volume.

        :type volume_id: str
        :type metrics: list|tuple
        :rtype: dict
        """

        metrics = metrics or VolumeConstantsGen2.DEFAULT_STATISTICS_METRICS
        return self.query_metrics('volume', volume_id, metrics)

    def remove_mapped_host(self,
                          volume_id,
                          host_id=None,
                          guid=None,
                          nqn=None,
                          all_hosts=None,
                          volume_class=VolumeClass.defaultclass):
        """Unmap PowerFlex volume from host.

        :param volume_id: str
        :param host_id: str
        :param guid: str
        :param nqn: str
        :param all_hosts: bool
        :param volume_class: str
        :return: dict
        """

        action = 'removeMappedHost'

        params = {
            "hostId": host_id,
            "guid": guid,
            "nqn": nqn,
            "allHosts": all_hosts,
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
                f"host. Error: {response}"
            )
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

    def rename(self, volume_id, name,
               volume_class=VolumeClass.defaultclass):
        """Rename PowerFlex volume/snapshot/thin clone.

        :param volume_id: str
        :param name: str
        :param volume_class: str
        :return: dict
        """

        action = 'setVolumeName'

        params = {
            "newName": name,
            "volumeClass": volume_class
        }

        return self._rename_entity(action, volume_id, params)

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

    def refresh(self, dest_vol_id, src_vol_id):
        """
        Refresh a destination volume from a source volume.

        :param dest_vol_id: ID of the destination volume
        :type dest_vol_id: str
        :param src_vol_id: ID of the source volume
        :type src_vol_id: str
        :return: dict
        """

        action = 'refresh'

        params = {
            "srcVolumeId": src_vol_id
        }

        r, response = self.send_post_request(self.base_action_url,
                                             action=action,
                                             entity=self.entity,
                                             entity_id=dest_vol_id,
                                             params=params)
        if r.status_code != requests.codes.ok:
            msg = (
                f"Failed to refresh PowerFlex {self.entity} "
                f"with id {dest_vol_id}. Error: {response}"
            )
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

    def restore(self, dest_vol_id, src_vol_id):
        """
        Restore a destination volume from a source volume.

        :param dest_vol_id: ID of the destination volume
        :type dest_vol_id: str
        :param src_vol_id: ID of the source volume
        :type src_vol_id: str
        :return: dict
        """

        action = 'restore'

        params = {
            "srcVolumeId": src_vol_id
        }

        r, response = self.send_post_request(self.base_action_url,
                                             action=action,
                                             entity=self.entity,
                                             entity_id=dest_vol_id,
                                             params=params)
        if r.status_code != requests.codes.ok:
            msg = (
                f"Failed to restore PowerFlex {self.entity} "
                f"with id {dest_vol_id}. Error: {response}"
            )
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)
