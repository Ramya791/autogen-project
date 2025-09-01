from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from gpt4all_local_model import GPT4AllLocalModel

app = FastAPI()

# Allow Studio frontend to call this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Path to the folder where your .gguf file is located
model_path = "C:/Users/sri79/autogen-project"
local_llm = GPT4AllLocalModel(model_path)

@app.post("/v1/chat/completions")
async def chat(request: Request):
    body = await request.json()
    messages = body.get("messages", [])
    if not messages:
        return {"error": "No messages provided."}

    # Build full prompt
    prompt = "\n".join([m["content"] for m in messages])
    response = local_llm.chat(prompt)

    return {
        "id": "chatcmpl-local",
        "object": "chat.completion",
        "choices": [{
            "message": {
                "role": "assistant",
                "content": response
            }
        }],
        "usage": {}
    }
