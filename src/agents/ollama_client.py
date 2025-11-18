from src.models.image_description import ImageStroyTelling

import ollama
import os
import requests
import base64

class OllamaClient:
    """Ollama client for image description generation."""

    def __init__(self):
        #ollama_host = os.getenv("OLLAMA_HOST", "http://ollama:11434")
        #self.client = ollama.Client(host=ollama_host)
        self.model = "LLaVA-LLaMA3"
        #self.client.pull(self.model)  # pull model, does not persist between restarts!

    def get_img_story(self, filepath):
        with open("src/prompts/story_telling.txt", "r") as f:
            prompt = f.read()
        with open(filepath, 'rb') as file:
            image_bytes = file.read()
        
        image_b64 = base64.b64encode(image_bytes).decode('utf-8')
        response = requests.post(
            "http://ollama:11434/api/generate", # Inside docker network use "ollama:11434", from host use "localhost:11435"
            json={
                "model": self.model,
                "messages": [
                    {
                        'role': 'user',
                        'content': prompt,
                        'images': [image_b64],
                    }
                    ],
            "format": ImageStroyTelling.model_json_schema(),
            "stream": False
            }
        
        )

        if response.status_code != 200:
            raise Exception(f"Request failed with status code {response.status_code}: {response.text}")
        # Attempt to decode JSON
        try:
            return response.json()['response']
        except ValueError as e:
            raise Exception(f"Failed to decode JSON: {e} - Response: {response}")