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
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from PyPowerFlex import exceptions
from PyPowerFlex import utils


requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
LOG = logging.getLogger(__name__)


class Request:
    def __init__(self, token, configuration):
        self.token = token
        self.configuration = configuration

    @property
    def base_url(self):
        return 'https://{address}:{port}/api'.format(
            address=self.configuration.gateway_address,
            port=self.configuration.gateway_port
        )

    @property
    def headers(self):
        return {'content-type': 'application/json'}

    @property
    def verify_certificate(self):
        verify_certificate = self.configuration.verify_certificate
        if (
                self.configuration.verify_certificate
                and self.configuration.certificate_path
        ):
            verify_certificate = self.configuration.certificate_path
        return verify_certificate

    def send_get_request(self, url, **url_params):
        request_url = self.base_url + url.format(**url_params)
        self._login()
        r = requests.get(request_url,
                         auth=(
                             self.configuration.username,
                             self.token.get()
                         ),
                         verify=self.verify_certificate,
                         timeout=self.configuration.timeout)
        self._logout()
        response = r.json()
        return r, response

    def send_post_request(self, url, params=None, **url_params):
        if params is None:
            params = dict()
        self._login()
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
        response = r.json()
        self._logout()
        return r, response

    def _login(self):
        request_url = self.base_url + '/login'

        r = requests.get(request_url,
                         auth=(
                             self.configuration.username,
                             self.configuration.password
                         ),
                         verify=self.verify_certificate,
                         timeout=self.configuration.timeout)
        if r.status_code != requests.codes.ok:
            exc = exceptions.PowerFlexFailQuerying('token')
            LOG.error(exc.message)
            raise exc
        token = r.json()
        self.token.set(token)

    def _logout(self):
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
    base_action_url = '/instances/{entity}::{entity_id}/action/{action}'
    base_entity_url = '/instances/{entity}::{entity_id}'
    base_entity_list_or_create_url = '/types/{entity}/instances'
    base_relationship_url = base_entity_url + '/relationships/{related}'
    entity_name = None

    @property
    def entity(self):
        return self.entity_name or self.__class__.__name__

    def _create_entity(self, params=None):
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

    def _rename_entity(self, action, entity_id, params=None):
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

        return self.get(entity_id=entity_id)

    def get(self, entity_id=None, filter_fields=None, fields=None):
        url = self.base_entity_list_or_create_url
        url_params = dict(entity=self.entity)

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

    def get_related(self, entity_id, related, filter_fields=None, fields=None):
        url_params = dict(
            entity=self.entity,
            entity_id=entity_id,
            related=related
        )

        r, response = self.send_get_request(self.base_relationship_url,
                                            **url_params)
        if r.status_code != requests.codes.ok:
            msg = (
                'Failed to query related {related} entities for PowerFlex '
                '{entity} with id {_id}.'
                ' Error: {response}'.format(related=related,
                                            entity=self.entity,
                                            _id=entity_id,
                                            response=response)
            )
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)
        if filter_fields:
            response = utils.filter_response(response, filter_fields)
        if fields:
            response = utils.query_response_fields(response, fields)
        return response
