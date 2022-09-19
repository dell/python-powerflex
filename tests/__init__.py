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

import collections
import contextlib
import json
import logging
from unittest import mock
from unittest import TestCase

import requests

import PyPowerFlex
from PyPowerFlex import utils


class MockResponse(requests.Response):
    """Mock HTTP Response.

    Defines http replies from mocked calls to do_request().
    """

    def __init__(self, content, status_code=200):
        super(MockResponse, self).__init__()

        self._content = content
        self.request = mock.MagicMock()
        self.status_code = status_code

    def json(self, **kwargs):
        return self._content

    @property
    def text(self):
        if not isinstance(self._content, bytes):
            return json.dumps(self._content)
        return super(MockResponse, self).text


class PyPowerFlexTestCase(TestCase):
    RESPONSE_MODE = (
        collections.namedtuple('RESPONSE_MODE', 'Valid Invalid BadStatus')
        (Valid='Valid', Invalid='Invalid', BadStatus='BadStatus')
    )
    BAD_STATUS_RESPONSE = MockResponse(
        {
            'errorCode': 500,
            'message': 'Test default bad status',
        }, 500
    )
    MOCK_RESPONSES = dict()
    DEFAULT_MOCK_RESPONSES = {
        RESPONSE_MODE.Valid: {
            '/login': 'token',
            '/version': '3.5',
            '/logout': '',
        },
        RESPONSE_MODE.Invalid: {
            '/version': '2.5',
        },
        RESPONSE_MODE.BadStatus: {
            '/login': MockResponse(
                {
                    'errorCode': 1,
                    'message': 'Test login bad status',
                }, 400
            ),
            '/version': MockResponse(
                {
                    'errorCode': 2,
                    'message': 'Test version bad status',
                }, 400
            ),
            '/logout': MockResponse(
                {
                    'errorCode': 3,
                    'message': 'Test logout bad status',
                }, 400
            )
        }
    }
    __http_response_mode = RESPONSE_MODE.Valid

    def setUp(self):
        self.gateway_address = '1.2.3.4'
        self.gateway_port = 443
        self.username = 'admin'
        self.password = 'admin'
        self.client = PyPowerFlex.PowerFlexClient(self.gateway_address,
                                                  self.gateway_port,
                                                  self.username,
                                                  self.password,
                                                  log_level=logging.DEBUG)
        self.get_mock = self.mock_object(requests,
                                         'get',
                                         side_effect=self.get_mock_response)
        self.post_mock = self.mock_object(requests,
                                          'post',
                                          side_effect=self.get_mock_response)
        utils.check_version = mock.MagicMock(return_value=False)

    def mock_object(self, obj, attr_name, *args, **kwargs):
        """Use python mock to mock an object attribute.

        Mocks the specified objects attribute with the given value.
        Automatically performs 'addCleanup' for the mock.
        """

        patcher = mock.patch.object(obj, attr_name, *args, **kwargs)
        result = patcher.start()
        self.addCleanup(patcher.stop)
        return result

    @contextlib.contextmanager
    def http_response_mode(self, mode):
        previous_response_mode, self.__http_response_mode = (
            self.__http_response_mode, mode
        )
        yield
        self.__http_response_mode = previous_response_mode

    def get_mock_response(self, url, mode=None, *args, **kwargs):
        if mode is None:
            mode = self.__http_response_mode
        api_path = url.split('/api')[1]
        try:
            if api_path == "/login":
                response = self.RESPONSE_MODE.Valid[0]
            elif api_path == "/logout":
                response = self.RESPONSE_MODE.Valid[2]
            else:
                response = self.MOCK_RESPONSES[mode][api_path]
        except KeyError:
            try:
                response = self.DEFAULT_MOCK_RESPONSES[mode][api_path]
            except KeyError:
                if mode == self.RESPONSE_MODE.BadStatus:
                    response = self.BAD_STATUS_RESPONSE
                else:
                    raise Exception(
                        'Mock API Endpoint is not implemented: [{}]{}'.format(
                            mode, api_path
                        )
                    )
        if not isinstance(response, MockResponse):
            response = MockResponse(response, 200)
        response.request.url = url
        response.request.body = kwargs.get('data')
        return response
