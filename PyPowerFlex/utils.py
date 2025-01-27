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

"""This module contains the utils used in the code."""

import json
import logging
import numbers
import sys

from PyPowerFlex import exceptions

def init_logger(log_level):
    """Initialize logger for PowerFlex client.

    :param log_level: logging level (e. g. logging.DEBUG)
    :type log_level: int
    :rtype: None
    """

    logging.basicConfig(
        stream=sys.stdout,
        level=log_level or logging.ERROR,
        format='[%(levelname)s] %(asctime)s '
               '%(name)s:%(funcName)s:%(lineno)s: %(message)s'
    )


def filter_response(response, filter_fields):
    """Filter PowerFlex API response by fields provided in `filter_fields`.

    Supports only flat filtering. Case-sensitive.

    :param response: PowerFlex API response
    :param filter_fields: key-value pairs of filter field and its value
    :type filter_fields: dict
    :return: filtered response
    :rtype: list
    """

    def filter_func(obj):
        for filter_key, filter_value in filter_fields.items():
            try:
                response_value = obj[filter_key]
                response_value, filter_value = map(
                    lambda value: [value]
                    if not isinstance(value, (list, tuple))
                    else value,
                    [response_value, filter_value])
                if not set(response_value).intersection(filter_value):
                    return False
            except (KeyError, TypeError):
                return False
        return True

    return list(filter(filter_func, response))


def query_response_fields(response, fields):
    """Extract specified fields from PowerFlex API response.

    :param response: PowerFlex API response
    :param fields: fields to extract
    :type fields: list | tuple
    :return: response containing only specified fields
    :rtype: list | dict
    """

    def query_entity_fields(entity):
        entity_fields = {}
        fields_not_found = []
        for field in fields:
            try:
                entity_fields[field] = entity[field]
            except (KeyError, TypeError):
                fields_not_found.append(field)
        if fields_not_found:
            msg = (
                'The following fields are not found in response: '
                f'{", ".join(fields_not_found)}.'
            )
            raise exceptions.FieldsNotFound(msg)
        return entity_fields

    if isinstance(response, list):
        return list(map(query_entity_fields, response))
    if isinstance(response, dict):
        return query_entity_fields(response)
    return None


def convert(param):
    """
    Convert parameters to appropriate types.

    :param param: request parameters
    :return: converted parameters
    """
    if isinstance(param, list):
        return [convert(item) for item in param]
    if isinstance(param, (numbers.Number, bool)):
        # Convert numbers and boolean to string.
        return str(param)
    # Other types are not converted.
    return param


def prepare_params(params, dump=True):
    """Prepare request parameters before sending.

    :param params: request parameters
    :type params: dict
    :param dump: dump params to json
    :return: prepared parameters
    """

    if not isinstance(params, dict):
        return params

    prepared = {}
    for name, value in params.items():
        if value is not None:
            prepared[name] = convert(value)
    if dump:
        return json.dumps(prepared)
    return prepared


def is_version_3(version):
    """ Check the API version.

    :param version: Specifies the current API version
    :return: True if API version is lesser than 4.0
    :rtype: bool
    """
    appliance_version = "4.0"
    if version < appliance_version:
        return True
    return False


def build_uri_with_params(uri, **url_params):
    """
    Build the URI with query parameters.

    :param uri: base URI
    :param url_params: query parameters
    :return: URI with query parameters
    """
    query_params = [
        f"{key}={item}" if isinstance(
            value,
            list) else f"{key}={value}" for key,
        value in url_params.items() for item in (
            value if isinstance(
                value,
                list) else [value]) if item is not None]
    if query_params:
        uri += '?' + '&'.join(query_params)
    return uri
