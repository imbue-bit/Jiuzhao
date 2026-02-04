import os
import subprocess
from typing import Dict, Any
from .base import BaseTool

class LeanTool(BaseTool):
    @property
    def name(self) -> str:
        return "lean_tool"

    @property
    def description(self) -> str:
        return "Compile Lean 4 files or run Lake build commands."

    @property
    def usage(self) -> str:
        return """<TOOL name="lean_tool">
{
  "command": "check_file" | "lake_build",
  "path": "filename.lean" (required for check_file)
}
</TOOL>"""

    def execute(self, args: Dict[str, Any]) -> str:
        command = args.get("command")
        
        if command == "check_file":
            path = args.get("path")
            if not path:
                return "Error: 'path' is required for check_file."
            if not os.path.exists(path):
                return f"Error: File {path} not found."
            
            # Using 'lean' directly to check a single file
            cmd = ["lean", path]
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                if result.returncode == 0:
                    return "SUCCESS: Proof Verified (No output from compiler)."
                else:
                    output = (result.stderr + "\n" + result.stdout).strip()
                    return f"COMPILER ERROR:\n{output}"
            except subprocess.TimeoutExpired:
                return "Error: Compilation timed out (30s)."
            except FileNotFoundError:
                return "Error: 'lean' executable not found."

        elif command == "lake_build":
            # Run 'lake build' for the whole project
            try:
                result = subprocess.run(["lake", "build"], capture_output=True, text=True, timeout=120)
                if result.returncode == 0:
                    return "SUCCESS: Project built successfully."
                else:
                    output = (result.stderr + "\n" + result.stdout).strip()
                    return f"BUILD ERROR:\n{output}"
            except subprocess.TimeoutExpired:
                return "Error: Build timed out (120s)."
            except FileNotFoundError:
                return "Error: 'lake' executable not found."
        
        return "Error: Invalid command. Use 'check_file' or 'lake_build'."
