# Copyright (c) 2020 Dell Inc. or its subsidiaries.
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


class Volume(base_client.EntityRequest):
    def add_mapped_sdc(self,
                       volume_id,
                       sdc_id=None,
                       sdc_guid=None,
                       allow_multiple_mappings=None,
                       allow_ext_managed=None,
                       access_mode=None):
        """Map PowerFlex volume to SDC.

        :param volume_id: str
        :param sdc_id: str
        :param sdc_guid: str
        :param allow_multiple_mappings: bool
        :param allow_ext_managed: bool
        :type access_mode: str
        :return: dict
        """

        action = 'addMappedSdc'

        if all([sdc_id, sdc_guid]) or not any([sdc_id, sdc_guid]):
            msg = 'Either sdc_id or sdc_guid must be set.'
            raise exceptions.InvalidInput(msg)
        params = dict(
            sdcId=sdc_id,
            guid=sdc_guid,
            allowMultipleMappings=allow_multiple_mappings,
            allowOnExtManagedVol=allow_ext_managed,
            accessMode=access_mode
        )

        r, response = self.send_post_request(self.base_action_url,
                                             action=action,
                                             entity=self.entity,
                                             entity_id=volume_id,
                                             params=params)
        if r.status_code != requests.codes.ok:
            msg = ('Failed to map PowerFlex {entity} with id {_id} '
                   'to SDC. Error: {response}'.format(entity=self.entity,
                                                      _id=volume_id,
                                                      response=response))
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

        return self.get(entity_id=volume_id)

    def create(self,
               storage_pool_id,
               size_in_gb,
               name=None,
               volume_type=None,
               use_rmcache=None,
               compression_method=None):
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
        :return: dict
        """

        params = dict(
            storagePoolId=storage_pool_id,
            volumeSizeInGb=size_in_gb,
            name=name,
            volumeType=volume_type,
            useRmcache=use_rmcache,
            compressionMethod=compression_method
        )

        return self._create_entity(params)

    def delete(self, volume_id, remove_mode, allow_ext_managed=None):
        """Remove PowerFlex volume.

        :param volume_id: str
        :param remove_mode: one of predefined attributes of RemoveMode
        :param allow_ext_managed: bool
        :return: None
        """

        params = dict(
            removeMode=remove_mode,
            allowOnExtManagedVol=allow_ext_managed
        )

        return self._delete_entity(volume_id, params)

    def extend(self, volume_id, size_in_gb, allow_ext_managed=None):
        """Extend PowerFlex volume.

        :param volume_id: str
        :param size_in_gb: int
        :param allow_ext_managed: bool
        :return: dict
        """

        action = 'setVolumeSize'

        params = dict(
            sizeInGB=size_in_gb,
            allowOnExtManagedVol=allow_ext_managed
        )

        r, response = self.send_post_request(self.base_action_url,
                                             action=action,
                                             entity=self.entity,
                                             entity_id=volume_id,
                                             params=params)
        if r.status_code != requests.codes.ok:
            msg = ('Failed to extend PowerFlex {entity} with id {_id}. '
                   'Error: {response}'.format(entity=self.entity,
                                              _id=volume_id,
                                              response=response))
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

        return self.get(entity_id=volume_id)

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
            msg = ('Failed to lock AutoSnapshot for PowerFlex {entity} '
                   'with id {_id}. '
                   'Error: {response}'.format(entity=self.entity,
                                              _id=volume_id,
                                              response=response))
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

        return self.get(entity_id=volume_id)

    def remove_mapped_sdc(self,
                          volume_id,
                          sdc_id=None,
                          sdc_guid=None,
                          all_sdcs=None,
                          skip_appliance_validation=None,
                          allow_ext_managed=None):
        """Unmap PowerFlex volume from SDC.

        :param volume_id: str
        :param sdc_id: str
        :param sdc_guid: str
        :param all_sdcs: bool
        :param skip_appliance_validation: bool
        :param allow_ext_managed: bool
        :return: dict
        """

        action = 'removeMappedSdc'

        if (
                all([sdc_id, sdc_guid, all_sdcs]) or
                not any([sdc_id, sdc_guid, all_sdcs])
        ):
            msg = 'Either sdc_id or sdc_guid or all_sdcs must be set.'
            raise exceptions.InvalidInput(msg)

        params = dict(
            sdcId=sdc_id,
            guid=sdc_guid,
            allSdcs=all_sdcs,
            skipApplianceValidation=skip_appliance_validation,
            allowOnExtManagedVol=allow_ext_managed
        )

        r, response = self.send_post_request(self.base_action_url,
                                             action=action,
                                             entity=self.entity,
                                             entity_id=volume_id,
                                             params=params)
        if r.status_code != requests.codes.ok:
            msg = ('Failed to unmap PowerFlex {entity} with id {_id} from '
                   'SDC. Error: {response}'.format(entity=self.entity,
                                                   _id=volume_id,
                                                   response=response))
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

        return self.get(entity_id=volume_id)

    def rename(self, volume_id, name, allow_ext_managed=None):
        """Rename PowerFlex volume.

        :param volume_id: str
        :param name: str
        :param allow_ext_managed: bool
        :return: dict
        """

        action = 'setVolumeName'

        params = dict(
            newName=name,
            allowOnExtManagedVol=allow_ext_managed
        )

        return self._rename_entity(action, volume_id, params)

    def unlock_auto_snapshot(self, volume_id, remove_auto_snapshot=None):
        """Unlock auto snapshot of PowerFlex volume.

        :param volume_id: str
        :param remove_auto_snapshot: bool
        :return: dict
        """

        action = 'unlockAutoSnapshot'

        params = dict(
            autoSnapshotWillBeRemoved=remove_auto_snapshot
        )

        r, response = self.send_post_request(self.base_action_url,
                                             action=action,
                                             entity=self.entity,
                                             entity_id=volume_id,
                                             params=params)
        if r.status_code != requests.codes.ok:
            msg = ('Failed to unlock AutoSnapshot for PowerFlex {entity} '
                   'with id {_id}. Error: '
                   '{response}'.format(entity=self.entity, _id=volume_id,
                                       response=response))
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

        params = dict(
            sdcId=sdc_id,
            bandwidthLimitInKbps=bandwidth_limit,
            iopsLimit=iops_limit
        )

        r, response = self.send_post_request(self.base_action_url,
                                             action=action,
                                             entity=self.entity,
                                             entity_id=volume_id,
                                             params=params)
        if r.status_code != requests.codes.ok:
            msg = ('Failed to update the SDC limits of PowerFlex'
                   ' {entity} with id {_id}. '
                   'Error: {response}'.format(entity=self.entity,
                                              _id=volume_id,
                                              response=response))
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

        params = dict(
            compressionMethod=compression_method,
        )

        r, response = self.send_post_request(self.base_action_url,
                                             action=action,
                                             entity=self.entity,
                                             entity_id=volume_id,
                                             params=params)
        if r.status_code != requests.codes.ok:
            msg = ('Failed to update the compression method of PowerFlex'
                   ' {entity} with id'
                   ' {_id}. Error: {response}'.format(entity=self.entity,
                                                      _id=volume_id,
                                                      response=response))
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

        params = dict(
            useRmcache=use_rmcache
        )

        r, response = self.send_post_request(self.base_action_url,
                                             action=action,
                                             entity=self.entity,
                                             entity_id=volume_id,
                                             params=params)
        if r.status_code != requests.codes.ok:
            msg = ('Failed to update the use_rmcache of PowerFlex'
                   ' {entity} with id {_id}. '
                   'Error: {response}'.format(entity=self.entity,
                                              _id=volume_id,
                                              response=response))
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

        params = dict(
            accessMode=access_mode,
            sdcId=sdc_id
        )

        r, response = self.send_post_request(self.base_action_url,
                                             action=action,
                                             entity=self.entity,
                                             entity_id=volume_id,
                                             params=params)
        if r.status_code != requests.codes.ok:
            msg = ('Failed to set the access mode for the SDC {sdc_id}'
                   ' mapped to PowerFlex {entity} with id {_id}. Error:'
                   ' {response}'.format(entity=self.entity, _id=volume_id,
                                        sdc_id=sdc_id, response=response))
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

        params = dict(
            retentionPeriodInMin=retention_period,
        )

        r, response = self.send_post_request(self.base_action_url,
                                             action=action,
                                             entity=self.entity,
                                             entity_id=snap_id,
                                             params=params)
        if r.status_code != requests.codes.ok:
            msg = ('Failed to set the retention period for PowerFlex'
                   ' {entity} with id {_id}.'
                   ' Error: {response}'.format(entity=self.entity,
                                               _id=snap_id,
                                               response=response))
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

        params = dict(
            accessModeLimit=access_mode_limit
        )

        r, response = self.send_post_request(self.base_action_url,
                                             action=action,
                                             entity=self.entity,
                                             entity_id=volume_id,
                                             params=params)
        if r.status_code != requests.codes.ok:
            msg = ('Failed to update the Volume Access Mode Limit of '
                   'PowerFlex {entity} with id {_id}. Error: {response}'
                   .format(entity=self.entity, _id=volume_id,
                           response=response))
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

        return self.get(entity_id=volume_id)
