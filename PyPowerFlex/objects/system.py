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
import re

import requests

from PyPowerFlex import base_client
from PyPowerFlex import exceptions
from PyPowerFlex import utils


LOG = logging.getLogger(__name__)


class SnapshotDef(dict):
    """PowerFlex definition of snapshot to create.

    JSON-serializable, should be used as `snapshot_defs` list item
    in `System.snapshot_volumes` method.
    """

    def __init__(self, volume_id, name=None):
        """Initialize SnapshotDef object.

        :type volume_id: str
        :type name: str
        """

        params = utils.prepare_params(
            {
                'volumeId': volume_id,
                'snapshotName': name,
            },
            dump=False
        )
        super(SnapshotDef, self).__init__(**params)


class System(base_client.EntityRequest):
    def __init__(self, token, configuration):
        self.__api_version = None
        super(System, self).__init__(token, configuration)

    def api_version(self, cached=True):
        """Get PowerFlex API version.

        :param cached: get version from cache or send API response
        :type cached: bool
        :rtype: str
        """

        url = '/version'

        if not self.__api_version or not cached:
            r, response = self.send_get_request(url)
            if r.status_code != requests.codes.ok:
                exc = exceptions.PowerFlexFailQuerying('API version')
                LOG.error(exc.message)
                raise exc
            pattern = re.compile(r'^\d+(\.\d+)*$')
            if not pattern.match(response):
                msg = (
                    'Failed to query PowerFlex API version. Invalid version '
                    'format: {response}.'.format(response=r.text)
                )
                LOG.error(msg)
                raise exceptions.PowerFlexClientException(msg)
            self.__api_version = response
        return self.__api_version

    def remove_cg_snapshots(self, system_id, cg_id, allow_ext_managed=None):
        """Remove PowerFlex ConsistencyGroup snapshots.

        :type system_id: str
        :type cg_id: str
        :type allow_ext_managed: bool
        :rtype: dict
        """

        action = 'removeConsistencyGroupSnapshots'

        params = dict(
            snapGroupId=cg_id,
            allowOnExtManagedVol=allow_ext_managed
        )

        r, response = self.send_post_request(self.base_action_url,
                                             action=action,
                                             entity=self.entity,
                                             entity_id=system_id,
                                             params=params)
        if r.status_code != requests.codes.ok:
            msg = ('Failed to remove consistency group snapshots from '
                   'PowerFlex {entity} with id {_id}. '
                   'Error: {response}'.format(entity=self.entity,
                                              _id=system_id,
                                              response=response))
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

        return response

    def snapshot_volumes(self,
                         system_id,
                         snapshot_defs,
                         access_mode=None,
                         retention_period=None,
                         allow_ext_managed=None):
        """Create snapshots of PowerFlex volumes.

        :type retention_period: str
        :type access_mode: str
        :type system_id: str
        :type snapshot_defs: list[dict]
        :type allow_ext_managed: bool
        :rtype: dict
        """

        action = 'snapshotVolumes'

        params = dict(
            snapshotDefs=snapshot_defs,
            allowOnExtManagedVol=allow_ext_managed,
            accessModeLimit=access_mode,
            retentionPeriodInMin=retention_period
        )

        r, response = self.send_post_request(self.base_action_url,
                                             action=action,
                                             entity=self.entity,
                                             entity_id=system_id,
                                             params=params)
        if r.status_code != requests.codes.ok:
            msg = ('Failed to snapshot volumes on PowerFlex {entity} '
                   'with id {_id}.'
                   ' Error: {response}'.format(entity=self.entity,
                                               _id=system_id,
                                               response=response))
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

        return response
