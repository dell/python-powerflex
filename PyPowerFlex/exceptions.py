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

"""This module contains the definitions of the exceptions used in the code."""

# pylint: disable=super-init-not-called

class PowerFlexClientException(Exception):
    """
    Base class for all exceptions raised by the PowerFlexClient.
    """
    def __init__(self, message, response=None):
        self.message = message
        self.response = response

    def __str__(self):
        return self.message


class ClientNotInitialized(PowerFlexClientException):
    """
    Exception raised when the PowerFlexClient is not initialized.
    """
    def __init__(self):
        self.message = (
            'PowerFlex Client is not initialized. '
            'Call `.initialize()` to proceed.'
        )


class InvalidConfiguration(PowerFlexClientException):
    """
    Exception raised when the configuration is invalid.
    """


class FieldsNotFound(PowerFlexClientException):
    """
    Exception raised when the required fields are not found.
    """


class InvalidInput(PowerFlexClientException):
    """
    Exception raised when the input is invalid.
    """


class PowerFlexFailCreating(PowerFlexClientException):
    """
    Exception raised when creating a PowerFlex entity fails.
    """
    base = 'Failed to create PowerFlex {entity}.'

    def __init__(self, entity, response=None):
        self.message = self.base.format(entity=entity)
        self.response = response
        if response:
            self.message = (
                f"{self.message} Error: "
                f"{response}"
            )


class PowerFlexFailDeleting(PowerFlexClientException):
    """
    Exception raised when deleting a PowerFlex entity fails.
    """
    base = 'Failed to delete PowerFlex {entity} with id {_id}.'

    def __init__(self, entity, entity_id, response=None):
        self.message = self.base.format(entity=entity, _id=entity_id)
        self.response = response
        if response:
            self.message = f"{self.message} Error: {response}"


class PowerFlexFailQuerying(PowerFlexClientException):
    """
    Exception raised when querying a PowerFlex entity fails.
    """
    base = 'Failed to query PowerFlex {entity}'

    def __init__(self, entity, entity_id=None, response=None):
        base = self.base.format(entity=entity)
        self.response = response
        if entity_id and response is None:
            self.message = f"{base} with id {entity_id}."
        elif entity is None and response:
            self.message = f"{base} Error: {response}."
        elif entity and response:
            self.message = f"{base} with id {entity_id}. Error: {response}."
        else:
            self.message = f"{base}."


class PowerFlexFailRenaming(PowerFlexClientException):
    """
    Exception raised when renaming a PowerFlex entity fails.
    """
    base = 'Failed to rename PowerFlex {entity} with id {_id}.'

    def __init__(self, entity, entity_id, response=None):
        self.message = self.base.format(entity=entity, _id=entity_id)
        self.response = response
        if response:
            self.message = f"{self.message} Error: {response}"

class PowerFlexFailEntityOperation(PowerFlexClientException):
    """
    Exception raised when performing an operation on a PowerFlex entity fails.
    """
    base = 'Failed to perform {action} on PowerFlex {entity} with id {_id}.'

    def __init__(self, entity, entity_id, action, response=None):
        self.message = \
            self.base.format(action=action, entity=entity, _id=entity_id)
        self.response = response
        if response:
            self.message = f"{self.message} Error: {response}"

class PowerFlexFailMigration(PowerFlexClientException):
    """
    Exception raised when migrating a PowerFlex entity fails.
    """
    base = 'Failed to migrate PowerFlex {entity} with id {_id} to storage pool {dest_sp_id}.'

    def __init__(self, entity, entity_id, dest_sp_id, response=None):
        self.message = self.base.format(
            entity=entity,
            _id=entity_id,
            dest_sp_id=dest_sp_id
        )
        self.response = response
        if response:
            self.message = f"{self.message} Error: {response}"


class PowerFlexCredentialNotSupported(PowerFlexClientException):
    """Raised when credential operations are attempted on unsupported Gateway versions."""

    def __init__(self, gateway_version):
        """Initialize the exception.

        :param gateway_version: The PowerFlex Gateway version that doesn't support
                               credential management
        :type gateway_version: str
        """
        self.gateway_version = gateway_version
        message = (f"Credential operations are not supported for PowerFlex "
                   f"Gateway version {gateway_version}. PowerFlex Gateway "
                   f"versions below 4.0 do not support credential management "
                   f"operations.")
        super().__init__(message)


class PowerFlexCredentialTypeError(PowerFlexClientException):
    """
    Exception raised when an invalid credential type is specified.
    """
    def __init__(self, credential_type=None):
        valid_types = [
            'serverCredential', 'iomCredential', 'vCenterCredential', 
            'emCredential', 'scaleIOCredential', 'PSCredential', 
            'OSCredential', 'OSUserCredential'
        ]
        
        self.message = (
            f'Invalid credential type: {credential_type}. '
            f'Valid credential types are: {", ".join(valid_types)}'
        )


class PowerFlexFailCredentialOperation(PowerFlexClientException):
    """
    Exception raised when performing an operation on a PowerFlex credential fails.
    """
    base = 'Failed to perform {action} on credential with id {_id}.'

    def __init__(self, credential_id, action, response=None):
        self.message = self.base.format(action=action, _id=credential_id)
        self.response = response
        if response:
            self.message = f"{self.message} Error: {response}"
