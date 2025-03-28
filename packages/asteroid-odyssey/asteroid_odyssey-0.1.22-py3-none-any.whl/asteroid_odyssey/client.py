from typing import Optional, Dict, Any, List, Union, Callable, Tuple
from uuid import UUID
import logging
import time
from enum import Enum
import os

from .api.generated.asteroid_agents_api_client.models import (
    CreateWorkflowRequest,
    WorkflowExecution,
    ExecutionStatus,
    Execution,
    WorkflowExecutionRequest,
    Agent,
    ResultSchema,
    CreateWorkflowRequestFields,
    CreateWorkflowRequestProvider
)
from .api.generated.asteroid_agents_api_client.client import Client as ApiClient
from .api.generated.asteroid_agents_api_client.api.execution.get_execution import sync_detailed as get_execution
from .api.generated.asteroid_agents_api_client.api.agent.get_agents import sync_detailed as asteroid_get_agents
from .api.generated.asteroid_agents_api_client.api.workflow.create_workflow import sync_detailed as create_workflow
from .api.generated.asteroid_agents_api_client.api.workflow.get_agent_workflow_executions import sync_detailed as get_agent_workflow_executions
from .api.generated.asteroid_agents_api_client.api.workflow.execute_workflow import sync_detailed as execute_workflow
logger = logging.getLogger(__name__)

class ExecutionTerminalState(Enum):
    """Terminal states for an execution"""
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    ERROR = "error"

agent_name = "iris"

class ExecutionResult:
    """Wrapper class for execution results"""
    def __init__(self, execution: Execution):
        self.execution_id = execution.id
        self.status = execution.status
        self.result = execution.result
        self.error = execution.error if hasattr(execution, 'error') else None
        self.created_at = execution.created_at
        self.completed_at = execution.completed_at if hasattr(execution, 'completed_at') else None

class AsteroidClient:
    """
    A high-level client for interacting with the Asteroid API.
    """
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        verify_ssl: bool = True
    ):
        """
        Initialize the Asteroid client.

        Args:
            api_key: API key for authentication. If not provided, will look for ASTEROID_API_KEY env var
            base_url: Base URL for the API. Defaults to production URL if not specified
            verify_ssl: Whether to verify SSL certificates. Defaults to True
        """
        self.api_key = api_key or os.getenv("ASTEROID_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API key is required. Either pass it directly or set ASTEROID_API_KEY environment variable"
            )

        self.base_url = base_url or "https://odyssey.asteroid.ai/api/v1"
        # Initialize API client
        self.client = ApiClient(
            base_url=self.base_url,
            verify_ssl=verify_ssl,
            headers={"X-Asteroid-Agents-Api-Key": f"{self.api_key}"}
        )

    def get_agents(self) -> List["Agent"]:
        """
        Get list of available agents.
        
        Returns:
            List of agent details
        """
        try:
            result = asteroid_get_agents(client=self.client)
            if result.parsed is None:
                raise ValueError("No agents were returned from the API")
            if not isinstance(result.parsed, list):
                raise ValueError(f"The result is not of type list, it is of type: {type(result.parsed)}")
            return result.parsed
        except Exception as e:
            logger.error(f"Failed to get agents: {str(e)}")
            raise

    def create_workflow(
        self, 
        workflow_name: str,
        start_url: str,
        prompt: str,
        result_schema: Optional[ResultSchema] = None
    ) -> str:
        """
        Create a new workflow for an agent.

        Args:
            workflow_name: Name of the workflow
            start_url: Starting URL for the workflow
            prompt: Prompt for the workflow
            result_schema: Optional custom result schema. Currently not fully supported.

        Returns:
            Workflow ID

        Warning:
            Custom result schemas are not fully supported yet and will be added in a future update.
            Currently, only the default schema will be used regardless of input.
        """
        if result_schema is not None:
            logger.warning("Custom result schemas are not fully supported yet and will be ignored. Using default schema.")

        # Default result schema
        default_schema = ResultSchema()
        default_schema.additional_properties = {
            "properties": {
                "explanation": {
                    "description": "Detailed explanation of the result",
                    "type": "string"
                },
                "success": {
                    "description": "Whether the operation was successful",
                    "type": "boolean"
                }
            },
            "required": [
                "explanation",
                "success"
            ],
            "type": "object"
        }
        
        if result_schema is None:
            result_schema = default_schema

        try:
            fields = CreateWorkflowRequestFields()
            fields.additional_properties = {
                "workflow_name": workflow_name,
                "start_url": start_url
            }

            request = CreateWorkflowRequest(
                name=workflow_name,
                result_schema=result_schema,
                fields=fields,
                prompts=[prompt],
                provider=CreateWorkflowRequestProvider.OPENAI
            )

            result = create_workflow(
                agent_name=agent_name,
                body=request,
                client=self.client
            ).parsed
            if not isinstance(result, str):
                raise ValueError("The result is not of type str")
            return result
        except Exception as e:
            logger.error(f"Failed to create workflow: {str(e)}")
            raise

    def execute_workflow(
        self,
        workflow_id: UUID,
        execution_params: Dict[str, Any]
    ) -> str:
        """
        Execute an existing workflow.

        Args:
            workflow_id: ID of workflow to execute
            execution_params: Parameters for workflow execution

        Returns:
            Execution ID
        """
        try:
            # Convert execution_params to WorkflowExecutionRequest using from_dict
            request_body = WorkflowExecutionRequest.from_dict(execution_params)
            
            result = execute_workflow(
                workflow_id=workflow_id,
                body=request_body,
                client=self.client
            ).parsed
            if not isinstance(result, str):
                raise ValueError("The result is not of type str")
            return result
        except Exception as e:
            logger.error(f"Failed to execute workflow: {str(e)}")
            raise

    def get_workflow_executions(self) -> List[WorkflowExecution]:
        """
        Get list of workflow executions.

        Returns:
            List of workflow executions
        """
        try:
            result = get_agent_workflow_executions(
                agent_name=agent_name,
                client=self.client
            ).parsed
            if not isinstance(result, List):
                raise ValueError("The result is not of type List")
            return result
        except Exception as e:
            logger.error(f"Failed to get workflow executions: {str(e)}")
            raise

    def get_execution(self, execution_id: str) -> Execution:
        """
        Get the full execution details.

        Args:
            execution_id: ID of the execution to retrieve

        Returns:
            Execution object with full details
        """
        try:
            result = get_execution(id=UUID(execution_id), client=self.client).parsed
            if not isinstance(result, Execution):
                raise ValueError("The result is not of type Execution")
            return result
        except Exception as e:
            logger.error(f"Failed to get execution: {str(e)}")
            raise

    def get_execution_status(self, execution_id: str) -> ExecutionStatus:
        """
        Get the current status of an execution.

        Args:
            execution_id: ID of the execution to check

        Returns:
            Current execution status
        """
        execution = self.get_execution(execution_id)
        if not isinstance(execution.status, ExecutionStatus):
            raise ValueError("The execution status is not of type ExecutionStatus")
        return execution.status

    def get_execution_result(self, execution_id: str) -> ExecutionResult:
        """
        Get the result of an execution.

        Args:
            execution_id: ID of the execution to get results for

        Returns:
            ExecutionResult object containing status, result, and other metadata

        Raises:
            ValueError: If execution doesn't exist or hasn't completed
        """
        execution = self.get_execution(execution_id)
        return ExecutionResult(execution)

    def wait_for_execution(
        self,
        execution_id: str,
        polling_interval: float = 1.0,
        timeout: Optional[float] = None,
        status_callback: Optional[Callable[[ExecutionStatus], None]] = None
    ) -> ExecutionStatus:
        """
        Wait for an execution to reach a terminal state.

        Args:
            execution_id: ID of the execution to wait for
            polling_interval: Time in seconds between status checks
            timeout: Maximum time in seconds to wait. None means wait indefinitely
            status_callback: Optional callback function that will be called with each status update

        Returns:
            Final execution status

        Raises:
            TimeoutError: If timeout is reached before execution reaches terminal state
            ValueError: If execution_id is invalid
        """
        start_time = time.time()
        last_status = None

        while True:
            # Check if we've exceeded timeout
            if timeout and (time.time() - start_time) > timeout:
                raise TimeoutError(f"Execution {execution_id} did not complete within {timeout} seconds")

            # Get current status
            current_status = self.get_execution_status(execution_id)

            # Call status callback if status has changed
            if status_callback and current_status != last_status:
                status_callback(current_status)
            last_status = current_status

            # Check if we've reached a terminal state
            if current_status.status.value in [state.value for state in ExecutionTerminalState]:
                return current_status

            # Wait before next check
            time.sleep(polling_interval)

    def wait_for_execution_result(
        self,
        execution_id: str,
        polling_interval: float = 1.0,
        timeout: Optional[float] = None,
        status_callback: Optional[Callable[[ExecutionStatus], None]] = None
    ) -> ExecutionResult:
        """
        Wait for an execution to complete and get its result.

        Args:
            execution_id: ID of the execution to wait for
            polling_interval: Time in seconds between status checks
            timeout: Maximum time in seconds to wait. None means wait indefinitely
            status_callback: Optional callback function that will be called with each status update

        Returns:
            ExecutionResult object containing final status, result, and other metadata

        Raises:
            TimeoutError: If timeout is reached before execution completes
            ValueError: If execution_id is invalid
        """
        # Wait for execution to reach terminal state
        final_status = self.wait_for_execution(
            execution_id=execution_id,
            polling_interval=polling_interval,
            timeout=timeout,
            status_callback=status_callback
        )

        # Get the final result
        result = self.get_execution_result(execution_id)

        # If execution failed, include error information in logs
        if final_status in [ExecutionTerminalState.FAILED, ExecutionTerminalState.ERROR]:
            logger.error(f"Execution {execution_id} failed with error: {result.error}")

        return result

    def execute_workflow_and_get_result(
        self,
        workflow_id: UUID,
        execution_params: Dict[str, Any],
        polling_interval: float = 1.0,
        timeout: Optional[float] = None,
        status_callback: Optional[Callable[[ExecutionStatus], None]] = None
    ) -> ExecutionResult:
        """
        Execute a workflow and wait for its result.

        Args:
            workflow_id: ID of workflow to execute
            execution_params: Parameters for workflow execution
            polling_interval: Time in seconds between status checks
            timeout: Maximum time in seconds to wait. None means wait indefinitely
            status_callback: Optional callback function that will be called with each status update

        Returns:
            ExecutionResult object containing final status, result, and other metadata
        """
        # Start execution
        execution_id = self.execute_workflow(workflow_id, execution_params)

        # Wait for result
        return self.wait_for_execution_result(
            execution_id=execution_id,
            polling_interval=polling_interval,
            timeout=timeout,
            status_callback=status_callback
        )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
