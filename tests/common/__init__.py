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

"""This module is used for the initialization of the test framework."""

# pylint: disable=too-many-instance-attributes,keyword-arg-before-vararg,broad-exception-raised,unused-argument

import collections
import copy
import contextlib
import json
import logging
from unittest import mock
from unittest import TestCase

import requests

import PyPowerFlex
from PyPowerFlex import utils


class MockResponse(requests.Response):
    """
    Mock HTTP Response.

    Defines http replies from mocked calls to do_request().
    """
    def __init__(self, content, status_code=200):
        """
        Initialize a MockResponse.

        Args:
            content (str or dict): The content of the response.
            status_code (int): The status code of the response.
        """
        super().__init__()
        self._content = content
        self.request = mock.MagicMock()
        self.status_code = status_code

    def json(self, **kwargs):
        """
        Return the content of the response as JSON.

        Args:
            **kwargs: Additional keyword arguments.

        Returns:
            dict: The content of the response.
        """
        return self._content

    @property
    def text(self):
        """
        Return the content of the response as text.

        Returns:
            str: The content of the response.
        """
        if not isinstance(self._content, bytes):
            return json.dumps(self._content)
        return super().text


class PyPowerFlexTestCase(TestCase):
    """
    Base test case for PyPowerFlex.

    Provides a mocked HTTP response for testing.
    """
    VERSION_API_PATH = '/version'

    @classmethod
    def version(cls, new_version):
        def decorator(subclass):
            subclass.DEFAULT_MOCK_RESPONSES = copy.deepcopy(cls.DEFAULT_MOCK_RESPONSES)
            subclass.DEFAULT_MOCK_RESPONSES[
                    cls.RESPONSE_MODE.Valid
                ][cls.VERSION_API_PATH] = new_version
            return subclass
        return decorator

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
    MOCK_RESPONSES = {}
    DEFAULT_MOCK_RESPONSES = {
        RESPONSE_MODE.Valid: {
            '/login': 'token',
            VERSION_API_PATH: '4.5',
            '/logout': '',
        },
        RESPONSE_MODE.Invalid: {
            VERSION_API_PATH: '2.5',
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
        """
        Set up the test case.

        Creates a PyPowerFlex client and sets up mocked HTTP responses.
        """
        self.gateway_address = '1.2.3.4'
        self.gateway_port = 443
        self.username = 'admin'
        self.password = 'admin'
        self.client = PyPowerFlex.PowerFlexClient(self.gateway_address,
                                                  self.gateway_port,
                                                  self.username,
                                                  self.password,
                                                  log_level=logging.DEBUG)
        requests.request = self.get_mock_response
        self.get_mock = self.mock_object(requests,
                                         'get',
                                         side_effect=self.get_mock_response)
        self.post_mock = self.mock_object(requests,
                                          'post',
                                          side_effect=self.get_mock_response)
        utils.is_version_3 = mock.MagicMock(return_value=True)

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
        """
        Context manager for setting the HTTP response mode.

        Args:
            mode: The HTTP response mode.

        Yields:
            None.
        """
        previous_response_mode, self.__http_response_mode = (
            self.__http_response_mode, mode
        )
        yield
        self.__http_response_mode = previous_response_mode

    def get_mock_response(self, url, request_url=None, mode=None, *args, **kwargs):
        """
        Get a mock HTTP response.

        Args:
            url (str): The URL of the request.
            request_url (str): The URL of the request.
            mode (str): The HTTP response mode.
            *args: Additional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            requests.Response: The mocked HTTP response.
        """
        if mode is None:
            mode = self.__http_response_mode

        api_path = url.split('/api')[1] if ('/api' in url) else request_url.split('/api')[1]
        try:
            if api_path == "/login":
                response = self.RESPONSE_MODE.Valid[0]
            elif api_path == "/logout":
                response = self.RESPONSE_MODE.Valid[2]
            else:
                response = self.MOCK_RESPONSES[mode][api_path]
        except KeyError as e:
            try:
                response = self.DEFAULT_MOCK_RESPONSES[mode][api_path]
            except KeyError:
                if mode == self.RESPONSE_MODE.BadStatus:
                    response = self.BAD_STATUS_RESPONSE
                else:
                    raise Exception(
                        f"Mock API Endpoint is not implemented: [{mode}]"
                        f"{api_path}"
                    ) from e
        if not isinstance(response, MockResponse):
            response = self._get_mock_response(response)

        response.request.url = url
        response.request.body = kwargs.get('data')
        return response

    def _get_mock_response(self, response):
        """
        Returns a MockResponse object based on the given response.

        Args:
            response (str): The response to be wrapped.

        Returns:
            MockResponse: The mock response object.
        """
        if "204" in str(response):
            return MockResponse(response, 204)
        return MockResponse(response, 200)
