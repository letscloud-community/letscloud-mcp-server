from typing import Dict, Any
import logging
from ..core.letscloud_client import LetsCloudClient
from ..models.context import Context, ContextResponse
from letscloud.domains import CreateInstanceRequest

logger = logging.getLogger(__name__)

class LetsCloudHandler:
    """Handler for LetsCloud contexts"""
    
    def __init__(self):
        self.client = LetsCloudClient()

    async def handle_context(self, context: Context) -> ContextResponse:
        """Handle a LetsCloud context"""
        try:
            if context.type == "INFRASTRUCTURE":
                return await self._handle_infrastructure(context)
            else:
                return ContextResponse(
                    context_id=context.id,
                    success=False,
                    error=f"Unsupported context type: {context.type}",
                    processing_time=0
                )
        except Exception as e:
            logger.error(f"Error handling context: {str(e)}")
            return ContextResponse(
                context_id=context.id,
                success=False,
                error=str(e),
                processing_time=0
            )

    async def _handle_infrastructure(self, context: Context) -> ContextResponse:
        """Handle infrastructure-related contexts"""
        try:
            # Get LetsCloud token from context metadata
            letscloud_token = context.metadata.get("letscloud_token")
            if not letscloud_token:
                return ContextResponse(
                    context_id=context.id,
                    success=False,
                    error="LetsCloud token not provided in context metadata",
                    processing_time=0
                )

            if context.action == "CREATE":
                if "title" in context.parameters and "key" in context.parameters:
                    # SSH Key creation
                    result = self.client.create_ssh_key(
                        letscloud_token=letscloud_token,
                        title=context.parameters["title"],
                        key=context.parameters["key"]
                    )
                    return ContextResponse(
                        context_id=context.id,
                        success=True,
                        result={"ssh_key": result.dict()},
                        processing_time=0
                    )
                elif "label" in context.parameters:
                    # Instance creation
                    request = CreateInstanceRequest(
                        label=context.parameters["label"],
                        plan_slug=context.parameters.get("plan_slug"),
                        image_slug=context.parameters.get("image_slug"),
                        location_slug=context.parameters.get("location_slug"),
                        hostname=context.parameters.get("hostname"),
                        password=context.parameters.get("password"),
                        ssh_keys=context.parameters.get("ssh_keys", [])
                    )
                    self.client.create_instance(letscloud_token=letscloud_token, request=request)
                    return ContextResponse(
                        context_id=context.id,
                        success=True,
                        result={"message": "Instance creation initiated"},
                        processing_time=0
                    )

            elif context.action == "READ":
                if "id" in context.parameters:
                    # Get specific resource
                    if "ssh_key" in context.metadata.get("resource_type", ""):
                        result = self.client.get_ssh_key(
                            letscloud_token=letscloud_token,
                            key_id=context.parameters["id"]
                        )
                        return ContextResponse(
                            context_id=context.id,
                            success=True,
                            result={"ssh_key": result.dict()},
                            processing_time=0
                        )
                    else:
                        result = self.client.get_instance(
                            letscloud_token=letscloud_token,
                            instance_id=context.parameters["id"]
                        )
                        return ContextResponse(
                            context_id=context.id,
                            success=True,
                            result={"instance": result.dict()},
                            processing_time=0
                        )
                elif "location" in context.parameters:
                    # Get location plans
                    result = self.client.get_location_plans(
                        letscloud_token=letscloud_token,
                        location=context.parameters["location"]
                    )
                    return ContextResponse(
                        context_id=context.id,
                        success=True,
                        result={"plans": [plan.dict() for plan in result]},
                        processing_time=0
                    )
                else:
                    # List all resources
                    if "ssh_key" in context.metadata.get("resource_type", ""):
                        result = self.client.list_ssh_keys(letscloud_token=letscloud_token)
                        return ContextResponse(
                            context_id=context.id,
                            success=True,
                            result={"ssh_keys": [key.dict() for key in result]},
                            processing_time=0
                        )
                    else:
                        result = self.client.list_instances(letscloud_token=letscloud_token)
                        return ContextResponse(
                            context_id=context.id,
                            success=True,
                            result={"instances": [instance.dict() for instance in result]},
                            processing_time=0
                        )

            elif context.action == "DELETE":
                if "id" in context.parameters:
                    if "ssh_key" in context.metadata.get("resource_type", ""):
                        self.client.delete_ssh_key(
                            letscloud_token=letscloud_token,
                            key_id=context.parameters["id"]
                        )
                    else:
                        self.client.delete_instance(
                            letscloud_token=letscloud_token,
                            instance_id=context.parameters["id"]
                        )
                    return ContextResponse(
                        context_id=context.id,
                        success=True,
                        result={"message": "Resource deleted successfully"},
                        processing_time=0
                    )

            elif context.action == "UPDATE":
                if "id" in context.parameters and "password" in context.parameters:
                    self.client.reset_instance_password(
                        letscloud_token=letscloud_token,
                        instance_id=context.parameters["id"],
                        password=context.parameters["password"]
                    )
                    return ContextResponse(
                        context_id=context.id,
                        success=True,
                        result={"message": "Password reset successfully"},
                        processing_time=0
                    )

            return ContextResponse(
                context_id=context.id,
                success=False,
                error=f"Unsupported action: {context.action}",
                processing_time=0
            )

        except Exception as e:
            logger.error(f"Error handling infrastructure context: {str(e)}")
            return ContextResponse(
                context_id=context.id,
                success=False,
                error=str(e),
                processing_time=0
            ) 