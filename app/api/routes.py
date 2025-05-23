from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from ..models.context import (
    Context,
    ContextResponse,
    ContextTemplate,
    ContextType,
    ContextState
)
from ..core.processor import ContextProcessor

router = APIRouter(prefix="/mcp", tags=["Model Context Protocol"])

# Dependency to get the context processor
def get_processor() -> ContextProcessor:
    return ContextProcessor()

@router.post("/contexts", response_model=ContextResponse)
async def create_context(
    context: Context,
    processor: ContextProcessor = Depends(get_processor)
):
    """
    Create and process a new context.
    
    This endpoint accepts a context object and processes it according to its type and action.
    The response includes the processing result and any errors that occurred.
    """
    return await processor.process_context(context)

@router.get("/contexts", response_model=List[Context])
async def list_contexts(
    context_type: Optional[ContextType] = None,
    state: Optional[ContextState] = None,
    processor: ContextProcessor = Depends(get_processor)
):
    """
    List all contexts with optional filtering by type and state.
    
    This endpoint returns a list of all contexts that match the specified filters.
    If no filters are provided, all contexts are returned.
    """
    return processor.list_contexts(context_type, state)

@router.get("/contexts/{context_id}", response_model=Context)
async def get_context(
    context_id: str,
    processor: ContextProcessor = Depends(get_processor)
):
    """
    Get a specific context by ID.
    
    This endpoint returns the details of a specific context, including its current state
    and processing results.
    """
    context = processor.get_context(context_id)
    if not context:
        raise HTTPException(status_code=404, detail="Context not found")
    return context

@router.delete("/contexts/{context_id}")
async def delete_context(
    context_id: str,
    processor: ContextProcessor = Depends(get_processor)
):
    """
    Delete a context by ID.
    
    This endpoint removes a context from the system. This is useful for cleaning up
    completed or failed contexts.
    """
    if not processor.delete_context(context_id):
        raise HTTPException(status_code=404, detail="Context not found")
    return {"message": "Context deleted successfully"}

@router.post("/templates", response_model=ContextTemplate)
async def create_template(
    template: ContextTemplate,
    processor: ContextProcessor = Depends(get_processor)
):
    """
    Create a new context template.
    
    This endpoint allows you to create a template that can be used to create new contexts
    with predefined parameters and validation rules.
    """
    # TODO: Implement template storage and validation
    return template

@router.get("/templates", response_model=List[ContextTemplate])
async def list_templates(
    context_type: Optional[ContextType] = None,
    processor: ContextProcessor = Depends(get_processor)
):
    """
    List all available context templates.
    
    This endpoint returns a list of all templates that can be used to create new contexts.
    Templates can be filtered by context type.
    """
    # TODO: Implement template listing
    return []

@router.get("/health")
async def health_check():
    """
    Check the health of the MCP service.
    
    This endpoint returns the current status of the MCP service and its components.
    """
    return {
        "status": "healthy",
        "version": "1.0.0",
        "components": {
            "processor": "operational",
            "api": "operational"
        }
    } 