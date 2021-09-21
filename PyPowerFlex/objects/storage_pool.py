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
from PyPowerFlex.objects import Sds


LOG = logging.getLogger(__name__)


class CompressionMethod:
    """Storage pool compression methods."""

    invalid = 'Invalid'
    none = 'None'
    normal = 'Normal'


class DataLayout:
    """Storage pool data layouts."""

    invalid = 'InvalidLayout'
    medium = 'MediumGranularity'
    fine = 'FineGranularity'


class ExternalAccelerationType:
    """Storage pool external acceleration types."""

    none = 'None'
    read = 'Read'
    write = 'Write'
    read_and_write = 'ReadAndWrite'


class MediaType:
    """Storage pool media types."""

    hdd = 'HDD'
    ssd = 'SSD'
    transitional = 'Transitional'


class RmcacheWriteHandlingMode:
    """Rmcache write handling modes."""

    passthrough = 'Passthrough'
    cached = 'Cached'


class StoragePool(base_client.EntityRequest):
    def create(self,
               media_type,
               protection_domain_id,
               checksum_enabled=None,
               compression_method=None,
               data_layout=None,
               external_acceleration_type=None,
               fgl_accp_id=None,
               name=None,
               rmcache_write_handling_mode=None,
               spare_percentage=None,
               use_rfcache=None,
               use_rmcache=None,
               zero_padding_enabled=None):
        """Create PowerFlex storage pool.

        :param media_type: one of predefined attributes of MediaType
        :type media_type: str
        :type protection_domain_id: str
        :type checksum_enabled: bool
        :param compression_method: one of predefined attributes of
                                   CompressionMethod
        :type compression_method: str
        :param data_layout: one of predefined attributes of DataLayout
        :type data_layout: str
        :param external_acceleration_type: one of predefined attributes of
                                           ExternalAccelerationType
        :type external_acceleration_type: str
        :type fgl_accp_id: str
        :type name: str
        :param rmcache_write_handling_mode: one of predefined attributes of
                                            RmcacheWriteHandlingMode
        :type spare_percentage: int
        :type use_rfcache: bool
        :type use_rmcache: bool
        :type zero_padding_enabled: bool
        :rtype: dict
        """

        if data_layout == DataLayout.fine and not fgl_accp_id:
            msg = 'fgl_accp_id must be set for Fine Granular Storage Pool.'
            raise exceptions.InvalidInput(msg)
        params = dict(
            mediaType=media_type,
            protectionDomainId=protection_domain_id,
            checksumEnabled=checksum_enabled,
            compressionMethod=compression_method,
            dataLayout=data_layout,
            externalAccelerationType=external_acceleration_type,
            fglAccpId=fgl_accp_id,
            name=name,
            rmcacheWriteHandlingMode=rmcache_write_handling_mode,
            sparePercentage=spare_percentage,
            useRfcache=use_rfcache,
            useRmcache=use_rmcache,
            zeroPaddingEnabled=zero_padding_enabled
        )

        return self._create_entity(params)

    def delete(self, storage_pool_id):
        """Remove PowerFlex storage pool.

        :type storage_pool_id: str
        :rtype: None
        """

        return self._delete_entity(storage_pool_id)

    def get_devices(self, storage_pool_id, filter_fields=None, fields=None):
        """Get related PowerFlex devices for storage pool.

        :type storage_pool_id: str
        :type filter_fields: dict
        :type fields: list|tuple
        :rtype: list[dict]
        """

        return self.get_related(storage_pool_id,
                                'Device',
                                filter_fields,
                                fields)

    def get_sdss(self, storage_pool_id, filter_fields=None, fields=None):
        """Get related PowerFlex SDSs for storage pool.

        :type storage_pool_id: str
        :type filter_fields: dict
        :type fields: list|tuple
        :rtype: list[dict]
        """

        sdss_ids = self.get_related(storage_pool_id,
                                    'SpSds',
                                    filter_fields,
                                    fields=('sdsId',))
        if filter_fields:
            filter_fields.update({'id': sdss_ids})
        return Sds(self.token, self.configuration).get(filter_fields, fields)

    def get_volumes(self, storage_pool_id, filter_fields=None, fields=None):
        """Get related PowerFlex volumes for storage pool.

        :type storage_pool_id: str
        :type filter_fields: dict
        :type fields: list|tuple
        :rtype: list[dict]
        """

        return self.get_related(storage_pool_id,
                                'Volume',
                                filter_fields,
                                fields)

    def rename(self, storage_pool_id, name):
        """Rename PowerFlex storage pool.

        :type storage_pool_id: str
        :type name: str
        :rtype: dict
        """

        action = 'setStoragePoolName'

        params = dict(
            name=name
        )

        return self._rename_entity(action, storage_pool_id, params)

    def set_checksum_enabled(self, storage_pool_id, checksum_enabled):
        """Enable/disable checksum for PowerFlex storage pool.

        :type storage_pool_id: str
        :type checksum_enabled: bool
        :rtype: dict
        """

        action = 'setChecksumEnabled'

        params = dict(
            checksumEnabled=checksum_enabled
        )

        r, response = self.send_post_request(self.base_action_url,
                                             action=action,
                                             entity=self.entity,
                                             entity_id=storage_pool_id,
                                             params=params)
        if r.status_code != requests.codes.ok:
            msg = ('Failed to enable/disable checksum for PowerFlex {entity} '
                   'with id {_id}. Error: {response}'
                   .format(entity=self.entity, _id=storage_pool_id,
                           response=response))
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

        return self.get(entity_id=storage_pool_id)

    def set_compression_method(self, storage_pool_id, compression_method):
        """Set compression method for PowerFlex storage pool.

        :type storage_pool_id: str
        :type compression_method: str
        :rtype: dict
        """

        action = 'modifyCompressionMethod'

        params = dict(
            compressionMethod=compression_method
        )

        r, response = self.send_post_request(self.base_action_url,
                                             action=action,
                                             entity=self.entity,
                                             entity_id=storage_pool_id,
                                             params=params)
        if r.status_code != requests.codes.ok:
            msg = ('Failed to set compression method for PowerFlex {entity} '
                   'with id {_id}. Error: {response}'
                   .format(entity=self.entity, _id=storage_pool_id,
                           response=response))
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

        return self.get(entity_id=storage_pool_id)

    def set_external_acceleration_type(
            self,
            storage_pool_id,
            external_acceleration_type,
            override_device_configuration=None,
            keep_device_ext_acceleration=None
    ):
        """Set external acceleration type for PowerFlex storage pool.

        :type storage_pool_id: str
        :param external_acceleration_type: one of predefined attributes of
                                           ExternalAccelerationType
        :type external_acceleration_type: str
        :type override_device_configuration: bool
        :type keep_device_ext_acceleration: bool
        :rtype: dict
        """

        action = 'setExternalAccelerationType'

        if all([override_device_configuration, keep_device_ext_acceleration]):
            msg = ('Either override_device_configuration or '
                   'keep_device_specific_external_acceleration can be set.')
            raise exceptions.InvalidInput(msg)
        params = dict(
            externalAccelerationType=external_acceleration_type,
            overrideDeviceConfiguration=override_device_configuration,
            keepDeviceSpecificExternalAcceleration=keep_device_ext_acceleration
        )

        r, response = self.send_post_request(self.base_action_url,
                                             action=action,
                                             entity=self.entity,
                                             entity_id=storage_pool_id,
                                             params=params)
        if r.status_code != requests.codes.ok:
            msg = ('Failed to set external acceleration type for PowerFlex '
                   '{entity} with id {_id}. Error: {response}'
                   .format(entity=self.entity, _id=storage_pool_id,
                           response=response))
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

        return self.get(entity_id=storage_pool_id)

    def set_media_type(self,
                       storage_pool_id,
                       media_type,
                       override_device_configuration=None):
        """Set media type for PowerFlex storage pool.

        :type storage_pool_id: str
        :param media_type: one of predefined attributes of MediaType
        :type media_type: str
        :type override_device_configuration: bool
        :rtype: dict
        """

        action = 'setMediaType'

        params = dict(
            mediaType=media_type,
            overrideDeviceConfiguration=override_device_configuration
        )

        r, response = self.send_post_request(self.base_action_url,
                                             action=action,
                                             entity=self.entity,
                                             entity_id=storage_pool_id,
                                             params=params)
        if r.status_code != requests.codes.ok:
            msg = ('Failed to set media type for PowerFlex {entity} '
                   'with id {_id}. Error: {response}'
                   .format(entity=self.entity, _id=storage_pool_id,
                           response=response))

            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

        return self.get(entity_id=storage_pool_id)

    def set_rebalance_enabled(self, storage_pool_id, rebalance_enabled):
        """Enable/disable rebalance for PowerFlex storage pool.

        :type storage_pool_id: str
        :type rebalance_enabled: str
        :rtype: dict
        """

        action = 'setRebalanceEnabled'

        params = dict(
            rebalanceEnabled=rebalance_enabled
        )

        r, response = self.send_post_request(self.base_action_url,
                                             action=action,
                                             entity=self.entity,
                                             entity_id=storage_pool_id,
                                             params=params)
        if r.status_code != requests.codes.ok:
            msg = ('Failed to enable/disable rebalance for PowerFlex {entity}'
                   ' with id {_id}. Error: {response}'
                   .format(entity=self.entity, _id=storage_pool_id,
                           response=response))
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

        return self.get(entity_id=storage_pool_id)

    def set_rebuild_enabled(self, storage_pool_id, rebuild_enabled):
        """Enable/disable rebuild for PowerFlex storage pool.

        :type storage_pool_id: str
        :type rebuild_enabled: bool
        :rtype: dict
        """

        action = 'setRebuildEnabled'

        params = dict(
            rebuildEnabled=rebuild_enabled
        )

        r, response = self.send_post_request(self.base_action_url,
                                             action=action,
                                             entity=self.entity,
                                             entity_id=storage_pool_id,
                                             params=params)
        if r.status_code != requests.codes.ok:
            msg = ('Failed to enable/disable rebuild for PowerFlex {entity} '
                   'with id {_id}. Error: {response}'
                   .format(entity=self.entity, _id=storage_pool_id,
                           response=response))
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

        return self.get(entity_id=storage_pool_id)

    def set_spare_percentage(self, storage_pool_id, spare_percentage):
        """Set spare percentage for PowerFlex storage pool.

        :type storage_pool_id: str
        :type spare_percentage: int
        :rtype: dict
        """

        action = 'setSparePercentage'

        params = dict(
            sparePercentage=spare_percentage
        )

        r, response = self.send_post_request(self.base_action_url,
                                             action=action,
                                             entity=self.entity,
                                             entity_id=storage_pool_id,
                                             params=params)
        if r.status_code != requests.codes.ok:
            msg = ('Failed to set spare percentage for PowerFlex {entity} '
                   'with id {_id}. Error: {response}'
                   .format(entity=self.entity, _id=storage_pool_id,
                           response=response))

            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

        return self.get(entity_id=storage_pool_id)

    def set_use_rfcache(self, storage_pool_id, use_rfcache):
        """Enable/disable Rfcache usage for PowerFlex storage pool.

        :type storage_pool_id: str
        :type use_rfcache: boold
        :rtype: dict
        """

        action = 'disableRfcache'
        if use_rfcache:
            action = 'enableRfcache'

        r, response = self.send_post_request(self.base_action_url,
                                             action=action,
                                             entity=self.entity,
                                             entity_id=storage_pool_id)
        if r.status_code != requests.codes.ok:
            msg = ('Failed to set Rfcache usage for PowerFlex {entity} '
                   'with id {_id}. Error: {response}'
                   .format(entity=self.entity, _id=storage_pool_id,
                           response=response))

            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

        return self.get(entity_id=storage_pool_id)

    def set_use_rmcache(self, storage_pool_id, use_rmcache):
        """Enable/disable Rmcache usage for PowerFlex storage pool.

        :type storage_pool_id: str
        :type use_rmcache: boold
        :rtype: dict
        """

        action = 'setUseRmcache'

        params = dict(
            useRmcache=use_rmcache
        )

        r, response = self.send_post_request(self.base_action_url,
                                             action=action,
                                             entity=self.entity,
                                             entity_id=storage_pool_id,
                                             params=params)
        if r.status_code != requests.codes.ok:
            msg = ('Failed to set Rmcache usage for PowerFlex {entity} '
                   'with id {_id}. Error: {response}'
                   .format(entity=self.entity, _id=storage_pool_id,
                           response=response))

            LOG.error(msg)

            raise exceptions.PowerFlexClientException(msg)

        return self.get(entity_id=storage_pool_id)

    def set_zero_padding_policy(self, storage_pool_id, zero_padding_enabled):
        """Enable/disable zero padding for PowerFlex storage pool.

        :type storage_pool_id: str
        :type zero_padding_enabled: bool
        :rtype: dict
        """

        action = 'setZeroPaddingPolicy'

        params = dict(
            zeroPadEnabled=zero_padding_enabled
        )

        r, response = self.send_post_request(self.base_action_url,
                                             action=action,
                                             entity=self.entity,
                                             entity_id=storage_pool_id,
                                             params=params)
        if r.status_code != requests.codes.ok:
            msg = ('Failed to set Zero Padding policy for PowerFlex {entity} '
                   'with id {_id}. Error: {response}'
                   .format(entity=self.entity, _id=storage_pool_id,
                           response=response))
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

        return self.get(entity_id=storage_pool_id)
