import re
import json
from jiuzhao.core.llm import LLMClient
from jiuzhao.tools.impl import ToolRegistry
from jiuzhao.utils.ui import console, print_agent_msg, print_tool_use, print_tool_output, print_success, print_error

class Agent:
    def __init__(self):
        self.llm = LLMClient()
        self.tools = ToolRegistry()
        self.history = []
        self._init_system_prompt()

    def _init_system_prompt(self):
        tool_docs = self.tools.get_tool_definitions()
        system_prompt = f"""
You are Jiuzhao, an expert Automated Formalization Agent for Lean 4.
Your goal is to formalize mathematical statements and prove them rigorously.

AVAILABLE TOOLS:
{tool_docs}

WORKFLOW:
1.  **Analyze**: Understand the user's request. If ambiguous, ask for clarification.
2.  **Act**: Use tools to write code or verify proofs.
    To use a tool, output XML strictly like this:
    <TOOL name="tool_name">
    {{ "json_arg": "value" }}
    </TOOL>
3.  **Refine**: If the compiler returns an error, analyze it and fix the code.
4.  **Finish**: When the proof is verified (SUCCESS), inform the user.

Do not output markdown code blocks for tool calls. Just raw XML tags.
"""
        self.history.append({"role": "system", "content": system_prompt})

    def _parse_tool_call(self, text: str):
        pattern = r'<TOOL name="(.*?)">\s*({.*?})\s*</TOOL>'
        match = re.search(pattern, text, re.DOTALL)
        if match:
            return match.group(1), match.group(2)
        return None, None

    def run(self, user_input: str):
        self.history.append({"role": "user", "content": user_input})
        
        max_turns = 10
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
                    tool_args = json.loads(tool_args_str)
                    print_tool_use(tool_name, str(tool_args))
                    
                    with console.status(f"[bold cyan]Executing {tool_name}..."):
                        tool_result = self.tools.execute(tool_name, tool_args)
                    
                    print_tool_output(tool_result)
                    
                    self.history.append({
                        "role": "user", 
                        "content": f"Tool '{tool_name}' output:\n{tool_result}"
                    })

                    if "SUCCESS: Proof Verified" in tool_result:
                        print_success("Proof verified by Lean compiler!")
                    
                except json.JSONDecodeError:
                    error_msg = "Error: Invalid JSON in tool arguments."
                    print_error(error_msg)
                    self.history.append({"role": "user", "content": error_msg})
            else:
                if "verified" in response.lower() and "success" in response.lower():
                    break
                
                break
