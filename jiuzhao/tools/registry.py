from typing import Dict, Any
from .base import BaseTool
from .file_system import FileSystemTool
from .lean import LeanTool
from .search import SearchTool

class ToolRegistry:
    def __init__(self):
        self.tools: Dict[str, BaseTool] = {}
        self._register_defaults()

    def _register_defaults(self):
        self.register(FileSystemTool())
        self.register(LeanTool())
        self.register(SearchTool())

    def register(self, tool: BaseTool):
        self.tools[tool.name] = tool

    def get_tool_definitions(self) -> str:
        defs = [t.get_definition() for t in self.tools.values()]
        return "\n---\n".join(defs)

    def execute(self, tool_name: str, args: Dict[str, Any]) -> str:
        if tool_name not in self.tools:
            return f"Error: Tool '{tool_name}' not found."
        try:
            return self.tools[tool_name].execute(args)
        except Exception as e:
            return f"Error executing {tool_name}: {str(e)}"
