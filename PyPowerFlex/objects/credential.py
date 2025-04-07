# Copyright (c) 2025 Dave Mobley.
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

"""Module for interacting with credential management APIs."""

# pylint: disable=no-member,too-many-arguments

import logging
import xml.etree.ElementTree as ET
from xml.dom import minidom
import requests

from PyPowerFlex import base_client
from PyPowerFlex import exceptions
from PyPowerFlex import utils
from PyPowerFlex.constants import CredentialConstants

LOG = logging.getLogger(__name__)


class BaseCredential:
    """Base class for all credential types."""

    def __init__(self, label, username, password, domain=None):
        """Initialize a base credential with common properties.

        :param label: The credential label (name)
        :type label: str
        :param username: The username for authentication
        :type username: str
        :param password: The password for authentication
        :type password: str
        :param domain: Optional domain for credentials that support it
        :type domain: str
        """
        self.label = label
        self.username = username
        self.password = password
        self.domain = domain
        self.credential_type = None  # Must be set by subclass

    def to_xml(self):
        """Convert credential to XML format required by PowerFlex API.

        :return: XML string representation of credential
        :rtype: str
        """
        if not self.credential_type:
            raise exceptions.InvalidInput("Credential type not specified")

        # Create the credential element
        credential_elem = ET.Element(self.credential_type)
        
        # Add the common elements
        label_elem = ET.SubElement(credential_elem, "label")
        label_elem.text = self.label
        
        username_elem = ET.SubElement(credential_elem, "username")
        username_elem.text = self.username
        
        password_elem = ET.SubElement(credential_elem, "password")
        password_elem.text = self.password
        
        # Add domain if supported and provided
        if self.domain and self.credential_type in CredentialConstants.DOMAIN_SUPPORTED_TYPES:
            domain_elem = ET.SubElement(credential_elem, "domain")
            domain_elem.text = self.domain
            
        return credential_elem

    @classmethod
    def create_credential(cls, credential_type, label, username, password, domain=None):
        """Factory method to create a credential object of the specified type.
        
        :param credential_type: The type of credential to create
        :type credential_type: str
        :param label: The credential label (name)
        :type label: str
        :param username: The username for authentication
        :type username: str
        :param password: The password for authentication
        :type password: str
        :param domain: Optional domain for credentials that support it
        :type domain: str
        :return: A credential object of the specified type
        :rtype: BaseCredential
        :raises: PowerFlexCredentialTypeError if the credential type is invalid
        """
        credential_type = credential_type.lower()
        
        # Map string type names to credential classes
        credential_map = {
            'server': ServerCredential,
            'servercredential': ServerCredential,
            'iom': IomCredential,
            'iomcredential': IomCredential,
            'vcenter': VCenterCredential,
            'vcentercredential': VCenterCredential,
            'em': EmCredential,
            'emcredential': EmCredential,
            'scaleio': ScaleIOCredential,
            'scaleiocredential': ScaleIOCredential,
            'ps': PSCredential,
            'pscredential': PSCredential,
            'os': OSCredential,
            'oscredential': OSCredential,
            'osuser': OSUserCredential,
            'osusercredential': OSUserCredential
        }
        
        if credential_type not in credential_map:
            raise exceptions.PowerFlexCredentialTypeError(credential_type)
        
        # Get the appropriate credential class
        credential_class = credential_map[credential_type]
        
        # Check if this credential type supports domains
        domain_supported = False
        
        # Map credential classes to their credential_type values without instantiating
        credential_type_map = {
            ServerCredential: CredentialConstants.SERVER_CREDENTIAL,
            IomCredential: CredentialConstants.IOM_CREDENTIAL,
            VCenterCredential: CredentialConstants.VCENTER_CREDENTIAL,
            EmCredential: CredentialConstants.EM_CREDENTIAL,
            ScaleIOCredential: CredentialConstants.SCALEIO_CREDENTIAL,
            PSCredential: CredentialConstants.PS_CREDENTIAL,
            OSCredential: CredentialConstants.OS_CREDENTIAL,
            OSUserCredential: CredentialConstants.OS_USER_CREDENTIAL
        }
        
        # Get the credential type string for the selected class
        class_credential_type = credential_type_map.get(credential_class)
        
        # Check if this credential type supports domains
        for supported_type in CredentialConstants.DOMAIN_SUPPORTED_TYPES:
            if supported_type.lower() == class_credential_type.lower():
                domain_supported = True
                break
        
        # Create the credential object
        if domain_supported and domain:
            return credential_class(label, username, password, domain)
        else:
            return credential_class(label, username, password)


class ServerCredential(BaseCredential):
    """Server credential type."""
    
    def __init__(self, label, username, password):
        """Initialize a server credential.
        
        :param label: The credential label (name)
        :type label: str
        :param username: The username for authentication
        :type username: str
        :param password: The password for authentication
        :type password: str
        """
        super().__init__(label, username, password)
        self.credential_type = CredentialConstants.SERVER_CREDENTIAL


class IomCredential(BaseCredential):
    """IOM credential type."""
    
    def __init__(self, label, username, password):
        """Initialize an IOM credential.
        
        :param label: The credential label (name)
        :type label: str
        :param username: The username for authentication
        :type username: str
        :param password: The password for authentication
        :type password: str
        """
        super().__init__(label, username, password)
        self.credential_type = CredentialConstants.IOM_CREDENTIAL


class VCenterCredential(BaseCredential):
    """vCenter credential type."""
    
    def __init__(self, label, username, password, domain=None):
        """Initialize a vCenter credential.
        
        :param label: The credential label (name)
        :type label: str
        :param username: The username for authentication
        :type username: str
        :param password: The password for authentication
        :type password: str
        :param domain: Optional domain for vCenter authentication
        :type domain: str
        """
        super().__init__(label, username, password, domain)
        self.credential_type = CredentialConstants.VCENTER_CREDENTIAL


class EmCredential(BaseCredential):
    """EM credential type."""
    
    def __init__(self, label, username, password, domain=None):
        """Initialize an EM credential.
        
        :param label: The credential label (name)
        :type label: str
        :param username: The username for authentication
        :type username: str
        :param password: The password for authentication
        :type password: str
        :param domain: Optional domain for EM authentication
        :type domain: str
        """
        super().__init__(label, username, password, domain)
        self.credential_type = CredentialConstants.EM_CREDENTIAL


class ScaleIOCredential(BaseCredential):
    """ScaleIO credential type."""
    
    def __init__(self, label, username, password):
        """Initialize a ScaleIO credential.
        
        :param label: The credential label (name)
        :type label: str
        :param username: The username for authentication
        :type username: str
        :param password: The password for authentication
        :type password: str
        """
        super().__init__(label, username, password)
        self.credential_type = CredentialConstants.SCALEIO_CREDENTIAL


class PSCredential(BaseCredential):
    """PS credential type."""
    
    def __init__(self, label, username, password, domain=None):
        """Initialize a PS credential.
        
        :param label: The credential label (name)
        :type label: str
        :param username: The username for authentication
        :type username: str
        :param password: The password for authentication
        :type password: str
        :param domain: Optional domain for PS authentication
        :type domain: str
        """
        super().__init__(label, username, password, domain)
        self.credential_type = CredentialConstants.PS_CREDENTIAL


class OSCredential(BaseCredential):
    """OS credential type."""
    
    def __init__(self, label, username, password, domain=None):
        """Initialize an OS credential.
        
        :param label: The credential label (name)
        :type label: str
        :param username: The username for authentication
        :type username: str
        :param password: The password for authentication
        :type password: str
        :param domain: Optional domain for OS authentication
        :type domain: str
        """
        super().__init__(label, username, password, domain)
        self.credential_type = CredentialConstants.OS_CREDENTIAL


class OSUserCredential(BaseCredential):
    """OS User credential type."""
    
    def __init__(self, label, username, password, domain=None):
        """Initialize an OS User credential.
        
        :param label: The credential label (name)
        :type label: str
        :param username: The username for authentication
        :type username: str
        :param password: The password for authentication
        :type password: str
        :param domain: Optional domain for OS User authentication
        :type domain: str
        """
        super().__init__(label, username, password, domain)
        self.credential_type = CredentialConstants.OS_USER_CREDENTIAL


class Credential(base_client.EntityRequest):
    """
    A class representing Credential client for PowerFlex credential management.
    """
    
    @property
    def entity_name(self):
        """Return the entity name for this object."""
        return 'Credential'
    
    def __init__(self, token, configuration, client=None):
        """Initialize a Credential client.
        
        :param token: The authentication token
        :type token: Token
        :param configuration: The client configuration
        :type configuration: Configuration
        :param client: The PowerFlex client instance
        :type client: PowerFlexClient
        """
        super().__init__(token, configuration)
        self._entity = 'Credential'
        self._api_version_path = "/Api/V1"
        self.client = client
        
    def create(self, credential):
        """Create PowerFlex credential.
        
        :param credential: The credential object to create
        :type credential: BaseCredential
        :rtype: dict
        """
        # Check if gateway version supports credentials
        self._check_gateway_version()
        
        # Check if credential type is valid
        self._validate_credential_type(credential)
        
        # Convert the credential to XML element
        credential_elem = credential.to_xml()
        
        # Create the ASM credential XML wrapper
        root = ET.Element("asmCredential")
        root.append(credential_elem)
        
        # Convert to XML string with proper formatting
        try:
            xml_string = minidom.parseString(ET.tostring(root)).toprettyxml(indent="  ")
            # Remove XML declaration line as it's already included in the template
            xml_string = xml_string.replace('<?xml version="1.0" ?>', '')
        except Exception as e:
            msg = f"Failed to parse XML for credential: {str(e)}"
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)
        
        # Create the final XML payload using the template
        xml_payload = CredentialConstants.CREATE_CREDENTIAL_TEMPLATE.format(
            credential_content=xml_string.strip()
        )
        
        # Send the request
        url = CredentialConstants.BASE_CREDENTIAL_URL
        headers = self.get_auth_headers()
        headers['content-type'] = CredentialConstants.XML_CONTENT_TYPE
        
        # Construct the full URL without duplicating the API version path
        request_url = f"{self.base_url}{url}"
        version = self.login()
        
        request_params = {
            'headers': headers,
            'verify': self.verify_certificate,
            'timeout': self.configuration.timeout,
            'data': xml_payload
        }
        
        if utils.is_version_3(version):
            request_params['auth'] = (
                self.configuration.username, self.token.get())
            del request_params['headers']['Authorization']
        
        try:
            response = requests.post(request_url, **request_params)
            self.logout(version)
            
            if response.status_code != requests.codes.ok:
                try:
                    error_response = response.json()
                except ValueError:
                    error_response = response.text
                    
                msg = f"Failed to create PowerFlex credential. Error: {error_response}"
                LOG.error(msg)
                raise exceptions.PowerFlexFailCreating(self._entity, error_response)
                
            return response.json()
        except requests.exceptions.RequestException as e:
            msg = f"Connection error creating credential: {str(e)}"
            LOG.error(msg)
            raise exceptions.PowerFlexFailCredentialOperation(None, "create", str(e))
        
    def get(self, entity_id=None, filter_fields=None, fields=None):
        """Get PowerFlex credentials.
        
        :param entity_id: Optional credential ID to get a specific credential
        :type entity_id: str
        :param filter_fields: Filter criteria for credentials
        :type filter_fields: dict
        :param fields: Specific fields to retrieve
        :type fields: list|tuple
        :rtype: dict|list[dict]
        """
        # Check if gateway version supports credentials
        self._check_gateway_version()
        
        if entity_id:
            url = f"{CredentialConstants.BASE_CREDENTIAL_URL}/{entity_id}"
        else:
            url = CredentialConstants.BASE_CREDENTIAL_URL
            
        headers = self.get_auth_headers()
        headers['Accept'] = CredentialConstants.JSON_CONTENT_TYPE
        
        # Add query parameters for filters and fields
        params = {}
        if filter_fields:
            params.update(utils.build_filter_params(filter_fields))
        if fields:
            params['fields'] = ','.join(fields)
            
        # Use the URL directly without adding the API version path again
        r, response = self.send_get_request(url, params)
        if r.status_code != requests.codes.ok:
            msg = f"Failed to get PowerFlex credentials. Error: {response}"
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)
            
        return response
        
    def update(self, credential_id, credential):
        """Update PowerFlex credential.
        
        :param credential_id: ID of credential to update
        :type credential_id: str
        :param credential: Updated credential object
        :type credential: BaseCredential
        :rtype: dict
        """
        # Check if gateway version supports credentials
        self._check_gateway_version()
        
        # Check if credential type is valid
        self._validate_credential_type(credential)
            
        # Convert the credential to XML element
        try:
            credential_elem = credential.to_xml()
            
            # Create the ASM credential XML wrapper
            root = ET.Element("asmCredential")
            root.append(credential_elem)
            
            # Convert to XML string with proper formatting
            xml_string = minidom.parseString(ET.tostring(root)).toprettyxml(indent="  ")
            # Remove XML declaration line as it's already included in the template
            xml_string = xml_string.replace('<?xml version="1.0" ?>', '')
        except Exception as e:
            msg = f"Failed to parse XML for credential update: {str(e)}"
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)
        
        # Create the final XML payload using the template
        xml_payload = CredentialConstants.UPDATE_CREDENTIAL_TEMPLATE.format(
            credential_content=xml_string.strip()
        )
        
        # Send the request
        url = f"{CredentialConstants.BASE_CREDENTIAL_URL}/{credential_id}"
        headers = self.get_auth_headers()
        headers['content-type'] = CredentialConstants.XML_CONTENT_TYPE
        
        # Construct the full URL without duplicating the API version path
        request_url = f"{self.base_url}{url}"
        version = self.login()
        
        request_params = {
            'headers': headers,
            'verify': self.verify_certificate,
            'timeout': self.configuration.timeout,
            'data': xml_payload
        }
        
        if utils.is_version_3(version):
            request_params['auth'] = (
                self.configuration.username, self.token.get())
            del request_params['headers']['Authorization']
        
        try:    
            response = requests.put(request_url, **request_params)
            self.logout(version)
            
            if response.status_code != requests.codes.ok:
                try:
                    error_response = response.json()
                except ValueError:
                    error_response = response.text
                    
                msg = f"Failed to update PowerFlex credential with id {credential_id}. Error: {error_response}"
                LOG.error(msg)
                raise exceptions.PowerFlexFailCredentialOperation(credential_id, "update", error_response)
                
            return response.json()
        except requests.exceptions.RequestException as e:
            msg = f"Connection error updating credential: {str(e)}"
            LOG.error(msg)
            raise exceptions.PowerFlexFailCredentialOperation(credential_id, "update", str(e))
        
    def delete(self, credential_id):
        """Delete PowerFlex credential.
        
        :param credential_id: ID of credential to delete
        :type credential_id: str
        :rtype: dict
        """
        # Check if gateway version supports credentials
        self._check_gateway_version()
        
        url = f"{CredentialConstants.BASE_CREDENTIAL_URL}/{credential_id}"
        headers = self.get_auth_headers()
        
        # Construct the full URL without duplicating the API version path
        request_url = f"{self.base_url}{url}"
        version = self.login()
        
        try:
            response = requests.delete(request_url, headers=headers)
            self.logout(version)
            
            if response.status_code != requests.codes.ok:
                try:
                    error_response = response.json()
                except ValueError:
                    error_response = response.text
                    
                msg = f"Failed to delete PowerFlex credential with id {credential_id}. Error: {error_response}"
                LOG.error(msg)
                raise exceptions.PowerFlexFailCredentialOperation(credential_id, "delete", error_response)
                
            return response.json()
        except requests.exceptions.RequestException as e:
            msg = f"Connection error deleting credential: {str(e)}"
            LOG.error(msg)
            raise exceptions.PowerFlexFailCredentialOperation(credential_id, "delete", str(e))

    def _check_gateway_version(self):
        """Check if the PowerFlex Gateway version supports credential management.
        
        :raises: PowerFlexCredentialNotSupported if version is not supported
        """
        try:
            # Get the API version from the system object
            if self.client and hasattr(self.client, 'system'):
                version = self.client.system.api_version()
            else:
                # Fallback to creating a new System instance if client is not available
                from PyPowerFlex.objects import system
                sys_client = system.System(self.token, self.configuration)
                version = sys_client.api_version()
            
            # Check if version is high enough to support credentials (4.0 or higher)
            major_version = version.split('.')[0]
            if int(major_version) < 4:
                msg = f"Credential management requires PowerFlex Gateway version 4.0 or higher. Current version: {version}"
                LOG.error(msg)
                raise exceptions.PowerFlexCredentialNotSupported(version)
        except Exception as e:
            if isinstance(e, exceptions.PowerFlexCredentialNotSupported):
                raise
            msg = f"Error checking PowerFlex Gateway version: {str(e)}"
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

    def get_credential_type(self, credential_data):
        """Extract the credential type from a credential API response.
        
        :param credential_data: The credential data from the API
        :type credential_data: dict
        :return: The credential type (e.g., 'serverCredential')
        :rtype: str
        :raises: PowerFlexClientException if no credential type can be detected
        """
        # Look for the credential type key
        credential_type = None
        for key in credential_data.keys():
            if key in CredentialConstants.ALL_CREDENTIAL_TYPES:
                credential_type = key
                break
        
        if not credential_type:
            msg = f"Could not determine credential type from response: {credential_data}"
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)
            
        return credential_type
    
    def verify_credential(self, credential):
        """Verify if a credential object is valid by attempting to create a temporary XML representation.
        This doesn't make an API call but validates that the credential can be serialized properly.
        
        :param credential: The credential object to verify
        :type credential: BaseCredential
        :return: True if the credential is valid
        :rtype: bool
        :raises: Various exceptions if validation fails
        """
        # Check if credential type is valid
        self._validate_credential_type(credential)
            
        # Check required attributes
        if not hasattr(credential, 'label') or not credential.label:
            raise exceptions.InvalidInput("Credential must have a label")
            
        if not hasattr(credential, 'username') or not credential.username:
            raise exceptions.InvalidInput("Credential must have a username")
            
        if not hasattr(credential, 'password') or not credential.password:
            raise exceptions.InvalidInput("Credential must have a password")
            
        # Check domain parameter if present
        if (hasattr(credential, 'domain') and credential.domain and 
                credential.credential_type not in CredentialConstants.DOMAIN_SUPPORTED_TYPES):
            LOG.warning(f"Domain parameter provided for {credential.credential_type} which doesn't support domains")
            
        # Try to create XML representation
        try:
            credential_elem = credential.to_xml()
            root = ET.Element("asmCredential")
            root.append(credential_elem)
            minidom.parseString(ET.tostring(root))
            return True
        except Exception as e:
            msg = f"Credential validation failed: {str(e)}"
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)

    def _validate_credential_type(self, credential):
        """
        Validate that a credential object has a valid credential type.
        
        :param credential: The credential object to validate
        :type credential: BaseCredential
        :raises: PowerFlexCredentialTypeError if the credential type is invalid
        """
        if not hasattr(credential, 'credential_type') or not credential.credential_type:
            raise exceptions.PowerFlexCredentialTypeError()
            
        # Check if the credential type is in the known types list
        if credential.credential_type not in CredentialConstants.ALL_CREDENTIAL_TYPES:
            raise exceptions.PowerFlexCredentialTypeError(credential.credential_type)