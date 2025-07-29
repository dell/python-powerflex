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

"""This module contains the objects for interacting with the PowerFlex APIs."""

import os
import inspect
import importlib
import logging

from PyPowerFlex.base_client import EntityRequest
from PyPowerFlex import exceptions

LOG = logging.getLogger(__name__)
__all__ = []

current_dir = os.path.dirname(__file__)
for filename in os.listdir(current_dir):
    if filename.endswith(".py") and filename != "__init__.py":
        module_name = filename[:-3]
        try:
            module = importlib.import_module(f"{__name__}.{module_name}")
            for name, obj in inspect.getmembers(module, inspect.isclass):
                if issubclass(obj, EntityRequest) and obj is not EntityRequest:
                    __all__.append(name)
                    globals()[name] = obj
        except Exception as e:
            msg = f"Failed to import module {module_name}: {e}"
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)
