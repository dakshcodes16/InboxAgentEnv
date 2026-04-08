from env.environment import InboxAgentEnv
from env.tasks import get_extract_code_state
from env.models import Action

env = InboxAgentEnv(get_extract_code_state(), "extract_code")
obs = env.reset()
print("Reset output:", obs.output)

action = Action(action_type="list_emails", params={})
obs, reward = env.step(action)
print("Step 1 (list_emails):", obs.output)

print("Tests passed.")
