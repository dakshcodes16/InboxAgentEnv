import os
import json
import logging
from openai import OpenAI
from env.environment import InboxAgentEnv
from env.models import Action
from env.tasks import get_extract_code_state, get_inbox_triage_state, get_meeting_scheduler_state

# We disable httpx logging as it gets verbose
logging.getLogger("httpx").setLevel(logging.WARNING)

def run_inference():
    client = OpenAI(
        base_url=os.environ.get("API_BASE_URL"),
        api_key=os.environ.get("HF_TOKEN") or os.environ.get("OPENAI_API_KEY") or "dummy_key"
    )
    model_name = os.environ.get("MODEL_NAME", "gpt-3.5-turbo")
    
    tasks = [
        {"name": "extract_code", "state": get_extract_code_state},
        {"name": "inbox_triage", "state": get_inbox_triage_state},
        {"name": "meeting_scheduler", "state": get_meeting_scheduler_state}
    ]
    
    for task in tasks:
        task_name = task["name"]
        env = InboxAgentEnv(initial_state=task["state"](), task_name=task_name)
        obs = env.reset()
        
        print(f"[START] task={task_name} env=inbox_agent model={model_name}")
        
        step_n = 1
        done = False
        score = 0.0
        rewards = []
        
        system_prompt = (
            "You are an AI Email Assistant managing a corporate inbox. "
            "You only reply with a valid JSON format specifying the action to take. "
            "Available actions: 'list_emails', 'read_email', 'archive_email', 'flag_email', 'search_contacts', 'send_email'."
        )
        messages = [{"role": "system", "content": system_prompt}]
        
        try:
            for i in range(10): # Max 10 steps
                prompt = (
                    f"Current Environment State:\n{json.dumps(obs.state, default=str)}\n\n"
                    f"Last output: {obs.output}\nLast error: {obs.error}\n\n"
                    "Output a strictly formatted JSON specifying the next action. Example: "
                    '{"action_type": "send_email", "params": {"to": "client@example.com", "body": "Confirmed."}}'
                )
                messages.append({"role": "user", "content": prompt})
                
                try:
                    response = client.chat.completions.create(
                        model=model_name,
                        messages=messages,
                        response_format={"type": "json_object"}
                    )
                    content = response.choices[0].message.content
                    messages.append({"role": "assistant", "content": content})
                    
                    action_data = json.loads(content)
                    action = Action(**action_data)
                    action_str = f"{action.action_type}({action.params})"
                except Exception as e:
                    action_str = f"parsing_or_api_error"
                    action = Action(action_type="list_emails", params={}) # fallback to something safe
                    obs.error = f"Agent API/parsing failed: {str(e)}"
                    
                obs, reward = env.step(action)
                done = reward.is_done
                score = reward.score
                rewards.append(score)
                
                print(f"[STEP] step={step_n} action={action_str} reward={score:.2f} done={str(done).lower()} error={obs.error or 'null'}")
                step_n += 1
                
                if done:
                    break
        except Exception as e:
            print(f"[STEP] step={step_n} action=error reward=0.00 done=true error={str(e)}")
            
        success = done and score >= 0.5
        rewards_str = ",".join([f"{r:.2f}" for r in rewards])
        print(f"[END] success={str(success).lower()} steps={step_n - 1} score={score:.2f} rewards={rewards_str}")

if __name__ == "__main__":
    run_inference()
