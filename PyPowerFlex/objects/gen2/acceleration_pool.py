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

"""Module for interacting with accelaration pool APIs."""

# pylint: disable=too-few-public-methods,duplicate-code

import logging
from gen1 import AccelerationPool
from PyPowerFlex import exceptions


LOG = logging.getLogger(__name__)


class AccelerationPool(AccelerationPool):
    """
    A class representing a PowerFlex acceleration pool.

    This class provides methods to create, delete, and query acceleration pools.
    """
    pass