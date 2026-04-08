from typing import Any, Dict, Tuple
from env.models import Action, Observation, Reward

class InboxAgentEnv:
    def __init__(self, initial_state: Dict[str, Any], task_name: str):
        self.initial_state = initial_state
        self.state_data = initial_state.copy()
        self.task_name = task_name
        self.current_score = 0.0
        self.history = []

    def reset(self) -> Observation:
        self.state_data = self.initial_state.copy()
        self.current_score = 0.0
        self.history = []
        return Observation(state=self.state_data, output="Environment reset.")

    def state(self) -> Dict[str, Any]:
        return self.state_data

    def step(self, action: Action) -> Tuple[Observation, Reward]:
        action_type = action.action_type
        params = action.params
        
        output = None
        error = None
        score_diff = 0.0
        is_done = False
        message = ""

        try:
            if action_type == "list_emails":
                emails = [
                    {"id": e["id"], "sender": e["sender"], "subject": e["subject"], "archived": e.get("archived", False), "flagged": e.get("flagged", False)}
                    for e in self.state_data.get("emails", []) if not e.get("archived", False)
                ]
                output = emails
                
            elif action_type == "read_email":
                email_id = params.get("id")
                email = next((e for e in self.state_data.get("emails", []) if e["id"] == email_id), None)
                if email:
                    output = email
                    # partial reward logic example for task 1
                    if self.task_name == "extract_code" and "Login Code" in email["subject"]:
                        if "read_correct_email" not in self.history:
                            score_diff += 0.2
                            self.history.append("read_correct_email")
                else:
                    error = f"Email {email_id} not found."
                    
            elif action_type == "send_email":
                to = params.get("to")
                body = params.get("body")
                self.state_data.setdefault("sent_emails", []).append({"to": to, "body": body})
                output = "Email sent."
                
                if self.task_name == "meeting_scheduler":
                    if to == "client@example.com" and "09:00" in body: 
                         score_diff += 0.8
                         is_done = True
                         message = "Successfully scheduled meeting."
                         
                if self.task_name == "extract_code":
                    if "654321" in body: 
                        score_diff += 0.8
                        is_done = True
                        message = "Successfully extracted security code."
                        
            elif action_type == "archive_email":
                email_id = params.get("id")
                email = next((e for e in self.state_data.get("emails", []) if e["id"] == email_id), None)
                if email:
                    email["archived"] = True
                    output = f"Email {email_id} archived."
                    
                    if self.task_name == "inbox_triage" and email_id == "newsletter_1":
                        if "archived_newsletter" not in self.history:
                            score_diff += 0.3
                            self.history.append("archived_newsletter")
                else:
                    error = f"Email {email_id} not found."
                    
            elif action_type == "flag_email":
                email_id = params.get("id")
                email = next((e for e in self.state_data.get("emails", []) if e["id"] == email_id), None)
                if email:
                    email["flagged"] = True
                    output = f"Email {email_id} flagged."
                    
                    if self.task_name == "inbox_triage" and email_id == "invoice_1":
                        if "flagged_invoice" not in self.history:
                            score_diff += 0.3
                            self.history.append("flagged_invoice")
                else:
                    error = f"Email {email_id} not found."

            elif action_type == "search_contacts":
                name = params.get("name", "").lower()
                contacts = [c for c in self.state_data.get("contacts", []) if name in c["name"].lower()]
                output = contacts

            else:
                error = f"Unknown action: {action_type}"
                
        except Exception as e:
            error = str(e)
            
        if self.task_name == "inbox_triage":
             has_archived = "archived_newsletter" in self.history
             has_flagged = "flagged_invoice" in self.history
             has_replied = any(e.get("to") == "boss@example.com" and "confirmed" in e.get("body", "").lower() for e in self.state_data.get("sent_emails", []))
             
             if not is_done and has_replied and "replied_boss" not in self.history:
                  score_diff += 0.4
                  self.history.append("replied_boss")
                  
             if has_archived and has_flagged and has_replied:
                  is_done = True
                  message = "Inbox triage complete."

        self.current_score += score_diff
        obs = Observation(state=self.state_data, output=output, error=error)
        reward = Reward(score=self.current_score, is_done=is_done, message=message)
        
        return obs, reward
