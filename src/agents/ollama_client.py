from src.models.image_description import ImageStroyTelling

import ollama
import os

class OllamaClient:
    """Ollama client for image description generation."""

    def __init__(self):
        ollama_host = os.getenv("OLLAMA_HOST", "http://ollama:11434")
        self.client = ollama.Client(host=ollama_host)
        self.model = "LLaVA-LLaMA3"
        self.client.pull(self.model)  # pull model, does not persist between restarts!

    def get_img_story(self, filepath):
        with open("src/prompts/story_telling.txt", "r") as f:
            prompt = f.read()
        with open(filepath, 'rb') as file:
            image_bytes = file.read()
            response = self.client.chat(
                model=self.model,
                messages=[
                    {
                        'role': 'user',
                        'content': prompt,
                        'images': [image_bytes],
                    }
                ],
                format=ImageStroyTelling.model_json_schema()
            )
        return response['message']['content']