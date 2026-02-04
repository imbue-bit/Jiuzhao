import typer
from rich.prompt import Prompt, IntPrompt, FloatPrompt
from jiuzhao.core.agent import Agent
from jiuzhao.config import load_config, save_config, load_default_models
from jiuzhao.utils.ui import print_header, console, print_error

app = typer.Typer(help="Jiuzhao: Automated Formalization Agent for Lean 4")

@app.command()
def prove(statement: str = typer.Argument(..., help="The mathematical statement or request")):
    """
    Start an interactive proving session.
    """
    print_header()
    
    try:
        agent = Agent()
        agent.run(statement)
        
        while True:
            console.print("\n[bold yellow]User Input[/bold yellow] (type 'exit' to quit):")
            user_input = Prompt.ask(">")
            
            if user_input.lower() in ["exit", "quit"]:
                console.print("[dim]Goodbye![/dim]")
                break
            
            if not user_input.strip():
                continue
                
            agent.run(user_input)
            
    except Exception as e:
        print_error(f"Failed to initialize agent: {str(e)}")
        console.print("[dim]Tip: Run 'jiuzhao config' to check your settings.[/dim]")

@app.command()
def config():
    """
    Configure models and generation parameters.
    """
    print_header()
    config_data = load_config()
    
    # --- Model Selection ---
    current = config_data.get("current_model", "None")
    console.print(f"Current Model: [bold green]{current}[/bold green]\n")
    
    console.print("[bold]Available Models:[/bold]")
    models = config_data["models"]
    for idx, m in enumerate(models):
        console.print(f"{idx + 1}. {m['name']} ({m['provider']})")
    
    choice = Prompt.ask(
        "Select model number (or press Enter to keep current)", 
        choices=[str(i+1) for i in range(len(models))] + [""], 
        default=""
    )
    
    if choice:
        selected_model = models[int(choice)-1]
        
        # Handle API Key
        if selected_model["provider"] == "openai" and not selected_model.get("api_key"):
            key = Prompt.ask(f"Enter API Key for {selected_model['name']}", password=True)
            if key:
                selected_model["api_key"] = key
                config_data["models"][int(choice)-1] = selected_model
        
        config_data["current_model"] = selected_model["name"]
        console.print(f"[info]Model updated to {selected_model['name']}[/info]")

    # --- Generation Parameters ---
    console.print("\n[bold]Generation Settings:[/bold]")
    gen_config = config_data.get("generation", {})
    
    if Prompt.ask("Edit generation parameters?", choices=["y", "n"], default="n") == "y":
        gen_config["temperature"] = FloatPrompt.ask(
            "Temperature", default=gen_config.get("temperature", 0.2)
        )
        gen_config["max_tokens"] = IntPrompt.ask(
            "Max Tokens", default=gen_config.get("max_tokens", 4096)
        )
        gen_config["max_turns"] = IntPrompt.ask(
            "Max Auto-Turns per Request", default=gen_config.get("max_turns", 15)
        )
        gen_config["timeout"] = IntPrompt.ask(
            "Timeout (seconds)", default=gen_config.get("timeout", 60)
        )
        config_data["generation"] = gen_config

    save_config(config_data)
    console.print("\n[bold green]Configuration saved successfully![/bold green]")

if __name__ == "__main__":
    app()
