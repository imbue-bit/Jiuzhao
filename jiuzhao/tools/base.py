from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseTool(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        pass

    @property
    @abstractmethod
    def usage(self) -> str:
        pass

    @abstractmethod
    def execute(self, args: Dict[str, Any]) -> str:
        pass

    def get_definition(self) -> str:
        return f"""Name: {self.name}
Description: {self.description}
Usage:
{self.usage}"""
