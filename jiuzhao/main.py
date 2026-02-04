import typer
import json
from rich.prompt import Prompt, Confirm
from jiuzhao.core.agent import Agent
from jiuzhao.config import load_config, save_config, load_default_models
from jiuzhao.utils.ui import print_header, console, print_error

app = typer.Typer(help="Jiuzhao: Automated Formalization Agent")

@app.command()
def prove(statement: str = typer.Argument(..., help="The mathematical statement to prove")):
    print_header()
    
    try:
        agent = Agent()
        agent.run(statement)
        
        while True:
            user_input = Prompt.ask("[bold yellow]You[/bold yellow]")
            if user_input.lower() in ["exit", "quit"]:
                break
            agent.run(user_input)
            
    except Exception as e:
        print_error(f"Failed to initialize agent: {str(e)}")
        console.print("[dim]Tip: Run 'jiuzhao config' to set up your model.[/dim]")

@app.command()
def config():
    print_header()
    config_data = load_config()
    
    default_models = load_default_models()
    if not config_data.get("models"):
        config_data["models"] = default_models
    
    current = config_data.get("current_model", "None")
    console.print(f"Current Model: [bold green]{current}[/bold green]\n")
    
    console.print("[bold]Available Models:[/bold]")
    models = config_data["models"]
    for idx, m in enumerate(models):
        console.print(f"{idx + 1}. {m['name']} ({m['provider']})")
    
    choice = Prompt.ask("Select model number", choices=[str(i+1) for i in range(len(models))], default="1")
    selected_model = models[int(choice)-1]
    
    if selected_model["provider"] == "openai" and not selected_model.get("api_key"):
        key = Prompt.ask(f"Enter API Key for {selected_model['name']}", password=True)
        selected_model["api_key"] = key
        config_data["models"][int(choice)-1] = selected_model
    
    config_data["current_model"] = selected_model["name"]
    save_config(config_data)
    
    console.print(f"\n[bold green]Configuration saved![/bold green] Using {selected_model['name']}.")

if __name__ == "__main__":
    app()
