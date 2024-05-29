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

import json

from PyPowerFlex import exceptions
from PyPowerFlex import utils
import tests


class TestBaseClient(tests.PyPowerFlexTestCase):
    def setUp(self):
        super(TestBaseClient, self).setUp()
        self.fake_response = [
            {
                'first': 1,
                'second': 1024,
                'third': ['one', 'two']
            },
            {
                'first': 2,
                'second': 2048,
                'third': ['two', 'three']
            }
        ]

    def test_client_not_initialized(self):
        with self.assertRaises(exceptions.ClientNotInitialized):
            self.client.volume.get()

    def test_client_initialize(self):
        self.client.initialize()

    def test_client_initialize_required_params_not_set(self):
        self.client.configuration.gateway_address = None
        with self.assertRaises(exceptions.InvalidConfiguration):
            self.client.initialize()

    def test_client_initialize_api_version_not_supported(self):
        with self.http_response_mode(self.RESPONSE_MODE.Invalid):
            with self.assertRaises(exceptions.PowerFlexClientException):
                self.client.initialize()

    def test_utils_filter_response(self):
        filter_fields = {'second': 2048}
        result = utils.filter_response(self.fake_response, filter_fields)
        self.assertTrue(len(result) == 1)
        self.assertTrue(result[0]['second'] == 2048)

    def test_utils_filter_response_iterable_in_response(self):
        filter_fields = {'third': 'one'}
        result = utils.filter_response(self.fake_response, filter_fields)
        self.assertTrue(len(result) == 1)

    def test_utils_filter_response_iterable_filter_field(self):
        filter_fields = {'third': ['one', 'two']}
        result = utils.filter_response(self.fake_response, filter_fields)
        self.assertTrue(len(result) == 2)

    def test_utils_filter_response_iterable_filter_field_no_match(self):
        filter_fields = {'third': ['four', 'five']}
        result = utils.filter_response(self.fake_response, filter_fields)
        self.assertFalse(len(result))

    def test_utils_filter_response_invalid_field(self):
        filter_fields = {'not_found_in_response': True}
        result = utils.filter_response(self.fake_response, filter_fields)
        self.assertTrue(len(result) == 0)

    def test_utils_query_response_fields_list(self):
        fields = ('first',)
        result = utils.query_response_fields(self.fake_response, fields)
        self.assertTrue(all(map(lambda entity: len(entity) == 1, result)))
        self.assertTrue(all(map(lambda entity: entity['first'], result)))

    def test_utils_query_response_fields_dict(self):
        fields = ('first',)
        result = utils.query_response_fields(self.fake_response[0], fields)
        self.assertTrue(len(result) == 1)
        self.assertTrue(result['first'])

    def test_utils_query_response_fields_invalid_field(self):
        fields = ('not_found_in_response', 'first', 'second')
        with self.assertRaises(exceptions.FieldsNotFound):
            utils.query_response_fields(self.fake_response, fields)

    def test_utils_prepare_params(self):
        params = dict(first=1, second=True, third=None)
        prepared = json.loads(utils.prepare_params(params))
        self.assertNotIn('third', prepared)
        self.assertEqual('1', prepared['first'])
        self.assertEqual('True', prepared['second'])

    def test_utils_prepare_params_with_lists(self):
        params = dict(first=['second', 3, [4, True, {'fifth': 5}]])
        prepared = json.loads(utils.prepare_params(params))
        self.assertEqual(
            {'first': ['second', '3', ['4', 'True', {'fifth': 5}]]}, prepared
        )
