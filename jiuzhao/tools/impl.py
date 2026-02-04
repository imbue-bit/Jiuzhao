import os
import subprocess
import json
from typing import Dict, Any

class ToolRegistry:
    def __init__(self):
        self.tools = {}
        self.register_tools()

    def register_tools(self):
        self.tools["file_system"] = self.file_system_tool
        self.tools["lean_compiler"] = self.lean_compiler_tool

    def get_tool_definitions(self) -> str:
        """读取 markdown 文件夹下的工具描述"""
        tool_defs = []
        md_dir = os.path.join(os.path.dirname(__file__), "markdown")
        if os.path.exists(md_dir):
            for f in os.listdir(md_dir):
                if f.endswith(".md"):
                    with open(os.path.join(md_dir, f), "r") as file:
                        tool_defs.append(file.read())
        return "\n---\n".join(tool_defs)

    def execute(self, tool_name: str, args: Dict[str, Any]) -> str:
        if tool_name not in self.tools:
            return f"Error: Tool '{tool_name}' not found."
        try:
            return self.tools[tool_name](args)
        except Exception as e:
            return f"Error executing {tool_name}: {str(e)}"

    def file_system_tool(self, args: Dict[str, Any]) -> str:
        action = args.get("action")
        path = args.get("path")
        
        if not path:
            return "Error: 'path' is required."

        if action == "write":
            content = args.get("content", "")
            try:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)
                return f"Successfully wrote to {path}."
            except Exception as e:
                return f"Write failed: {str(e)}"
        
        elif action == "read":
            if not os.path.exists(path):
                return f"Error: File {path} does not exist."
            try:
                with open(path, "r", encoding="utf-8") as f:
                    return f.read()
            except Exception as e:
                return f"Read failed: {str(e)}"
        
        return "Error: Invalid action. Use 'read' or 'write'."

    def lean_compiler_tool(self, args: Dict[str, Any]) -> str:
        path = args.get("path")
        if not path:
            return "Error: 'path' is required."
        
        if not os.path.exists(path):
            return f"Error: File {path} not found."

        cmd = ["lean", path]
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                return "SUCCESS: Proof Verified."
            else:
                output = (result.stderr + "\n" + result.stdout).strip()
                return f"COMPILER ERROR:\n{output}"
                
        except subprocess.TimeoutExpired:
            return "Error: Compilation timed out."
        except FileNotFoundError:
            return "Error: 'lean' command not found. Please ensure Lean 4 is installed and in PATH."
