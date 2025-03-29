def main():
    from ghcopilot.api import GithubCopilotClient, CopilotAuthError, CopilotAPIError
    import logging
    import inquirer
    import sys
    import time
    from rich.console import Console
    from rich.markdown import Markdown
    from rich.panel import Panel
    from rich.live import Live
    from rich.layout import Layout
    from rich.spinner import Spinner
    from rich.table import Table
    from rich.box import ROUNDED

    # Configure logging for the CLI
    logging.basicConfig(level=logging.INFO, format='%(message)s')

    # Initialize rich console for better markdown rendering
    console = Console()

    client = GithubCopilotClient()

    # Try to load token from file first
    if not client.load_token_from_file():
        # If no token found, authenticate through browser
        console.print(Panel("[bold yellow]No authentication token found[/bold yellow]", 
                            title="Authentication Required", border_style="yellow"))
        cookies = client.get_cookies()
        client.authenticate(cookies)
        # Save token for future use
        client.save_token_to_file()
        console.print(Panel("[bold green]Authentication successful![/bold green]", border_style="green"))

    try:
        # Display a spinner while loading
        with console.status("[bold blue]Loading Copilot...[/bold blue]", spinner="dots"):
            thread_id = client.get_latest_thread()
            models = client.get_models()
        
        if not models:
            console.print(Panel("[bold red]No models available[/bold red]", 
                                title="Error", border_style="red"))
            sys.exit(1)
        
        # Build model selection options text
        model_options = "[bold white]Available Models:[/bold white]\n\n"
        for idx, model in enumerate(models, 1):
            model_options += f"  [cyan]{idx}[/cyan]. {model['name']}\n"
        
        model_options += "\n[yellow]Enter the number of your selected model:[/yellow]"
        
        # Display model selection panel
        console.print(Panel(model_options, title="Model Selection", border_style="cyan", width=80))
        
        # Get model selection via direct input
        valid_selection = False
        selected_model = None
        
        while not valid_selection:
            try:
                choice = console.input("[bold cyan]Select model > [/bold cyan]")
                model_idx = int(choice) - 1
                
                if 0 <= model_idx < len(models):
                    selected_model = models[model_idx]
                    valid_selection = True
                else:
                    console.print("[bold red]Invalid selection. Please try again.[/bold red]")
            except ValueError:
                console.print("[bold red]Please enter a valid number.[/bold red]")
        
        selected_model_name = selected_model["name"]
        console.print(f"[green]Selected model: [bold]{selected_model_name}[/bold][/green]")
        
        # Welcome panel with improved styling and information
        welcome = Panel(
            f"[bold white]Welcome to GitHub Copilot Chat[/bold white]\n\n"
            f"[cyan]Model:[/cyan] {selected_model_name}\n\n"
            f"[yellow]Commands:[/yellow]\n"
            f"  • [bold]exit[/bold] - Quit the application\n"
            f"  • [bold]new thread[/bold] - Start a fresh conversation\n"
            f"  • [bold]clear[/bold] - Clear the screen\n"
            f"  • [bold]help[/bold] - Show available commands",
            title="[bold]GitHub Copilot CLI[/bold]",
            border_style="green",
            width=80
        )
        console.print(welcome)
        
        # Begin conversation loop
        conversation_active = True
        while conversation_active:
            prompt = console.input("\n[bold cyan]You > [/bold cyan]")
            
            # Handle special commands
            if prompt.lower() == 'exit':
                console.print("[yellow]Exiting chat...[/yellow]")
                # Ensure exit is called immediately without any further processing
                return sys.exit(0)  # Changed from sys.exit(0) to return sys.exit(0)
            elif prompt.lower() == 'new thread':
                thread_id = client.create_new_thread()
                console.print("[yellow]Created new conversation thread[/yellow]")
                continue
            elif prompt.lower() == 'clear':
                console.clear()
                console.print(welcome)
                continue
            elif prompt.lower() == 'help':
                console.print(Panel(
                    "[yellow]Available Commands:[/yellow]\n"
                    "  • [bold]exit[/bold] - Quit the application\n"
                    "  • [bold]new thread[/bold] - Start a fresh conversation\n"
                    "  • [bold]clear[/bold] - Clear the screen\n"
                    "  • [bold]help[/bold] - Show this help message",
                    title="Help", border_style="blue"
                ))
                continue
            elif not prompt.strip():
                continue
            
            # Process normal chat message
            console.print("[bold green]Copilot > [/bold green]")
            
            response_text = ""
            # Create a live display for updating markdown in real-time
            with Live(Markdown(""), auto_refresh=True, refresh_per_second=10) as live:
                for message in client.send_message(prompt, selected_model["id"], thread_id):
                    if message["type"] == "content":
                        content = message["text"]
                        response_text += content
                        # Update the live display with current markdown
                        live.update(Markdown(response_text))
                    elif message["type"] == "complete":
                        # Final render with references if available
                        if message.get("references"):
                            references = "\n\n### References\n"
                            for ref in message["references"]:
                                url = ref.get('url', '')
                                references += f"- {url}\n"
                            response_text += references
                            live.update(Markdown(response_text))
            
            # Add a separator between conversations
            console.print("─" * 80, style="dim")
                    
    except (CopilotAuthError, CopilotAPIError) as e:
        console.print(Panel(f"[bold red]Error: {e}[/bold red]", title="API Error", border_style="red"))
        return sys.exit(1)  # Changed from sys.exit(1) to return sys.exit(1)
    except KeyboardInterrupt:
        console.print("\n[yellow]Chat session terminated.[/yellow]")
    except ImportError:
        console.print(Panel(
            "Required libraries not installed. Run:\n[bold]pip install rich[/bold]",
            title="Missing Dependencies", 
            border_style="red"
        ))
        # Fallback to simple text display if rich is not available
        print(f"\n\n{response_text}")

if __name__ == "__main__":
    main()