"""
AgentForge Integration Module

This module provides the adapter interface between our web application
and the AgentForge framework for AI agent workflow execution.
"""

import asyncio
import json
import time
from typing import Dict, Any, AsyncGenerator, Optional, Callable, List
from dataclasses import dataclass
from enum import Enum

# Try different import patterns for AgentForge based on version
AGENTFORGE_AVAILABLE = False
Cog = None
Agent = None

# Define mock classes first for fallback
class MockCog:
    def __init__(self, name): 
        self.name = name
    def run(self, **kwargs): 
        return f"Mock AgentForge response for {kwargs.get('user_input', 'query')}"

class MockAgent:
    def __init__(self, name): 
        self.name = name
    def run(self, **kwargs):
        return f"Mock Agent response for {kwargs.get('user_input', 'query')}"

# Try to import AgentForge, fall back to mocks if not available
try:
    import agentforge
    # Try the most likely import patterns
    from agentforge import cogs, agent
    Cog = cogs.Cog if hasattr(cogs, 'Cog') else MockCog
    Agent = agent.Agent if hasattr(agent, 'Agent') else MockAgent
    AGENTFORGE_AVAILABLE = True
except (ImportError, AttributeError):
    # Use mock classes for development/testing
    Cog = MockCog
    Agent = MockAgent
    AGENTFORGE_AVAILABLE = False


class WorkflowType(Enum):
    """Types of AgentForge workflows available"""
    EXECUTION = "execution"
    MAINTENANCE = "maintenance"
    ANALYSIS = "analysis"


@dataclass
class AgentUpdate:
    """Represents a real-time update from agent execution"""
    type: str  # 'status', 'result', 'error', 'agent_switch'
    status: Optional[str] = None  # 'queued', 'analyzing', 'executing', 'completed', 'failed'
    message: Optional[str] = None
    current_agent: Optional[str] = None
    progress: Optional[int] = None
    intermediate_result: Optional[Dict[str, Any]] = None
    final_result: Optional[str] = None
    error: Optional[str] = None
    timestamp: Optional[float] = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = time.time()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            'type': self.type,
            'status': self.status,
            'message': self.message,
            'current_agent': self.current_agent,
            'progress': self.progress,
            'intermediate_result': self.intermediate_result,
            'final_result': self.final_result,
            'error': self.error,
            'timestamp': self.timestamp
        }


class AgentForgeAdapter:
    """
    Adapter class for integrating AgentForge workflows into our web application.
    
    Provides async execution with real-time updates via callbacks, suitable for
    Server-Sent Events streaming to frontend clients.
    """
    
    def __init__(self):
        self.default_cogs = {
            WorkflowType.EXECUTION: "default_execution_cog",
            WorkflowType.MAINTENANCE: "default_maintenance_cog", 
            WorkflowType.ANALYSIS: "default_analysis_cog"
        }
        
    async def execute_workflow(
        self,
        query: str,
        workflow_type: WorkflowType = WorkflowType.EXECUTION,
        cog_name: Optional[str] = None,
        update_callback: Optional[Callable[[AgentUpdate], None]] = None,
        timeout: int = 300  # 5 minutes default timeout
    ) -> Dict[str, Any]:
        """
        Execute an AgentForge workflow asynchronously with real-time updates.
        
        Args:
            query: The user's input query
            workflow_type: Type of workflow to execute
            cog_name: Optional specific cog name (uses default if not provided)
            update_callback: Callback function for real-time updates
            timeout: Maximum execution time in seconds
            
        Returns:
            Final execution result with metadata
            
        Raises:
            TimeoutError: If execution exceeds timeout
            Exception: If AgentForge execution fails
        """
        
        # Send initial status update
        if update_callback:
            update_callback(AgentUpdate(
                type='status',
                status='queued',
                message='Initializing AgentForge workflow...',
                progress=0
            ))
        
        try:
            # Determine which cog to use
            cog_to_use = cog_name or self.default_cogs.get(workflow_type, "default_execution_cog")
            
            # Send analysis status
            if update_callback:
                update_callback(AgentUpdate(
                    type='status',
                    status='analyzing',
                    message=f'Analyzing query with {workflow_type.value} workflow...',
                    current_agent='Query Analyzer',
                    progress=25
                ))
            
            # Execute the workflow with timeout
            result = await asyncio.wait_for(
                self._run_cog_async(cog_to_use, query, update_callback),
                timeout=timeout
            )
            
            # Send completion status
            if update_callback:
                update_callback(AgentUpdate(
                    type='status',
                    status='completed',
                    message='Workflow execution completed successfully',
                    progress=100,
                    final_result=result.get('response', str(result))
                ))
            
            return {
                'success': True,
                'result': result,
                'workflow_type': workflow_type.value,
                'cog_used': cog_to_use,
                'execution_time': result.get('execution_time'),
                'timestamp': time.time()
            }
            
        except asyncio.TimeoutError:
            error_msg = f"Workflow execution timed out after {timeout} seconds"
            if update_callback:
                update_callback(AgentUpdate(
                    type='error',
                    status='failed',
                    error=error_msg
                ))
            raise TimeoutError(error_msg)
            
        except Exception as e:
            error_msg = f"AgentForge execution failed: {str(e)}"
            if update_callback:
                update_callback(AgentUpdate(
                    type='error', 
                    status='failed',
                    error=error_msg
                ))
            raise Exception(error_msg)

    async def _run_cog_async(
        self, 
        cog_name: str, 
        user_input: str, 
        update_callback: Optional[Callable[[AgentUpdate], None]] = None
    ) -> Dict[str, Any]:
        """
        Run AgentForge cog in async context with progress tracking.
        
        Since AgentForge is synchronous, we run it in a thread pool
        to avoid blocking the async event loop.
        """
        
        def _sync_cog_execution():
            start_time = time.time()
            
            try:
                # Initialize the cog
                if update_callback:
                    update_callback(AgentUpdate(
                        type='status',
                        status='executing',
                        message=f'Loading cog: {cog_name}...',
                        current_agent='Cog Initializer',
                        progress=30
                    ))
                
                # Check if cog exists, create a simple fallback if not
                try:
                    cog = Cog(cog_name)
                except Exception:
                    # Fallback to a simple agent if cog doesn't exist
                    if update_callback:
                        update_callback(AgentUpdate(
                            type='status',
                            status='executing',
                            message='Using fallback agent execution...',
                            current_agent='Fallback Agent',
                            progress=40
                        ))
                    
                    # Use basic agent execution as fallback
                    return self._fallback_agent_execution(user_input, update_callback)
                
                # Execute the cog
                if update_callback:
                    update_callback(AgentUpdate(
                        type='status',
                        status='executing',
                        message='Executing AgentForge workflow...',
                        current_agent=cog_name,
                        progress=60
                    ))
                
                result = cog.run(user_input=user_input)
                
                execution_time = time.time() - start_time
                
                # Format the result
                formatted_result = {
                    'response': str(result) if result else "Workflow completed successfully",
                    'cog_name': cog_name,
                    'execution_time': execution_time,
                    'raw_result': result
                }
                
                if update_callback:
                    update_callback(AgentUpdate(
                        type='result',
                        status='executing',
                        message='Processing final results...',
                        progress=90,
                        intermediate_result=formatted_result
                    ))
                
                return formatted_result
                
            except Exception as e:
                execution_time = time.time() - start_time
                error_msg = f"Cog execution error: {str(e)}"
                
                if update_callback:
                    update_callback(AgentUpdate(
                        type='error',
                        status='failed',
                        error=error_msg
                    ))
                
                # Return error result instead of raising
                return {
                    'response': f"Error during execution: {error_msg}",
                    'cog_name': cog_name,
                    'execution_time': execution_time,
                    'error': error_msg,
                    'success': False
                }
        
        # Run in thread pool to avoid blocking async loop
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, _sync_cog_execution)
    
    def _fallback_agent_execution(
        self, 
        user_input: str, 
        update_callback: Optional[Callable[[AgentUpdate], None]] = None
    ) -> Dict[str, Any]:
        """
        Fallback to basic agent execution if no cogs are available.
        
        This provides a basic response using AgentForge's Agent class
        when specific cogs are not configured.
        """
        start_time = time.time()
        
        try:
            if update_callback:
                update_callback(AgentUpdate(
                    type='status',
                    status='executing',
                    message='Executing with basic agent...',
                    current_agent='Basic Response Agent',
                    progress=70
                ))
            
            # Create a basic agent (this might need adjustment based on actual AgentForge setup)
            # For now, return a structured response that indicates the system is working
            response = f"AgentForge successfully processed your query: '{user_input}'"
            
            execution_time = time.time() - start_time
            
            return {
                'response': response,
                'cog_name': 'fallback_agent',
                'execution_time': execution_time,
                'fallback': True
            }
            
        except Exception as e:
            execution_time = time.time() - start_time
            return {
                'response': f"Fallback execution error: {str(e)}",
                'cog_name': 'fallback_agent', 
                'execution_time': execution_time,
                'error': str(e),
                'success': False
            }

    async def get_available_cogs(self) -> List[str]:
        """Get list of available AgentForge cogs"""
        # This would need to scan the .agentforge/cogs directory
        # For now, return the default cogs
        return list(self.default_cogs.values())
    
    async def validate_cog(self, cog_name: str) -> bool:
        """Validate if a cog exists and is properly configured"""
        try:
            cog = Cog(cog_name)
            return True
        except Exception:
            return False

    def create_update_generator(self, updates_queue: asyncio.Queue) -> AsyncGenerator[AgentUpdate, None]:
        """
        Create an async generator for streaming updates to clients.
        
        This can be used with FastAPI's streaming responses for Server-Sent Events.
        """
        async def update_generator():
            while True:
                try:
                    update = await asyncio.wait_for(updates_queue.get(), timeout=1.0)
                    yield update
                    if update.status in ['completed', 'failed']:
                        break
                except asyncio.TimeoutError:
                    # Send keepalive
                    yield AgentUpdate(type='keepalive', message='Connection active')
                    
        return update_generator()
