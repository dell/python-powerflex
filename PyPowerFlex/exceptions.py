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


class PowerFlexClientException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class ClientNotInitialized(PowerFlexClientException):
    def __init__(self):
        self.message = (
            'PowerFlex Client is not initialized. '
            'Call `.initialize()` to proceed.'
        )


class InvalidConfiguration(PowerFlexClientException):
    pass


class FieldsNotFound(PowerFlexClientException):
    pass


class InvalidInput(PowerFlexClientException):
    pass


class PowerFlexFailCreating(PowerFlexClientException):
    base = 'Failed to create PowerFlex {entity}.'

    def __init__(self, entity):
        self.message = self.base.format(entity=entity)


class PowerFlexFailDeleting(PowerFlexClientException):
    base = 'Failed to delete PowerFlex {entity} with id {_id}.'

    def __init__(self, entity, entity_id):
        self.message = self.base.format(entity=entity, _id=entity_id)


class PowerFlexFailQuerying(PowerFlexClientException):
    base = 'Failed to query PowerFlex {entity}'

    def __init__(self, entity, entity_id=None):
        base = self.base.format(entity=entity)
        if entity_id:
            self.message = '{base} with id {_id}.'.format(base=base,
                                                          _id=entity_id)
        else:
            self.message = '{base}.'.format(base=base)


class PowerFlexFailRenaming(PowerFlexClientException):
    base = 'Failed to rename PowerFlex {entity} with id {_id}.'

    def __init__(self, entity, entity_id):
        self.message = self.base.format(entity=entity, _id=entity_id)
