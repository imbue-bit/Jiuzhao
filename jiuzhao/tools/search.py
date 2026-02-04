import os
from typing import Dict, Any
from .base import BaseTool

class SearchTool(BaseTool):
    @property
    def name(self) -> str:
        return "project_search"

    @property
    def description(self) -> str:
        return "Search for a string or keyword in all .lean files in the project."

    @property
    def usage(self) -> str:
        return """<TOOL name="project_search">
{
  "query": "theorem_name_or_keyword"
}
</TOOL>"""

    def execute(self, args: Dict[str, Any]) -> str:
        query = args.get("query")
        if not query:
            return "Error: 'query' argument is required."
        
        results = []
        try:
            # Simple recursive search
            for root, dirs, files in os.walk("."):
                # Skip common ignore dirs
                if ".git" in dirs: dirs.remove(".git")
                if ".lake" in dirs: dirs.remove(".lake")
                if "lake-packages" in dirs: dirs.remove("lake-packages")
                
                for file in files:
                    if file.endswith(".lean"):
                        path = os.path.join(root, file)
                        try:
                            with open(path, "r", encoding="utf-8") as f:
                                lines = f.readlines()
                                for i, line in enumerate(lines):
                                    if query in line:
                                        # Truncate line if too long
                                        content = line.strip()[:100]
                                        results.append(f"{path}:{i+1}: {content}")
                        except Exception:
                            continue # Skip unreadable files
            
            if not results:
                return f"No results found for '{query}'."
            
            # Limit results to prevent context overflow
            return "Search Results:\n" + "\n".join(results[:20])
        except Exception as e:
            return f"Search failed: {str(e)}"
