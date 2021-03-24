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

from PyPowerFlex import base_client


LOG = logging.getLogger(__name__)


class Sdc(base_client.EntityRequest):
    def delete(self, sdc_id):
        """Remove PowerFlex SDC.

        :type sdc_id: str
        :rtype: None
        """

        return self._delete_entity(sdc_id)

    def get_mapped_volumes(self, sdc_id, filter_fields=None, fields=None):
        """Get PowerFlex volumes mapped to SDC.

        :type sdc_id: str
        :type filter_fields: dict
        :type fields: list|tuple
        :rtype: list[dict]
        """

        return self.get_related(sdc_id, 'Volume', filter_fields, fields)

    def rename(self, sdc_id, name):
        """Rename PowerFlex SDC.

        :type sdc_id: str
        :type name: str
        :rtype: dict
        """

        action = 'setSdcName'

        params = dict(
            sdcName=name
        )

        return self._rename_entity(action, sdc_id, params)

    def set_performance_profile(self, sdc_id, perf_profile):
        """Apply a performance profile to the specified SDC.

        :type sdc_id: str
        :type perf_profile: str
        :rtype: dict
        """

        action = 'setSdcPerformanceParameters'

        params = dict(
            perfProfile=perf_profile
        )

        r, response = self.send_post_request(self.base_action_url, action, sdc_id, params)

        if r.status_code != requests.codes.ok:
            msg = ('Failed to set Performance Profile on '
                   'PowerFlex {entity} with id {_id} '
                   '. Error: {response}'.format(entity=self.entity,
                                                _id=sdc_id,
                                                response=response))
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

        return self.get(entity_id=sdc_id)