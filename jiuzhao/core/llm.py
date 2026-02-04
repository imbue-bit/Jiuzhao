import os
from openai import OpenAI
from typing import List, Dict, Any
from jiuzhao.config import load_config, get_model_config, get_generation_config

class LLMClient:
    def __init__(self):
        self.config = load_config()
        self.model_name = self.config.get("current_model")
        self.model_config = get_model_config(self.model_name)
        self.gen_config = get_generation_config()
        
        if not self.model_config:
            raise ValueError(f"Model configuration for '{self.model_name}' not found. Please run 'jiuzhao config'.")

        # API Key resolution: Config > Env Var > Default/Ollama
        api_key = self.model_config.get("api_key")
        if not api_key:
            api_key = os.getenv("OPENAI_API_KEY", "ollama")

        self.client = OpenAI(
            base_url=self.model_config.get("base_url"),
            api_key=api_key,
            timeout=self.gen_config.get("timeout", 60)
        )

    def chat(self, messages: List[Dict[str, str]]) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=self.gen_config.get("temperature", 0.2),
                max_tokens=self.gen_config.get("max_tokens", 4096)
            )
            content = response.choices[0].message.content
            if not content:
                return "Error: Empty response from LLM."
            return content
        except Exception as e:
            return f"LLM Connection Error: {str(e)}"
