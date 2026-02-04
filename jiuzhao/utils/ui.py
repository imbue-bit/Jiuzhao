from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.theme import Theme

custom_theme = Theme({
    "info": "dim cyan",
    "warning": "magenta",
    "danger": "bold red"
})

console = Console(theme=custom_theme)

def print_header():
    console.print(Panel.fit(
        "[bold blue]Jiuzhao[/bold blue]: Automated Formalization Agent\n"
        "[dim]Powered by LLMs & Lean 4[/dim]",
        border_style="blue"
    ))

def print_agent_msg(content: str):
    console.print(Panel(
        Markdown(content),
        title="🤖 Agent",
        border_style="green",
        title_align="left"
    ))

def print_tool_use(tool_name: str, args: str):
    console.print(f"[dim]🔨 Tool Call: [bold]{tool_name}[/bold]({args})[/dim]")

def print_tool_output(output: str):
    display_output = output[:500] + "..." if len(output) > 500 else output
    console.print(f"[dim]   Result: {display_output}[/dim]")

def print_error(msg: str):
    console.print(f"[danger]❌ Error:[/danger] {msg}")

def print_success(msg: str):
    console.print(f"[bold green]✅ Success:[/bold green] {msg}")
