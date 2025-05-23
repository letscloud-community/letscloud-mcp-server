from typing import Dict, List, Optional, Any, Callable
from datetime import datetime
import time
import logging
from ..models.context import (
    Context,
    ContextResponse,
    ContextState,
    ContextType,
    ContextAction,
    ContextValidation
)

logger = logging.getLogger(__name__)

class ContextProcessor:
    """Processes and manages context operations"""
    
    def __init__(self):
        self._handlers: Dict[ContextType, Dict[ContextAction, Callable]] = {}
        self._validators: Dict[ContextType, ContextValidation] = {}
        self._context_store: Dict[str, Context] = {}

    def register_handler(
        self,
        context_type: ContextType,
        action: ContextAction,
        handler: Callable
    ) -> None:
        """Register a handler for a specific context type and action"""
        if context_type not in self._handlers:
            self._handlers[context_type] = {}
        self._handlers[context_type][action] = handler

    def register_validator(
        self,
        context_type: ContextType,
        validation: ContextValidation
    ) -> None:
        """Register validation rules for a context type"""
        self._validators[context_type] = validation

    def validate_context(self, context: Context) -> List[str]:
        """Validate a context against its type's validation rules"""
        errors = []
        
        if context.type not in self._validators:
            return ["No validation rules found for context type"]

        validation = self._validators[context.type]

        # Check required parameters
        for param in validation.required_parameters:
            if param not in context.parameters:
                errors.append(f"Missing required parameter: {param}")

        # Check parameter types
        for param, expected_type in validation.parameter_types.items():
            if param in context.parameters:
                param_value = context.parameters[param]
                if not isinstance(param_value, eval(expected_type)):
                    errors.append(
                        f"Parameter {param} should be of type {expected_type}"
                    )

        # Check allowed actions
        if context.action not in validation.allowed_actions:
            errors.append(
                f"Action {context.action} not allowed for context type {context.type}"
            )

        return errors

    async def process_context(self, context: Context) -> ContextResponse:
        """Process a context and return the response"""
        start_time = time.time()
        
        try:
            # Validate context
            validation_errors = self.validate_context(context)
            if validation_errors:
                return ContextResponse(
                    context_id=context.id,
                    success=False,
                    error="\n".join(validation_errors),
                    processing_time=time.time() - start_time
                )

            # Store context
            self._context_store[context.id] = context

            # Update state
            context.state = ContextState.PROCESSING
            context.updated_at = datetime.utcnow()

            # Get handler
            if context.type not in self._handlers or context.action not in self._handlers[context.type]:
                return ContextResponse(
                    context_id=context.id,
                    success=False,
                    error=f"No handler found for {context.type}.{context.action}",
                    processing_time=time.time() - start_time
                )

            # Process context
            handler = self._handlers[context.type][context.action]
            result = await handler(context)

            # Update context state
            context.state = ContextState.COMPLETED
            context.updated_at = datetime.utcnow()

            return ContextResponse(
                context_id=context.id,
                success=True,
                result=result,
                processing_time=time.time() - start_time
            )

        except Exception as e:
            logger.exception("Error processing context")
            context.state = ContextState.FAILED
            context.updated_at = datetime.utcnow()
            
            return ContextResponse(
                context_id=context.id,
                success=False,
                error=str(e),
                processing_time=time.time() - start_time
            )

    def get_context(self, context_id: str) -> Optional[Context]:
        """Get a context by ID"""
        return self._context_store.get(context_id)

    def list_contexts(
        self,
        context_type: Optional[ContextType] = None,
        state: Optional[ContextState] = None
    ) -> List[Context]:
        """List contexts with optional filtering"""
        contexts = list(self._context_store.values())
        
        if context_type:
            contexts = [c for c in contexts if c.type == context_type]
        
        if state:
            contexts = [c for c in contexts if c.state == state]
            
        return contexts

    def delete_context(self, context_id: str) -> bool:
        """Delete a context by ID"""
        if context_id in self._context_store:
            del self._context_store[context_id]
            return True
        return False 