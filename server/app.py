from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
from env.environment import InboxAgentEnv
from env.tasks import get_extract_code_state, get_inbox_triage_state, get_meeting_scheduler_state
from env.models import Action

app = FastAPI()

current_env = None

class ResetRequest(BaseModel):
    task_id: Optional[str] = None
    task_name: Optional[str] = None # OpenEnv might use task_name or task_id

@app.post("/reset")
def reset_env(req: Optional[ResetRequest] = None):
    global current_env
    task_id = "extract_code"
    if req:
        task_id = req.task_id or req.task_name or "extract_code"
    
    if task_id == "extract_code":
        state = get_extract_code_state()
    elif task_id == "inbox_triage":
        state = get_inbox_triage_state()
    elif task_id == "meeting_scheduler":
        state = get_meeting_scheduler_state()
    else:
        # Fallback to easy if missing
        state = get_extract_code_state()
        task_id = "extract_code"
        
    current_env = InboxAgentEnv(initial_state=state, task_name=task_id)
    obs = current_env.reset()
    return obs.dict()

@app.post("/step")
def step_env(action: Action):
    global current_env
    if not current_env:
        # Auto-initialize if stepping before reset
        reset_env(ResetRequest(task_id="extract_code"))
        
    obs, reward = current_env.step(action)
    return {"observation": obs.dict(), "reward": reward.dict()}

@app.get("/state")
def get_state():
    global current_env
    if not current_env:
        return {}
    return current_env.state()

@app.get("/")
def read_root():
    return {"status": "ok", "message": "InboxAgentEnv API"}

def main():
    import uvicorn
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()

