import os
from openai import OpenAI
from typing import List, Dict, Optional
from jiuzhao.config import load_config, get_model_config

class LLMClient:
    def __init__(self):
        self.config = load_config()
        self.model_name = self.config.get("current_model")
        self.model_config = get_model_config(self.model_name)
        
        if not self.model_config:
            raise ValueError(f"Model configuration for '{self.model_name}' not found.")

        api_key = self.model_config.get("api_key")
        if not api_key or api_key == "ollama":
            api_key = os.getenv("OPENAI_API_KEY", "ollama")

        self.client = OpenAI(
            base_url=self.model_config.get("base_url"),
            api_key=api_key
        )

    def chat(self, messages: List[Dict[str, str]]) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=0.2,
                max_tokens=4096
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"LLM Error: {str(e)}"
