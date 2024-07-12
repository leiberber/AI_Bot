import requests

class OpenAI:
    def __init__(self, api_key, base_url):
        self.api_key = api_key
        self.base_url = base_url

    def chat_completions_create(self, model, messages, stream=False, max_tokens=256, temperature=0.8, presence_penalty=1.1, top_p=0.8):
        url = f"{self.base_url}/chat/completions"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {
            "model": model,
            "messages": messages,
            "stream": stream,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "presence_penalty": presence_penalty,
            "top_p": top_p,
        }
        response = requests.post(url, json=payload, headers=headers)
        return response.json()

    def embeddings_create(self, model, input):
        url = f"{self.base_url}/embeddings"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {"model": model, "input": input}
        response = requests.post(url, json=payload, headers=headers)
        return response.json()