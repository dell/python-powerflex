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

"""This module is used for the configuration of the client."""

# pylint: disable=too-many-instance-attributes,too-many-arguments,too-many-positional-arguments,too-few-public-methods

from PyPowerFlex import exceptions

class Configuration:
    """
    Configuration class for the PyPowerFlex library.
    """
    def __init__(self,
                 gateway_address=None,
                 gateway_port=443,
                 username=None,
                 password=None,
                 verify_certificate=False,
                 certificate_path=None,
                 timeout=120,
                 log_level=None):
        """
        Initializes the Configuration class.
        """
        self.gateway_address = gateway_address
        self.gateway_port = gateway_port
        self.username = username
        self.password = password
        self.verify_certificate = verify_certificate
        self.certificate_path = certificate_path
        self.timeout = timeout
        self.log_level = log_level

    def validate(self):
        """
        Validates the configuration.

        :raises exceptions.InvalidConfiguration: If any of the required parameters are not set.
        """
        if not all(
                [
                    self.gateway_address,
                    self.gateway_port,
                    self.username,
                    self.password
                ]
        ):
            raise exceptions.InvalidConfiguration(
                'The following parameters must be set: '
                'gateway_address, gateway_port, username, password.'
            )
