from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "InboxAgentEnv running. Port exposed for Hugging Face Spaces validation."}
