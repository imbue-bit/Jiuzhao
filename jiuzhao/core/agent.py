import re
import json
from jiuzhao.core.llm import LLMClient
from jiuzhao.tools.registry import ToolRegistry
from jiuzhao.config import get_generation_config
from jiuzhao.utils.ui import console, print_agent_msg, print_tool_use, print_tool_output, print_success, print_error

class Agent:
    def __init__(self):
        self.llm = LLMClient()
        self.tools = ToolRegistry()
        self.history = []
        self.gen_config = get_generation_config()
        self._init_system_prompt()

    def _init_system_prompt(self):
        tool_docs = self.tools.get_tool_definitions()
        system_prompt = f"""
You are Jiuzhao, an expert Automated Formalization Agent for Lean 4.

GOAL:
Formalize mathematical statements and prove them rigorously using Lean 4.

AVAILABLE TOOLS:
{tool_docs}

INSTRUCTIONS:
1. **Explore**: If you don't know the project structure, use `file_system` (list) or `project_search`.
2. **Plan**: Break down the proof into lemmas if necessary.
3. **Act**: Write code using `file_system` (write).
4. **Verify**: ALWAYS verify your code using `lean_tool` (check_file).
5. **Refine**: If compilation fails, read the error, adjust the code, and retry.
6. **Finish**: When `lean_tool` returns SUCCESS, inform the user.

TOOL USAGE FORMAT:
To use a tool, output XML strictly like this:
<TOOL name="tool_name">
{{ "json_key": "json_value" }}
</TOOL>

Do not use markdown code blocks (```xml) for tool calls.
"""
        self.history.append({"role": "system", "content": system_prompt})

    def _parse_tool_call(self, text: str):
        # Improved regex to handle potential newlines inside the tag
        pattern = r'<TOOL name="(.*?)">\s*({.*?})\s*</TOOL>'
        match = re.search(pattern, text, re.DOTALL)
        if match:
            return match.group(1), match.group(2)
        return None, None

    def run(self, user_input: str):
        self.history.append({"role": "user", "content": user_input})
        
        max_turns = self.gen_config.get("max_turns", 15)
        turn = 0
        
        while turn < max_turns:
            turn += 1
            
            with console.status(f"[bold green]Jiuzhao is thinking ({turn}/{max_turns})..."):
                response = self.llm.chat(self.history)
            
            self.history.append({"role": "assistant", "content": response})
            print_agent_msg(response)

            tool_name, tool_args_str = self._parse_tool_call(response)
            
            if tool_name:
                try:
                    # Clean up potential markdown formatting inside JSON if model hallucinates it
                    clean_json = tool_args_str.strip()
                    if clean_json.startswith("```json"): clean_json = clean_json[7:]
                    if clean_json.endswith("```"): clean_json = clean_json[:-3]
                    
                    tool_args = json.loads(clean_json)
                    print_tool_use(tool_name, str(tool_args))
                    
                    with console.status(f"[bold cyan]Executing {tool_name}..."):
                        tool_result = self.tools.execute(tool_name, tool_args)
                    
                    print_tool_output(tool_result)
                    
                    self.history.append({
                        "role": "user", 
                        "content": f"Tool '{tool_name}' output:\n{tool_result}"
                    })

                    if "SUCCESS" in tool_result:
                        print_success("Action verified successfully by tool!")
                    
                except json.JSONDecodeError:
                    error_msg = "Error: Invalid JSON in tool arguments."
                    print_error(error_msg)
                    self.history.append({"role": "user", "content": error_msg})
                except Exception as e:
                    error_msg = f"Error processing tool call: {str(e)}"
                    print_error(error_msg)
                    self.history.append({"role": "user", "content": error_msg})
            else:
                # No tool called. Check if the agent thinks it's done.
                # Heuristic: If it says "QED" or "proven" or "done" and no tool was called.
                if "QED" in response or ("proven" in response.lower() and "success" in response.lower()):
                    print_success("Jiuzhao has finished the task.")
                    break
                
                # If it's just a conversational response, we might want to stop or ask user
                # For now, we break to let the user reply in the main loop
                break
