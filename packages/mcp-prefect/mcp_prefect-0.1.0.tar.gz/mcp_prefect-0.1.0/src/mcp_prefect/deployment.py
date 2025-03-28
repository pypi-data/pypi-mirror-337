from typing import Any, Callable, Dict, List, Optional, Union
from uuid import UUID

import mcp.types as types
from prefect import get_client

from .envs import PREFECT_API_URL


def get_all_functions() -> list[tuple[Callable, str, str]]:
    return [
        (get_deployments, "get_deployments", "Get all deployments"),
        (get_deployment, "get_deployment", "Get a deployment by ID"),
        (create_flow_run_from_deployment, "create_flow_run_from_deployment", "Create a flow run from a deployment"),
        (delete_deployment, "delete_deployment", "Delete a deployment"),
        (update_deployment, "update_deployment", "Update a deployment"),
        (get_deployment_schedule, "get_deployment_schedule", "Get a deployment's schedule"),
        (set_deployment_schedule, "set_deployment_schedule", "Set a deployment's schedule"),
        (pause_deployment_schedule, "pause_deployment_schedule", "Pause a deployment's schedule"),
        (resume_deployment_schedule, "resume_deployment_schedule", "Resume a deployment's schedule"),
    ]


def get_deployment_url(deployment_id: str) -> str:
    base_url = PREFECT_API_URL.replace("/api", "")
    return f"{base_url}/deployments/{deployment_id}"


async def get_deployments(
    limit: Optional[int] = None,
    offset: Optional[int] = None,
    flow_name: Optional[str] = None,
    name: Optional[str] = None,
    tags: Optional[List[str]] = None,
    is_schedule_active: Optional[bool] = None,
    work_queue_name: Optional[str] = None,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Get a list of deployments with optional filtering.
    
    Args:
        limit: Maximum number of deployments to return
        offset: Number of deployments to skip
        flow_name: Filter by flow name
        name: Filter by deployment name
        tags: Filter by tags
        is_schedule_active: Filter by schedule active status
        work_queue_name: Filter by work queue name
        
    Returns:
        A list of deployments with their details
    """
    async with get_client() as client:
    
        # Build filter parameters
        filters = {}
        if flow_name:
            filters["flow_name"] = {"like_": f"%{flow_name}%"}
        if name:
            filters["name"] = {"like_": f"%{name}%"}
        if tags:
            filters["tags"] = {"all_": tags}
        if is_schedule_active is not None:
            filters["is_schedule_active"] = {"eq_": is_schedule_active}
        if work_queue_name:
            filters["work_queue_name"] = {"eq_": work_queue_name}
        
        deployments = await client.read_deployments(
            limit=limit,
            offset=offset,
            **filters
        )
        
        # Add UI links to each deployment
        deployments_result = {
            "deployments": [
                {
                    **deployment.dict(),
                    "ui_url": get_deployment_url(str(deployment.id))
                }
                for deployment in deployments
            ]
        }
        
        return [types.TextContent(type="text", text=str(deployments_result))]


async def get_deployment(
    deployment_id: str,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Get details of a specific deployment by ID.
    
    Args:
        deployment_id: The deployment UUID
        
    Returns:
        Deployment details
    """
    async with get_client() as client:
        deployment = await client.read_deployment(UUID(deployment_id))
        
        # Add UI link
        deployment_dict = deployment.dict()
        deployment_dict["ui_url"] = get_deployment_url(deployment_id)
        
        return [types.TextContent(type="text", text=str(deployment_dict))]


async def create_flow_run_from_deployment(
    deployment_id: str,
    parameters: Optional[Dict[str, Any]] = None,
    name: Optional[str] = None,
    tags: Optional[List[str]] = None,
    idempotency_key: Optional[str] = None,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Create a flow run from a deployment.
    
    Args:
        deployment_id: The deployment UUID
        parameters: Optional parameters to pass to the flow run
        name: Optional name for the flow run
        tags: Optional tags for the flow run
        idempotency_key: Optional idempotency key
        
    Returns:
        Details of the created flow run
    """
    async with get_client() as client:
        parameters = parameters or {}
        
        flow_run = await client.create_flow_run_from_deployment(
            deployment_id=UUID(deployment_id),
            parameters=parameters,
            name=name,
            tags=tags,
            idempotency_key=idempotency_key,
        )
        
        # Add URL
        flow_run_dict = flow_run.dict()
        flow_run_dict["ui_url"] = PREFECT_API_URL.replace("/api", "") + f"/flow-runs/{flow_run.id}"
        
        return [types.TextContent(type="text", text=str(flow_run_dict))]


async def delete_deployment(
    deployment_id: str,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Delete a deployment by ID.
    
    Args:
        deployment_id: The deployment UUID
        
    Returns:
        Confirmation message
    """
    async with get_client() as client:
        await client.delete_deployment(UUID(deployment_id))
        
        return [types.TextContent(type="text", text=f"Deployment '{deployment_id}' deleted successfully.")]


async def update_deployment(
    deployment_id: str,
    name: Optional[str] = None,
    description: Optional[str] = None,
    version: Optional[str] = None,
    tags: Optional[List[str]] = None,
    parameters: Optional[Dict[str, Any]] = None,
    work_queue_name: Optional[str] = None,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Update a deployment.
    
    Args:
        deployment_id: The deployment UUID
        name: New name for the deployment
        description: New description
        version: New version
        tags: New tags
        parameters: New parameters
        work_queue_name: New work queue name
        
    Returns:
        Details of the updated deployment
    """
    async with get_client() as client:
        # Get current deployment
        deployment = await client.read_deployment(UUID(deployment_id))
        
        # Prepare update data
        update_data = {}
        if name is not None:
            update_data["name"] = name
        if description is not None:
            update_data["description"] = description
        if version is not None:
            update_data["version"] = version
        if tags is not None:
            update_data["tags"] = tags
        if parameters is not None:
            update_data["parameters"] = parameters
        if work_queue_name is not None:
            update_data["work_queue_name"] = work_queue_name
        
        # Update deployment
        updated_deployment = await client.update_deployment(
            deployment_id=UUID(deployment_id),
            **update_data
        )
        
        # Add UI link
        updated_deployment_dict = updated_deployment.dict()
        updated_deployment_dict["ui_url"] = get_deployment_url(deployment_id)
        
        return [types.TextContent(type="text", text=str(updated_deployment_dict))]


async def get_deployment_schedule(
    deployment_id: str,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Get a deployment's schedule.
    
    Args:
        deployment_id: The deployment UUID
        
    Returns:
        Schedule details
    """
    async with get_client() as client:
        schedule = await client.read_deployment_schedule(UUID(deployment_id))
        
        return [types.TextContent(type="text", text=str(schedule.dict()))]


async def set_deployment_schedule(
    deployment_id: str,
    cron: Optional[str] = None,
    interval_seconds: Optional[int] = None,
    anchor_date: Optional[str] = None,
    timezone: Optional[str] = None,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Set a deployment's schedule.
    
    Args:
        deployment_id: The deployment UUID
        cron: Cron expression for the schedule
        interval_seconds: Alternative to cron - interval in seconds
        anchor_date: Required for interval schedules - the anchor date
        timezone: Timezone for the schedule
        
    Returns:
        Updated schedule details
    """
    async with get_client() as client:
        # Check schedule type
        if cron is not None and interval_seconds is not None:
            return [types.TextContent(
                type="text",
                text="Cannot specify both cron and interval_seconds. Choose one schedule type."
            )]
        
        if cron is not None:
            # Set cron schedule
            schedule = await client.set_deployment_schedule(
                deployment_id=UUID(deployment_id),
                schedule={"cron": cron, "timezone": timezone}
            )
        elif interval_seconds is not None:
            # Set interval schedule
            if not anchor_date:
                return [types.TextContent(
                    type="text",
                    text="anchor_date is required for interval schedules"
                )]
            
            schedule = await client.set_deployment_schedule(
                deployment_id=UUID(deployment_id),
                schedule={
                    "interval": interval_seconds,
                    "anchor_date": anchor_date,
                    "timezone": timezone
                }
            )
        else:
            return [types.TextContent(
                type="text",
                text="Must specify either cron or interval_seconds to set a schedule"
            )]
        
        return [types.TextContent(type="text", text=str(schedule.dict()))]


async def pause_deployment_schedule(
    deployment_id: str,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Pause a deployment's schedule.
    
    Args:
        deployment_id: The deployment UUID
        
    Returns:
        Confirmation message
    """
    async with get_client() as client:
        await client.pause_deployment_schedule(UUID(deployment_id))
        
        return [types.TextContent(type="text", text=f"Schedule for deployment '{deployment_id}' paused successfully.")]


async def resume_deployment_schedule(
    deployment_id: str,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Resume a deployment's schedule.
    
    Args:
        deployment_id: The deployment UUID
        
    Returns:
        Confirmation message
    """
    async with get_client() as client:
        await client.resume_deployment_schedule(UUID(deployment_id))
        
        return [types.TextContent(type="text", text=f"Schedule for deployment '{deployment_id}' resumed successfully.")]