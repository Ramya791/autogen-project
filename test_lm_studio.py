from openai import OpenAI

client = OpenAI(base_url="http://127.0.0.1:1234/v1", api_key="lm-studio")
resp = client.chat.completions.create(
    model="mistral-7b-instruct-v0.1",
    messages=[{"role": "user", "content": "Say hello in one sentence."}],
    temperature=0.2,
    max_tokens=32,
)
print(resp.choices[0].message.content)
