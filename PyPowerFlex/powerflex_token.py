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

"""This module is used for the management of token."""

class PowerFlexToken:
    """
    A class to manage a token.
    """
    def __init__(self):
        """
        Initialize the Token object.

        The initial value of the token is None.
        """
        self.__token = None

    def get(self):
        """
        Get the current token.

        Returns:
            The current token.
        """
        return self.__token

    def set(self, token):
        """
        Set the token.

        Args:
            token (Any): The new token.

        Returns:
            None
        """
        self.__token = token
