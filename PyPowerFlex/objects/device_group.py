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

"""Module for interacting with protection domain APIs."""

# pylint: disable=too-few-public-methods,no-member,too-many-arguments,too-many-positional-arguments,duplicate-code

import logging
import requests

from marshmallow import fields, validate
from PyPowerFlex import base_client, exceptions


LOG = logging.getLogger(__name__)


class DeviceGroupSchema(base_client.BaseSchema):
    id = fields.Str(
        metadata={
            "description": "Protection Domain Id",
        }
    )
    name = fields.Str(
        required=True,
        metadata={
            "description": "Protection Domain Name",
        }
    )


def load_device_group_schema(obj):
    return DeviceGroupSchema().load(obj)

class DeviceGroup(base_client.EntityRequest):
    """
    A class representing Device Group client.
    """
    def list(self):
        """List PowerFlex device groups.

        :rtype: list[dict]
        """
        return list(map(load_device_group_schema, self.get()))

    def get_by_id(self, id):
        """Get PowerFlex device group.

        :type id: str
        :rtype: dict
        """
        return load_device_group_schema(self.get(entity_id=id))

    def get_by_name(self, name):
        """Get PowerFlex device group.

        :type name: str
        :rtype: dict
        """
        result = self.get(filter_fields={'name': name})
        if len(result) >= 1:
            return load_device_group_schema(result[0])
        else:
            return None
