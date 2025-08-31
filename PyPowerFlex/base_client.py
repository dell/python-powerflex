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

"""This module is the base client of the PowerFlex APIs."""

# pylint: disable=no-member,import-error,broad-exception-raised

import logging

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from PyPowerFlex import exceptions
from PyPowerFlex import utils

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
LOG = logging.getLogger(__name__)


class Request:
    """
    This class contains the methods for making requests to the PowerFlex API.
    """
    GET = "get"
    POST = "post"
    PUT = "put"
    DELETE = "delete"

    def __init__(self, token, configuration):
        self.token = token
        self.configuration = configuration
        self.__refresh_token = None

    @property
    def base_url(self):
        """
        Get the base URL for the PowerFlex API.

        Returns:
            str: The base URL.
        """
        return f'https://{self.configuration.gateway_address}:{self.configuration.gateway_port}/api'

    @property
    def auth_url(self):
        """
        Get the authentication URL for the PowerFlex API.

        Returns:
            str: The authentication URL.
        """
        gateway_address = self.configuration.gateway_address
        port = self.configuration.gateway_port
        return (
            f"https://{gateway_address}:{port}/rest/auth"
        )

    @property
    def headers(self):
        """
        Get the headers for the PowerFlex API.

        Returns:
            dict: The headers.
        """
        return {'content-type': 'application/json'}

    @property
    def verify_certificate(self):
        """
        Get the verification status of the certificate for the PowerFlex API.

        Returns:
            bool: The verification status.
        """
        verify_certificate = self.configuration.verify_certificate
        if (
                self.configuration.verify_certificate
                and self.configuration.certificate_path
        ):
            verify_certificate = self.configuration.certificate_path
        return verify_certificate

    def get_auth_headers(self, request_type=None):
        """
        Get the authentication headers for the PowerFlex API.

        Args:
            request_type (str): The type of the request.

        Returns:
            dict: The authentication headers.
        """
        if request_type == self.GET:
            return {'Authorization': f'Bearer {self.token.get()}'}
        return {
            'Authorization': f'Bearer {self.token.get()}',
            'content-type': 'application/json'
        }

    def send_request(self, method, url, params=None, use_base_url=True, **url_params):
        """
        Send a request to the PowerFlex API.

        Args:
            method (str): The HTTP method.
            url (str): The URL.
            use_base_url (bool, optional): Whether to use the base URL. Defaults to True.
            params (dict): The parameters.
            url_params (dict): The URL parameters.

        Returns:
            Response: The response object.
        """
        params = params or {}
        use_base_url = True if use_base_url is None else use_base_url
        if use_base_url:
            request_url = f"{self.base_url}{url.format(**url_params)}"
        else:
            request_url = f"{self.base_url.removesuffix('/api')}{url.format(**url_params)}"

        version = self.login()
        request_params = {
            'headers': self.get_auth_headers(method),
            'verify': self.verify_certificate,
            'timeout': self.configuration.timeout
        }
        if utils.is_version_3(version):
            request_params['auth'] = (
                self.configuration.username, self.token.get())
            del request_params['headers']['Authorization']

        if method in [self.PUT, self.POST]:
            request_params['data'] = utils.prepare_params(params)
        response = requests.request(method, request_url, **request_params)
        self.logout(version)
        return response

    def send_get_request(self, url, params=None, **url_params):
        """
        Send a GET request to the PowerFlex API.

        Args:
            url (str): The URL.
            params (dict): The parameters.
            url_params (dict): The URL parameters.

        Returns:
            tuple: The response object and the response content.
        """
        response = self.send_request(self.GET, url, params, **url_params)
        return response, response.json()

    def send_post_request(self, url, use_base_url=True, params=None, **url_params):
        """
        Send a POST request to the PowerFlex API.

        Args:
            url (str): The URL.
            use_base_url (bool, optional): Whether to use the base URL. Defaults to True.
            params (dict): The parameters.
            url_params (dict): The URL parameters.

        Returns:
            tuple: The response object and the response content.
        """
        response = self.send_request(
            self.POST, url, params, use_base_url, **url_params)
        return response, response.json()

    def send_put_request(self, url, params=None, **url_params):
        """
        Send a PUT request to the PowerFlex API.

        Args:
            url (str): The URL.
            params (dict): The parameters.
            url_params (dict): The URL parameters.

        Returns:
            tuple: The response object and the response content.
        """
        response = self.send_request(self.PUT, url, params, **url_params)
        return response, response.json()

    def send_delete_request(self, url, params=None, **url_params):
        """
        Send a DELETE request.

        Args:
            url (str): The URL for the request.
            params (dict, optional): The parameters for the request. Defaults to None.

        Returns:
            The response from the request.
        """
        return self.send_request(self.DELETE, url, params, **url_params)

    def send_mdm_cluster_post_request(self, url, params=None, **url_params):
        """
        Send a POST request for the MDM cluster.

        Args:
            url (str): The URL for the request.
            params (dict, optional): The parameters for the request. Defaults to None.

        Returns:
            tuple: A tuple containing the response and the JSON content of the response.
        """
        if params is None:
            params = {}
        response = None
        version = self.login()
        request_url = self.base_url + url.format(**url_params)
        r = requests.post(request_url,
                          auth=(
                              self.configuration.username,
                              self.token.get()
                          ),
                          headers=self.headers,
                          data=utils.prepare_params(params),
                          verify=self.verify_certificate,
                          timeout=self.configuration.timeout)

        if r.content != b'':
            response = r.json()
        self.logout(version)
        return r, response

    def login(self):
        """
        Perform login based on the API version.

        Returns:
            str: The API version.
        """
        version = self.get_api_version()
        if utils.is_version_3(version=version):
            self._login()
        else:
            self._appliance_login()
        return version

    def logout(self, version):
        """
        Perform logout based on the API version.
        """
        if utils.is_version_3(version=version):
            self._logout()
        else:
            self._appliance_logout()

    def get_api_version(self):
        """
        Get the current API version.

        Returns:
            dict: The JSON response containing the API version.
        """
        request_url = self.base_url + '/version'
        self._login()
        r = requests.get(request_url,
                         auth=(
                             self.configuration.username,
                             self.token.get()),
                         verify=self.verify_certificate,
                         timeout=self.configuration.timeout)
        response = r.json()
        return response

    def _appliance_login(self):
        """
        Perform login for API version 4.0 and above.
        """
        request_url = self.auth_url + '/login'
        payload = {
            "username": f"{self.configuration.username}",
            "password": f"{self.configuration.password}"
        }
        r = requests.post(request_url, headers=self.headers, json=payload,
                          verify=self.verify_certificate,
                          timeout=self.configuration.timeout
                          )
        if r.status_code != requests.codes.ok:
            exc = exceptions.PowerFlexFailQuerying('token')
            LOG.error(exc.message)
            raise exc
        response = r.json()
        token = response['access_token']
        self.token.set(token)
        self.__refresh_token = response['refresh_token']

    def _appliance_logout(self):
        """
        Perform logout for API version 4.0 and above.
        """
        request_url = self.auth_url + '/logout'
        data = {'refresh_token': f'{self.__refresh_token}'}
        r = requests.post(
            request_url,
            headers=self.get_auth_headers(),
            json=data,
            verify=self.verify_certificate,
            timeout=self.configuration.timeout)

        if r.status_code != requests.codes.no_content:
            exc = exceptions.PowerFlexFailQuerying('token')
            LOG.error(exc.message)
            raise exc
        self.token.set("")
        self.__refresh_token = None

    def _login(self):
        """
        Perform login for API version below 4.0.
        """
        request_url = self.base_url + '/login'
        try:
            r = requests.get(request_url,
                             auth=(
                                 self.configuration.username,
                                 self.configuration.password
                             ),
                             verify=self.verify_certificate,
                             timeout=self.configuration.timeout)
            r.raise_for_status()
            token = r.json()
            self.token.set(token)
        except requests.exceptions.RequestException as e:
            error_msg = (
                f'Login failed with error: {e.response.content}'
                if e.response
                else f'Login failed with error: {str(e)}'
            )
            LOG.error(error_msg)
            raise Exception(error_msg) from e

    def _logout(self):
        """
        Perform logout for API version below 4.0.
        """
        token = self.token.get()

        if token:
            request_url = self.base_url + '/logout'
            r = requests.get(request_url,
                             auth=(
                                 self.configuration.username,
                                 token
                             ),
                             verify=self.verify_certificate,
                             timeout=self.configuration.timeout)
            if r.status_code != requests.codes.ok:
                exc = exceptions.PowerFlexFailQuerying('token')
                LOG.error(exc.message)
                raise exc
            self.token.set("")


class EntityRequest(Request):
    """
    Base class for entity requests.
    """
    base_action_url = '/instances/{entity}::{entity_id}/action/{action}'
    base_entity_url = '/instances/{entity}::{entity_id}'
    base_entity_list_or_create_url = '/types/{entity}/instances'
    base_relationship_url = base_entity_url + '/relationships/{related}'
    base_object_url = '/instances/{entity}/action/{action}'
    base_type_special_action_url = '/types/{entity}/instances/action/{action}'
    query_mdm_cluster_url = '/instances/{entity}/queryMdmCluster'
    list_statistics_url = '/types/{entity}/instances/action/{action}'
    metrics_query_url = '/dtapi/rest/v1/metrics/query'
    service_template_url = '/V1/ServiceTemplate'
    managed_device_url = '/V1/ManagedDevice'
    deployment_url = '/V1/Deployment'
    firmware_repository_url = '/V1/FirmwareRepository'
    pfmp_version_url = '/v1/corelcm/status'
    entity_name = None

    @property
    def entity(self):
        """
        Returns the entity name.
        """
        return self.entity_name or self.__class__.__name__

    def _create_entity(self, params=None):
        """
        Creates an entity.

        Args:
            params (dict, optional): Parameters for the entity.

        Returns:
            dict: The created entity.

        Raises:
            PowerFlexFailCreating: If the entity fails to be created.
        """
        r, response = self.send_post_request(
            self.base_entity_list_or_create_url,
            entity=self.entity,
            params=params
        )
        if r.status_code != requests.codes.ok:
            exc = exceptions.PowerFlexFailCreating(self.entity, response)
            LOG.error(exc.message)
            raise exc

        entity_id = response['id']
        return self.get(entity_id=entity_id)

    def _delete_entity(self, entity_id, params=None):
        """
        Deletes an entity.

        Args:
            entity_id (str): The ID of the entity.
            params (dict, optional): Parameters for the entity.

        Returns:
            dict: The response from the API.

        Raises:
            PowerFlexFailDeleting: If the entity fails to be deleted.
        """
        action = 'remove' + self.entity

        r, response = self.send_post_request(self.base_action_url,
                                             action=action,
                                             entity=self.entity,
                                             entity_id=entity_id,
                                             params=params)
        if r.status_code != requests.codes.ok:
            exc = exceptions.PowerFlexFailDeleting(self.entity, entity_id,
                                                   response)
            LOG.error(exc.message)
            raise exc
        return response

    def _rename_entity(self, action, entity_id, params=None):
        """
        Renames an entity.

        Args:
            action (str): The action to perform.
            entity_id (str): The ID of the entity.
            params (dict, optional): Parameters for the entity.

        Returns:
            dict: The response from the API.

        Raises:
            PowerFlexFailRenaming: If the entity fails to be renamed.
        """
        r, response = self.send_post_request(self.base_action_url,
                                             action=action,
                                             entity=self.entity,
                                             entity_id=entity_id,
                                             params=params)
        if r.status_code != requests.codes.ok:
            exc = exceptions.PowerFlexFailRenaming(self.entity, entity_id,
                                                   response)
            LOG.error(exc.message)
            raise exc
        return response

    def get(self, entity_id=None, filter_fields=None, fields=None):
        """
        Gets an entity.

        Args:
            entity_id (str, optional): The ID of the entity.
            filter_fields (dict, optional): Fields to filter.
            fields (dict, optional): Fields to query.

        Returns:
            dict: The entity.

        Raises:
            PowerFlexFailQuerying: If the entity fails to be queried.
        """
        url = self.base_entity_list_or_create_url
        url_params = {'entity': self.entity}

        if entity_id:
            url = self.base_entity_url
            url_params['entity_id'] = entity_id
            if filter_fields:
                msg = 'Can not apply filtering while querying entity by id.'
                raise exceptions.InvalidInput(msg)

        r, response = self.send_get_request(url, **url_params)
        if r.status_code != requests.codes.ok:
            exc = exceptions.PowerFlexFailQuerying(self.entity, entity_id,
                                                   response)
            LOG.error(exc.message)
            raise exc
        if filter_fields:
            response = utils.filter_response(response, filter_fields)
        if fields:
            response = utils.query_response_fields(response, fields)
        return response

    def get_related(self, entity_id, related, filter_fields=None,
                    fields=None):
        """
        Gets related entities.

        Args:
            entity_id (str): The ID of the entity.
            related (str): The related entity.
            filter_fields (dict, optional): Fields to filter.
            fields (dict, optional): Fields to query.

        Returns:
            dict: The related entities.

        Raises:
            PowerFlexClientException: If the related entities fail to be queried.
        """
        url_params = {
            "entity": self.entity,
            "entity_id": entity_id,
            "related": related
        }

        r, response = self.send_get_request(self.base_relationship_url,
                                            **url_params)
        if r.status_code != requests.codes.ok:
            msg = (
                f"Failed to query related {related} entities for PowerFlex "
                f"{self.entity} with id {entity_id}. Error: {response}"
            )
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)
        if filter_fields:
            response = utils.filter_response(response, filter_fields)
        if fields:
            response = utils.query_response_fields(response, fields)
        return response

    def _perform_entity_operation_based_on_action(
            self,
            entity_id,
            action,
            params=None,
            add_entity=True,
            **url_params):
        """
        Perform a specific action on an entity.

        Args:
            entity_id (str): The ID of the entity.
            action (str): The action to perform.
            params (dict, optional): Additional parameters.
            add_entity (bool, optional): Whether to add the entity to the action.
            **url_params: Additional URL parameters.

        Raises:
            exceptions.PowerFlexFailEntityOperation: If the entity operation fails.

        Returns:
            dict: The response from the API.
        """
        if add_entity:
            action = action + self.entity

        r, response = self.send_post_request(self.base_action_url,
                                             action=action,
                                             entity=self.entity,
                                             entity_id=entity_id,
                                             params=params,
                                             **url_params)
        if r.status_code != requests.codes.ok:
            exc = exceptions.PowerFlexFailEntityOperation(
                self.entity, entity_id, action, response)
            LOG.error(exc.message)
            raise exc
        return response

    def _query_selected_statistics(self, action, params=None):
        """
        Query the selected statistics.

        Args:
            action (str): The action to perform.
            params (dict, optional): Additional parameters.

        Raises:
            exceptions.PowerFlexFailQuerying: If the query fails.

        Returns:
            dict: The response from the API.
        """
        r, response = self.send_post_request(self.base_type_special_action_url,
                                             action=action,
                                             entity=self.entity,
                                             params=params)
        if r.status_code != requests.codes.ok:
            exc = exceptions.PowerFlexFailQuerying(self.entity,
                                                   response=response,
                                                   entity_id=params["ids"]
                                                   if "ids" in params
                                                   else "all IDs"
                                                   if "allIds" in params
                                                   else None)
            LOG.error(exc.message)
            raise exc
        return response

    def query_metrics(self, resource_type, ids=None, metrics=None):
        """Query PowerFlex resource metrics.

        :param resource_type: str
        :param ids: list
        :param metrics: list
        :return: dict
        """

        params = {
            'resource_type': resource_type
        }
        if ids is not None:
            params['ids'] = ids
        if metrics is not None:
            params['metrics'] = metrics

        r, response = self.send_post_request(self.metrics_query_url,
                                             use_base_url=False,
                                             params=params)
        if r.status_code != requests.codes.ok:
            msg = (
                f"Failed to query {resource_type} statistics. "
                f"Error: {response}"
            )
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

        return response
