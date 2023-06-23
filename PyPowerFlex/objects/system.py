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

    def add_standby_mdm(self, mdm_ips, role, management_ips=None, port=None,
                        mdm_name=None, allow_multiple_ips=None, clean=None,
                        virtual_interface=None):
        """
        Add a standby MDM to the system.
        :param mdm_ips: List of ip addresses assigned to new MDM. It can
                        contain IPv4 addresses.
        :type mdm_ips: list[str]
        :param role: Role of the new MDM.
        :type role: str
        :param management_ips: List of IP addresses used to manage the MDM.
                               It can contain IPv4 addresses.
        :type management_ips: list[str]
        :param port: Port of new MDM. Default: 9011
        :type port: str
        :param mdm_name: Name of the new MDM.
        :type mdm_name: str
        :param allow_multiple_ips: Allow the added node to have a different
                                   number of IPs from the primary node.
        :type allow_multiple_ips: str
        :param clean: Clean a previous MDM configuration.
        :type clean: str
        :param virtual_interface: List of NIC interfaces that will be used
                                  for virtual IP address.
        :type virtual_interface: list[str]
        :return: ID of new standby MDM.
        :rtype: dict
        """
        action = 'addStandbyMdm'
        params = dict(
            ips=mdm_ips,
            role=role,
            managementIps=management_ips,
            name=mdm_name,
            port=port,
            allowAsymmetricIps=allow_multiple_ips,
            forceClean=clean,
            virtIpIntfs=virtual_interface
        )

        r, response = self.send_post_request(self.base_object_url,
                                             action=action,
                                             entity=self.entity,
                                             params=params)
        if r.status_code != requests.codes.ok:
            msg = ('Failed to add standBy MDM on PowerFlex {entity}. '
                   'Error: {response}'.format(entity=self.entity,
                                              response=response))
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

        return response

    def remove_standby_mdm(self, mdm_id):
        """
        Remove a standby MDM from the system.
        :param mdm_id: ID of MDM to be removed.
        :type mdm_id: str
        :return: None
        """
        action = 'removeStandbyMdm'
        params = dict(
            id=mdm_id
        )

        r, response = self.send_mdm_cluster_post_request(self.base_object_url,
                                                         action=action,
                                                         entity=self.entity,
                                                         params=params)
        if r.status_code != requests.codes.ok and response is not None:
            msg = ('Failed to remove standBy MDM from PowerFlex {entity}. '
                   'Error: {response}.'.format(entity=self.entity,
                                               response=response))
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

        return True

    def get_mdm_cluster_details(self):
        """
        Get the MDM cluster details
        :return: MDM cluster details
        :rtype: dict
        """

        r, response = self.send_post_request(self.query_mdm_cluster_url,
                                             entity=self.entity)
        if r.status_code != requests.codes.ok:
            msg = ('Failed to get MDM cluster details on PowerFlex {entity}. '
                   'Error: {response}'.format(entity=self.entity,
                                              response=response))
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

        return response

    def get_gateway_configuration_details(self):
        """
        Get the gateway configuration details
        :return: Gateway configuration details
        :rtype: dict
        """

        r, response = self.send_get_request('/Configuration')
        if r.status_code != requests.codes.ok:
            msg = ('Failed to get gateway configuration details on PowerFlex {entity}. '
                   'Error: {response}'.format(entity=self.entity,
                                              response=response))
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

        return response

    def change_mdm_ownership(self, mdm_id):
        """
        Change MDM cluster ownership from current master MDM to different MDM.

        :param mdm_id: ID of New Manager MDM
        :type mdm_id: str
        :return: None
        :rtype: dict
        """
        action = 'changeMdmOwnership'
        params = dict(
            id=mdm_id
        )

        r, response = self.send_post_request(self.base_object_url,
                                             action=action,
                                             entity=self.entity,
                                             params=params)
        if r.status_code != requests.codes.ok:
            msg = ('Failed to change ownership on PowerFlex {entity}. '
                   'Error: {response}'.format(entity=self.entity,
                                              response=response))
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

    def set_cluster_mdm_performance_profile(self, performance_profile):
        """
        Set the Cluster MDMs performance profile.

        :param performance_profile: Define the performance profile of MDMs.
        :type performance_profile: str
        :return: None
        :rtype: dict
        """
        action = 'setMdmPerformanceParameters'
        params = dict(
            perfProfile=performance_profile
        )

        r, response = self.send_post_request(self.base_object_url,
                                             action=action,
                                             entity=self.entity,
                                             params=params)
        if r.status_code != requests.codes.ok:
            msg = ('Failed to set performance profile of MDMs on PowerFlex '
                   '{entity}. Error: {response}'.format(entity=self.entity,
                                                        response=response))
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

        return response

    def rename_mdm(self, mdm_id, mdm_new_name):
        """
        Set the Cluster MDMs performance profile.

        :param mdm_id: ID of MDM.
        :type mdm_id: str
        :param mdm_new_name: new name of MDM.
        :type mdm_new_name: str
        :return: None
        :rtype: dict
        """
        action = 'renameMdm'
        params = dict(
            id=mdm_id,
            newName=mdm_new_name
        )

        r, response = self.send_post_request(self.base_object_url,
                                             action=action,
                                             entity=self.entity,
                                             params=params)
        if r.status_code != requests.codes.ok:
            msg = ('Failed to rename the MDM on PowerFlex {entity}. Error: '
                   '{response}'.format(entity=self.entity, response=response))
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

        return response

    def modify_virtual_ip_interface(self, mdm_id, virtual_ip_interfaces=None,
                                    clear_interfaces=None):
        """
        Set the Cluster MDMs performance profile.

        :param mdm_id: ID of MDM.
        :type mdm_id: str
        :param virtual_ip_interfaces: List of interface names to be used for
                                      the MDM virtual IPs.
        :type virtual_ip_interfaces: list[str]
        :param clear_interfaces: Clear all virtual IP interfaces.
        :type mdm_id: str
        :return: None
        :rtype: dict
        """
        action = 'modifyVirtualIpInterfaces'
        if virtual_ip_interfaces is not None:
            params = dict(
                id=mdm_id,
                virtIpIntfs=virtual_ip_interfaces
            )
        else:
            params = dict(
                id=mdm_id,
                clear=clear_interfaces
            )

        r, response = self.send_post_request(self.base_object_url,
                                             action=action,
                                             entity=self.entity,
                                             params=params)
        if r.status_code != requests.codes.ok:
            msg = ('Failed to modify virtual IP interface on PowerFlex '
                   '{entity}. Error: {response}'.format(entity=self.entity,
                                                        response=response))
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

        return response

    def switch_cluster_mode(self, cluster_mode, add_secondary=None,
                            remove_secondary=None, add_tb=None, remove_tb=None):
        """
        Switch cluster mode.

        :param cluster_mode: New mode of MDM cluster
        :type cluster_mode: str
        :param add_secondary: List of secondary MDM IDs that will be part of
                              the cluster. A maximum of two IDs are allowed.
        :type add_secondary: list[str]
        :param remove_secondary: List of secondary MDM IDs that will be removed
                                 from the cluster.
        :type remove_secondary: list[str]
        :param add_tb: List of TieBreaker MDM IDs that will be part of the
                       cluster.
        :type add_tb: list[str]
        :param remove_tb: List of TieBreaker MDM IDs that will be removed
                          from the cluster.
        :type remove_tb: list[str]
        :return: None
        """
        action = 'switchClusterMode'
        params = dict(
            mode=cluster_mode,
            addSlaveMdmIdList=add_secondary,
            addTBIdList=add_tb,
            removeSlaveMdmIdList=remove_secondary,
            removeTBIdList=remove_tb
        )

        r, response = self.send_mdm_cluster_post_request(self.base_object_url,
                                                         action=action,
                                                         entity=self.entity,
                                                         params=params)
        if r.status_code != requests.codes.ok and response is not None:
            msg = ('Failed to switch MDM cluster mode PowerFlex {entity}. '
                   'Error: {response}.'.format(entity=self.entity,
                                               response=response))
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

        return True
