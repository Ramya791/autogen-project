from gpt4all import GPT4All

class GPT4AllLocalModel:
    def __init__(self, model_path):
        model_name = "mistral-7b-openorca.Q4_K_M.gguf"
        self.model = GPT4All(model_name=model_name, model_path=model_path, allow_download=False)

    def chat(self, prompt: str) -> str:
        return self.model.generate(prompt)
