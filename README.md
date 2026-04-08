# InboxAgentEnv

## Goal and Motivation
The InboxAgentEnv is a professional email assistant environment designed to evaluate AI models in real-world corporate inbox triage, reading, and scheduling tasks. It represents tasks human workers perform daily—reading correspondence, archiving irrelevant information, flagging urgent messages, and organizing schedules across time zones.

## Action and Observation Spaces
**Action Space**:
- `list_emails`: Retrieve a list of all non-archived emails in the inbox.
- `read_email(id)`: Read the comprehensive contents of an email.
- `send_email(to, body)`: Draft and output a response email to a given address.
- `archive_email(id)`: Archive a given email to remove it from the primary sight.
- `flag_email(id)`: Flag a message as urgent.
- `search_contacts(name)`: Query the user's contact book.

**Observation Space**:
- `state`: The underlying mock database representation containing the email array and contact list.
- `output`: Returns the result of the last action executed (e.g. email payload, search result).
- `error`: Displays errors if illegal parameter types or incorrect IDs are invoked.

## Tasks
1. **Extract Code (Easy)**: The agent must find an email titled 'Your Login Code' and formulate a response that correctly regurgitates the 6-digit security code.
2. **Inbox Triage (Medium)**: The agent must systematically traverse a larger inbox, properly archive a non-important newsletter, flag an urgent invoice, and reply to a meeting request.
3. **Meeting Scheduler (Hard)**: The agent must parse an ambiguous meeting request ("Let's meet at 9 AM my time"), discover the user's timezone by searching the contact book, and reply suggesting the exact equivalent meeting time mapped to their respective locale.

## Setup and Usage Instructions
**Prerequisites:**
- Make sure you are using Python 3.10+
- Install dependencies: `pip install -r requirements.txt`

**Running the Baseline Validation:**
The environment baseline can be locally validated using the provided baseline inference script.
```bash
export OPENAI_API_KEY="your-api-key"
export MODEL_NAME="gpt-4o"
python inference.py
```

## Baseline Performance Scores
*Pending initialization. The baseline script validates that typical models like GPT-4o are capable of reaching `0.8 - 1.0` scores for all three difficulties when initialized with a 10-step limitation constraint.*
