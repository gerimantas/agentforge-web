"""
Agent execution API endpoints

Handles AgentForge workflow execution and session management.
"""

import asyncio
import json
import time
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse
from typing import List, Dict, Any
from sqlalchemy.orm import Session

from ..schemas.agent import AgentRequest, AgentResponse, AgentSessionResponse
from ..agentforge import AgentForgeAdapter, WorkflowType, AgentUpdate
from ..models import AgentSession, User
from ..api.deps import get_db, get_current_user

router = APIRouter()

# Initialize AgentForge adapter
agent_adapter = AgentForgeAdapter()


@router.post("/execute", response_model=Dict[str, Any])
async def execute_agent(
    request: AgentRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Execute AgentForge workflow with real-time streaming"""
    
    # Create agent session record
    session = AgentSession(
        user_id=current_user.id,
        query=request.query,
        workflow_type=request.workflow_type,
        status="queued"
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    
    # Start background execution
    background_tasks.add_task(
        _execute_agent_workflow, 
        session.id, 
        request, 
        db
    )
    
    return {
        "session_id": session.id,
        "status": "queued",
        "message": "Agent execution started"
    }


@router.get("/execute/{session_id}/stream")
async def stream_agent_execution(
    session_id: int,
    db: Session = Depends(get_db)
):
    """Stream real-time updates for agent execution via Server-Sent Events"""
    
    # For development - simplified auth (using mock user ID = 1)
    # TODO: In production, implement proper token verification
    session = db.query(AgentSession).filter(
        AgentSession.id == session_id,
        AgentSession.user_id == 1  # Mock user ID
    ).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    async def event_generator():
        """Generate Server-Sent Events for real-time updates"""
        last_update_time = time.time()
        
        while True:
            # Refresh session from database
            db.refresh(session)
            
            # Check if execution is complete
            if session.status in ["completed", "failed"]:
                # Send final update
                update_data = {
                    "type": "status",
                    "status": session.status,
                    "progress": session.progress or 100,
                    "message": "Execution completed" if session.status == "completed" else "Execution failed",
                    "final_result": session.final_result,
                    "error_message": session.error_message
                }
                yield f"data: {json.dumps(update_data)}\n\n"
                break
            
            # Send progress update
            update_data = {
                "type": "status", 
                "status": session.status,
                "progress": session.progress or 0,
                "current_agent": session.current_agent,
                "message": f"Status: {session.status}"
            }
            yield f"data: {json.dumps(update_data)}\n\n"
            
            # Send keepalive every 30 seconds
            if time.time() - last_update_time > 30:
                yield f"data: {json.dumps({'type': 'keepalive'})}\n\n"
                last_update_time = time.time()
            
            await asyncio.sleep(2)  # Check every 2 seconds
    
    return StreamingResponse(
        event_generator(),
        media_type="text/plain",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*",
        }
    )


async def _execute_agent_workflow(
    session_id: int, 
    request: AgentRequest, 
    db: Session
):
    """Background task to execute AgentForge workflow"""
    
    session = db.query(AgentSession).filter(AgentSession.id == session_id).first()
    if not session:
        return
    
    try:
        # Update session status
        session.status = "analyzing"
        session.started_at = datetime.utcnow()
        db.commit()
        
        # Define update callback to persist progress
        def update_callback(update: AgentUpdate):
            nonlocal session, db
            db.refresh(session)
            
            session.status = update.status or session.status
            session.current_agent = update.current_agent or session.current_agent
            session.progress = update.progress or session.progress
            
            if update.intermediate_result:
                # Store intermediate results
                current_results = session.intermediate_results or []
                current_results.append(update.intermediate_result)
                session.intermediate_results = current_results
            
            if update.final_result:
                session.final_result = update.final_result
                
            if update.error:
                session.error_message = update.error
                session.status = "failed"
            
            db.commit()
        
        # Execute workflow
        workflow_type = WorkflowType(request.workflow_type)
        result = await agent_adapter.execute_workflow(
            query=request.query,
            workflow_type=workflow_type,
            cog_name=request.cog_name,
            update_callback=update_callback,
            timeout=request.timeout or 300
        )
        
        # Update session with final result
        session.status = "completed"
        session.final_result = result.get("result", {}).get("response", "No response")
        session.completed_at = datetime.utcnow()
        session.progress = 100
        
    except Exception as e:
        # Handle execution errors
        session.status = "failed"
        session.error_message = str(e)
        session.completed_at = datetime.utcnow()
        
    finally:
        db.commit()


@router.get("/sessions", response_model=List[AgentSessionResponse])
async def get_user_sessions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 50
):
    """Get user's agent execution history"""
    
    sessions = db.query(AgentSession).filter(
        AgentSession.user_id == current_user.id
    ).offset(skip).limit(limit).all()
    
    return sessions

@router.get("/sessions/{session_id}", response_model=AgentSessionResponse)
async def get_session_detail(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get detailed information about a specific session"""
    
    session = db.query(AgentSession).filter(
        AgentSession.id == session_id,
        AgentSession.user_id == current_user.id
    ).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
        
    return session


@router.delete("/sessions/{session_id}")
async def delete_session(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a specific session"""
    
    session = db.query(AgentSession).filter(
        AgentSession.id == session_id,
        AgentSession.user_id == current_user.id
    ).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    db.delete(session)
    db.commit()
    
    return {"message": "Session deleted successfully"}


@router.get("/cogs")
async def get_available_cogs():
    """Get list of available AgentForge cogs"""
    cogs = await agent_adapter.get_available_cogs()
    return {"cogs": cogs}


@router.get("/health")
async def agent_health_check():
    """Health check for AgentForge integration"""
    return {
        "status": "healthy",
        "agentforge_available": agent_adapter.AGENTFORGE_AVAILABLE if hasattr(agent_adapter, 'AGENTFORGE_AVAILABLE') else False,
        "timestamp": time.time()
    }
