from gpt4all import GPT4All

model = GPT4All(model_name="mistral-7b-openorca.Q4_K_M.gguf", model_path=".")
print("Model loaded successfully.")

response = model.generate(
    "Tell me a fun fact about space.",
    max_tokens=100,
    temp=0.7
)
print("Model response:", response)
