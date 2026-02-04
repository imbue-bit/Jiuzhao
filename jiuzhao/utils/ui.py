from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.theme import Theme
from rich.align import Align

custom_theme = Theme({
    "info": "dim cyan",
    "warning": "magenta",
    "danger": "bold red",
    "success": "bold green"
})

console = Console(theme=custom_theme)

BANNER = r"""
      ██╗██╗██╗   ██╗███████╗██╗  ██╗ █████╗  ██████╗ 
      ██║██║██║   ██║╚══███╔╝██║  ██║██╔══██╗██╔═══██╗
      ██║██║██║   ██║  ███╔╝ ███████║███████║██║   ██║
 ██   ██║██║██║   ██║ ███╔╝  ██╔══██║██╔══██║██║   ██║
 ╚█████╔╝██║╚██████╔╝███████╗██║  ██║██║  ██║╚██████╔╝
  ╚════╝ ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ 
"""

def print_header():
    console.print(Align.center(f"[bold blue]{BANNER}[/bold blue]"))
    console.print(Align.center(
        "[dim]Automated Formalization Agent for Lean 4[/dim]\n"
        "[dim]v0.2.0[/dim]"
    ))
    console.print()

def print_agent_msg(content: str):
    console.print(Panel(
        Markdown(content),
        title="🤖 Agent",
        border_style="green",
        title_align="left"
    ))

def print_tool_use(tool_name: str, args: str):
    console.print(f"[dim]🔨 Tool Call: [bold]{tool_name}[/bold][/dim]")
    # Truncate args if they are too long (e.g. file content)
    if len(args) > 200:
        args = args[:200] + "..."
    console.print(f"[dim]   Args: {args}[/dim]")

def print_tool_output(output: str):
    # Truncate very long outputs for display
    display_output = output
    if len(output) > 1000:
        display_output = output[:1000] + "\n... [Output Truncated]"
        
    style = "dim"
    if "ERROR" in output:
        style = "danger"
    elif "SUCCESS" in output:
        style = "success"
        
    console.print(f"[{style}]   Result: {display_output}[/{style}]")

def print_error(msg: str):
    console.print(f"[danger]❌ Error:[/danger] {msg}")

def print_success(msg: str):
    console.print(f"[success]✅ Success:[/success] {msg}")
