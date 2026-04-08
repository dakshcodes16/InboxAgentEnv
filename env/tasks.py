from typing import Dict, Any

def get_extract_code_state() -> Dict[str, Any]:
    return {
        "emails": [
            {
                "id": "email_1", 
                "sender": "security@company.com", 
                "subject": "Your Login Code", 
                "body": "Your 6-digit security code is 654321. Do not share it.", 
                "archived": False,
                "flagged": False
            }
        ],
        "contacts": [],
        "sent_emails": []
    }

def get_inbox_triage_state() -> Dict[str, Any]:
    return {
        "emails": [
            {
                "id": "newsletter_1", 
                "sender": "news@weekly.com", 
                "subject": "Weekly Tech Newsletter", 
                "body": "Here is the news...", 
                "archived": False,
                "flagged": False
            },
            {
                "id": "invoice_1", 
                "sender": "billing@vendor.com", 
                "subject": "URGENT: Invoice Overdue", 
                "body": "Please pay 500 USD.", 
                "archived": False, 
                "flagged": False
            },
            {
                "id": "meeting_1", 
                "sender": "boss@example.com", 
                "subject": "Meeting Request", 
                "body": "Can we meet tomorrow?", 
                "archived": False,
                "flagged": False
            }
        ],
        "contacts": [],
        "sent_emails": []
    }

def get_meeting_scheduler_state() -> Dict[str, Any]:
    return {
        "emails": [
            {
                "id": "meet_req", 
                "sender": "client@example.com", 
                "subject": "Let's sync up", 
                "body": "I am in Tokyo. Let's meet at 9:00 AM my time. Can you suggest the time?", 
                "archived": False,
                "flagged": False
            }
        ],
        "contacts": [
            {"name": "Client Moto", "email": "client@example.com", "timezone": "Asia/Tokyo"}
        ],
        "sent_emails": []
    }
