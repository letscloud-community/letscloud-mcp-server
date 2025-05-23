from typing import List, Optional
import logging
from letscloud import LetsCloud
from letscloud.domains import (
    SSHKey,
    SSHKeyCreateRequest,
    Instance,
    CreateInstanceRequest,
    Plan
)

logger = logging.getLogger(__name__)

class LetsCloudClient:
    """Client wrapper for LetsCloud SDK"""
    
    def __init__(self):
        pass

    def _get_client(self, letscloud_token: str) -> LetsCloud:
        """Get a LetsCloud client instance with the provided token"""
        return LetsCloud(letscloud_token)

    # SSH Key Operations
    def create_ssh_key(self, letscloud_token: str, title: str, key: str) -> SSHKey:
        """Create a new SSH key"""
        try:
            client = self._get_client(letscloud_token)
            request = SSHKeyCreateRequest(
                title=title,
                key=key
            )
            return client.NewSSHKey(request.title, request.key)
        except Exception as e:
            logger.error(f"Failed to create SSH key: {str(e)}")
            raise

    def list_ssh_keys(self, letscloud_token: str) -> List[SSHKey]:
        """List all SSH keys"""
        try:
            client = self._get_client(letscloud_token)
            return client.SSHKeys()
        except Exception as e:
            logger.error(f"Failed to list SSH keys: {str(e)}")
            raise

    def get_ssh_key(self, letscloud_token: str, key_id: str) -> SSHKey:
        """Get a specific SSH key"""
        try:
            client = self._get_client(letscloud_token)
            return client.SSHKey(key_id)
        except Exception as e:
            logger.error(f"Failed to get SSH key: {str(e)}")
            raise

    def delete_ssh_key(self, letscloud_token: str, key_id: str) -> None:
        """Delete an SSH key"""
        try:
            client = self._get_client(letscloud_token)
            client.DeleteSSHKey(key_id)
        except Exception as e:
            logger.error(f"Failed to delete SSH key: {str(e)}")
            raise

    # Instance Operations
    def create_instance(self, letscloud_token: str, request: CreateInstanceRequest) -> None:
        """Create a new instance"""
        try:
            client = self._get_client(letscloud_token)
            client.CreateInstance(request)
        except Exception as e:
            logger.error(f"Failed to create instance: {str(e)}")
            raise

    def list_instances(self, letscloud_token: str) -> List[Instance]:
        """List all instances"""
        try:
            client = self._get_client(letscloud_token)
            return client.Instances()
        except Exception as e:
            logger.error(f"Failed to list instances: {str(e)}")
            raise

    def get_instance(self, letscloud_token: str, instance_id: str) -> Instance:
        """Get a specific instance"""
        try:
            client = self._get_client(letscloud_token)
            return client.Instance(instance_id)
        except Exception as e:
            logger.error(f"Failed to get instance: {str(e)}")
            raise

    def delete_instance(self, letscloud_token: str, instance_id: str) -> None:
        """Delete an instance"""
        try:
            client = self._get_client(letscloud_token)
            client.DeleteInstance(instance_id)
        except Exception as e:
            logger.error(f"Failed to delete instance: {str(e)}")
            raise

    def reset_instance_password(self, letscloud_token: str, instance_id: str, password: str) -> None:
        """Reset instance password"""
        try:
            client = self._get_client(letscloud_token)
            client.ResetPasswordInstance(instance_id, password)
        except Exception as e:
            logger.error(f"Failed to reset instance password: {str(e)}")
            raise

    # Location Plans
    def get_location_plans(self, letscloud_token: str, location: str) -> List[Plan]:
        """Get available plans for a location"""
        try:
            client = self._get_client(letscloud_token)
            return client.LocationPlans(location)
        except Exception as e:
            logger.error(f"Failed to get location plans: {str(e)}")
            raise 