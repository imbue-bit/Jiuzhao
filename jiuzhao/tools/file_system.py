import os
from typing import Dict, Any
from .base import BaseTool

class FileSystemTool(BaseTool):
    @property
    def name(self) -> str:
        return "file_system"

    @property
    def description(self) -> str:
        return "Read, write, or list files in the project directory."

    @property
    def usage(self) -> str:
        return """<TOOL name="file_system">
{
  "action": "read" | "write" | "list",
  "path": "path/to/file_or_dir",
  "content": "content to write (only for write action)"
}
</TOOL>"""

    def execute(self, args: Dict[str, Any]) -> str:
        action = args.get("action")
        path = args.get("path", ".")
        
        # Basic security check
        if ".." in path or path.startswith("/"):
            return "Error: Access denied. Please use relative paths within the project."

        if action == "write":
            content = args.get("content", "")
            try:
                # Ensure directory exists
                os.makedirs(os.path.dirname(path) if os.path.dirname(path) else ".", exist_ok=True)
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
        
        elif action == "list":
            try:
                if not os.path.exists(path):
                    return f"Error: Directory {path} does not exist."
                
                files = []
                for item in os.listdir(path):
                    if item.startswith("."): continue # skip hidden files
                    full_path = os.path.join(path, item)
                    kind = "DIR" if os.path.isdir(full_path) else "FILE"
                    files.append(f"[{kind}] {item}")
                return "\n".join(files) if files else "(Empty Directory)"
            except Exception as e:
                return f"List failed: {str(e)}"
        
        return "Error: Invalid action. Use 'read', 'write', or 'list'."
