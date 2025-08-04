# Copyright (c) 2025 Dell Inc. or its subsidiaries.
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

"""Module for general setup."""

# pylint: disable=import-error

from setuptools import setup

setup(
    name='PyPowerFlex',
    version='2.0.0',
    description='Python library for Dell PowerFlex',
    author='Ansible Team at Dell',
    author_email='ansible.team@dell.com',
    install_requires=[
        'packaging>=20.4',
        'requests>=2.23.0',
    ],
    license_files = ('LICENSE',),
    classifiers=['License :: OSI Approved :: Apache Software License'],
    packages=[
        'PyPowerFlex',
        'PyPowerFlex.objects.common',
        'PyPowerFlex.objects.gen1',
        'PyPowerFlex.objects.gen2',
    ],
    python_requires='>=3.5'
)
