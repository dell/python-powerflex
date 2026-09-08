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

"""Module for testing the Gen1/Gen2 detection done on client initialization."""

# pylint: disable=duplicate-code

from PyPowerFlex.objects import gen1
from PyPowerFlex.objects import gen2
from tests.common import PyPowerFlexTestCase


@PyPowerFlexTestCase.version('4.5')
class TestGen1Client(PyPowerFlexTestCase):
    """
    Test the detection of a Gen1 system, where the API version and the
    component version are in sync.
    """

    def setUp(self):
        """
        Set up the test environment.
        """
        super().setUp()
        self.client.initialize()

    def test_gen1_objects_are_used(self):
        """
        Test that the Gen1 objects are used.
        """
        self.assertIsInstance(self.client.device, gen1.Device)
        self.assertIsInstance(self.client.storage_pool, gen1.StoragePool)

    def test_gen2_only_objects_are_not_available(self):
        """
        Test that the Gen2 only objects are not available.
        """
        self.assertFalse(hasattr(self.client, 'device_group'))
        self.assertFalse(hasattr(self.client, 'storage_node'))

    def test_gen1_only_objects_are_available(self):
        """
        Test that the Gen1 only objects are available.
        """
        self.assertIsInstance(self.client.sds, gen1.Sds)
        self.assertIsInstance(self.client.replication_consistency_group,
                              gen1.ReplicationConsistencyGroup)

    def test_component_version_is_not_queried(self):
        """
        Test that an API version below 5.0 is conclusive on its own, so no
        component version is queried while initializing the client.
        """
        call_count = self.get_mock.call_count
        self.client.initialize()
        self.assertEqual(call_count * 2, self.get_mock.call_count)


@PyPowerFlexTestCase.version('5.0')
class TestGen2Client(PyPowerFlexTestCase):
    """
    Test the detection of a Gen2 system, where the API version and the
    component version are in sync.
    """

    def setUp(self):
        """
        Set up the test environment.
        """
        super().setUp()
        self.client.initialize()

    def test_gen2_objects_are_used(self):
        """
        Test that the Gen2 objects are used.
        """
        self.assertIsInstance(self.client.device, gen2.Device)
        self.assertIsInstance(self.client.storage_pool, gen2.StoragePool)

    def test_gen2_only_objects_are_available(self):
        """
        Test that the Gen2 only objects are available.
        """
        self.assertIsInstance(self.client.device_group, gen2.DeviceGroup)
        self.assertIsInstance(self.client.storage_node, gen2.StorageNode)

    def test_component_version(self):
        """
        Test that the component version is reported.
        """
        self.assertEqual('5.0.0.0', self.client.system.component_version())


@PyPowerFlexTestCase.version('5.1', component_version='4.5')
class TestGen1ClientWithGen2Api(PyPowerFlexTestCase):
    """
    Test the detection of a Gen1 system that already exposes the 5.x API.

    The API version and the components are upgraded independently, so a
    system running components 4.5.x can serve API version 5.1. Such a system
    is still a Gen1 system and must be handled with the Gen1 objects.
    """

    def setUp(self):
        """
        Set up the test environment.
        """
        super().setUp()
        self.client.initialize()

    def test_api_and_component_versions_differ(self):
        """
        Test that the API version and the component version differ.
        """
        self.assertEqual('5.1', self.client.system.api_version())
        self.assertEqual('4.5.0.0', self.client.system.component_version())

    def test_gen1_objects_are_used(self):
        """
        Test that the component version wins over the API version.
        """
        self.assertIsInstance(self.client.device, gen1.Device)
        self.assertIsInstance(self.client.storage_pool, gen1.StoragePool)

    def test_gen2_only_objects_are_not_available(self):
        """
        Test that the Gen2 only objects are not available.
        """
        self.assertFalse(hasattr(self.client, 'device_group'))
        self.assertFalse(hasattr(self.client, 'storage_node'))

    def test_component_version_is_cached(self):
        """
        Test that the component version is cached.
        """
        self.client.system.component_version()
        call_count = self.get_mock.call_count
        self.client.system.component_version()
        self.client.system.component_version()
        self.assertEqual(call_count, self.get_mock.call_count)

    def test_component_version_not_cached(self):
        """
        Test that the cache can be bypassed.
        """
        self.client.system.component_version()
        call_count = self.get_mock.call_count
        self.assertEqual('4.5.0.0',
                         self.client.system.component_version(cached=False))
        self.assertGreater(self.get_mock.call_count, call_count)


@PyPowerFlexTestCase.version('5.1')
class TestComponentVersionFallback(PyPowerFlexTestCase):
    """
    Test the behaviour when the component version cannot be determined.
    """

    def setUp(self):
        """
        Set up the test environment.
        """
        super().setUp()
        # A system that does not report any usable version information.
        self.MOCK_RESPONSES = {
            self.RESPONSE_MODE.Valid: {
                self.SYSTEM_API_PATH: [{'id': '1'}],
            },
        }

    def test_component_version_falls_back_to_api_version(self):
        """
        Test that the API version is used when the component version is
        unknown, so the previous behaviour is kept.
        """
        self.client.initialize()
        self.assertEqual('5.1', self.client.system.component_version())

    def test_gen2_objects_are_used(self):
        """
        Test that the client falls back to the API version based detection.
        """
        self.client.initialize()
        self.assertIsInstance(self.client.device, gen2.Device)
