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

from PyPowerFlex import exceptions


class Configuration:
    def __init__(self,
                 gateway_address=None,
                 gateway_port=443,
                 username=None,
                 password=None,
                 verify_certificate=False,
                 certificate_path=None,
                 timeout=120,
                 log_level=None):
        self.gateway_address = gateway_address
        self.gateway_port = gateway_port
        self.username = username
        self.password = password
        self.verify_certificate = verify_certificate
        self.certificate_path = certificate_path
        self.timeout = timeout
        self.log_level = log_level

    def validate(self):
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
