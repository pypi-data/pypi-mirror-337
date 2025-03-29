import json
import os
import time
import uuid
import logging
from pathlib import Path
from typing import Dict, List, Generator, Any, Optional, Union

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configure logging
logger = logging.getLogger(__name__)

class CopilotAuthError(Exception):
    """Exception raised for authentication errors."""
    pass

class CopilotAPIError(Exception):
    """Exception raised for API errors."""
    pass

class GithubCopilotClient:
    """Client for interacting with GitHub Copilot API."""
    
    BASE_URL = "https://api.individual.githubcopilot.com"
    
    def __init__(self, auth_token: Optional[str] = None, debug: bool = False):
        """Initialize the GitHub Copilot client.
        
        Args:
            auth_token: Optional authentication token to reuse
            debug: Whether to enable debug logging
        """
        self.session = requests.Session()
        self.auth_token = auth_token
        
        # Configure logging
        log_level = logging.DEBUG if debug else logging.INFO
        logging.basicConfig(level=log_level, format='%(levelname)s: %(message)s')
        
        self.headers = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'sec-gpc': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
        }
    
    def load_token_from_file(self, filepath: Union[str, Path] = "copilot_token.txt", timeout_period: int = 30) -> bool:
        """Load authentication token from file.
        
        Args:
            filepath: Path to the token file
            timeout_period: Maximum age in minutes of the token
            
        Returns:
            True if token was loaded successfully and is within timeout period, False otherwise
        """
        try:
            with open(filepath, 'r') as f:
                lines = f.readlines()
                if len(lines) < 2:
                    logger.debug(f"Invalid token file format: {filepath}")
                    return False
                    
                token = lines[0].strip()
                try:
                    creation_time = int(lines[1].strip())
                    current_time = int(time.time())
                    # Check if token is still valid (within timeout period)
                    if current_time - creation_time > timeout_period * 60:
                        logger.debug(f"Token expired ({timeout_period} minutes timeout)")
                        return False
                        
                    self.auth_token = token
                    logger.info("Token loaded successfully")
                    return True
                except ValueError:
                    logger.debug(f"Invalid timestamp in token file: {filepath}")
                    return False
        except FileNotFoundError:
            logger.debug(f"Token file not found: {filepath}")
            return False
    
    def save_token_to_file(self, filepath: Union[str, Path] = "copilot_token.txt") -> None:
        """Save authentication token to file.
        
        Args:
            filepath: Path where to save the token
        """
        if not self.auth_token:
            raise CopilotAuthError("No token available to save")
            
        with open(filepath, 'w') as f:
            f.write(f"{self.auth_token}\n{int(time.time())}")
        logger.info(f"Token saved to {filepath}")
        
    def get_inline_completion(self, prompt: str, language: str = 'python', 
                              max_tokens: int = 1000, temperature: float = 0) -> str:
        """Get inline code completion from GitHub Copilot.
        
        Args:
            prompt: The code prompt to complete
            language: Programming language of the code
            max_tokens: Maximum number of tokens to generate
            temperature: Sampling temperature (0-1)
            
        Returns:
            The completion text
            
        Raises:
            CopilotAuthError: If not authenticated
            CopilotAPIError: If the API request fails
        """
        if not self.auth_token:
            raise CopilotAuthError("Authentication token not set. Authenticate first.")
            
        completion_text = ""
        
        try:
            response = self.session.post(
                'https://copilot-proxy.githubusercontent.com/v1/engines/copilot-codex/completions',
                headers={'authorization': f'Bearer {self.auth_token}'},
                json={
                    'prompt': prompt,
                    'suffix': '',
                    'max_tokens': max_tokens,
                    'temperature': temperature,
                    'top_p': 1,
                    'n': 1,
                    'stop': ['\n'],
                    'nwo': 'github/copilot.vim',
                    'stream': True,
                    'extra': {'language': language}
                },
                stream=True
            )
            response.raise_for_status()
            
            for line in response.iter_lines():
                if not line:
                    continue
                    
                line_text = line.decode('utf-8')
                if line_text.startswith('data: {'):
                    try:
                        completion_data = json.loads(line_text[6:])
                        choice_text = completion_data.get('choices', [{}])[0].get('text', '')
                        completion_text += choice_text or '\n'
                    except json.JSONDecodeError:
                        continue
                        
        except requests.exceptions.RequestException as error:
            logger.error(f"Error getting inline completion: {error}")
            raise CopilotAPIError(f"Failed to get completion: {error}")
            
        return completion_text
    
    def get_cookies(self, headless: bool = False, timeout: int = 300) -> Dict[str, str]:
        """Get GitHub cookies by automating browser login.
        
        Args:
            headless: Whether to run browser in headless mode
            timeout: Seconds to wait for login
            
        Returns:
            Dictionary of cookies
            
        Raises:
            CopilotAuthError: If login fails
        """
        from selenium.webdriver.chrome.options import Options
        
        logger.info("Opening browser for GitHub login...")
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
        
        driver = webdriver.Chrome(options=chrome_options)
        driver.get('https://github.com/login')
        
        logger.info("Please sign in to GitHub in the opened browser window.")
        logger.info(f"Waiting for login (timeout: {timeout}s)...")
        
        try:
            WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".logged-in, .dashboard"))
            )
            logger.info("Login successful!")
            
            cookies = {cookie['name']: cookie['value'] for cookie in driver.get_cookies()}
            return cookies
        except Exception as e:
            logger.error(f"Error capturing cookies: {e}")
            raise CopilotAuthError(f"Failed to get GitHub cookies: {e}")
        finally:
            driver.quit()

    def authenticate(self, cookies: Optional[Dict[str, str]] = None) -> str:
        """Authenticate with GitHub Copilot.
        
        Args:
            cookies: Optional cookies dictionary. If not provided, will open browser for login.
            
        Returns:
            Authentication token
            
        Raises:
            CopilotAuthError: If authentication fails
        """
        if not cookies:
            cookies = self.get_cookies()
            
        headers = {**self.headers}
        headers.update({
            'content-type': 'application/json',
            'github-verified-fetch': 'true',
            'origin': 'https://github.com',
            'referer': 'https://github.com/copilot',
            'x-requested-with': 'XMLHttpRequest',
        })
    
        try:
            response = self.session.post(
                'https://github.com/github-copilot/chat/token', 
                cookies=cookies, 
                headers=headers
            )
            response.raise_for_status()
            token = response.json().get("token")
            
            if not token:
                raise CopilotAuthError("No token received from GitHub")
                
            self.auth_token = token
            logger.info("Authentication successful")
            return token
            
        except Exception as e:  # Catch all exceptions
            logger.error(f"Authentication failed: {e}")
            # Ensure we're catching the exception and properly converting it
            raise CopilotAuthError(f"Failed to get auth token: {e}") from e

    def _get_auth_headers(self) -> Dict[str, str]:
        """Get headers with authentication token.
        
        Returns:
            Headers dictionary with auth token
            
        Raises:
            CopilotAuthError: If not authenticated
        """
        if not self.auth_token:
            raise CopilotAuthError("Authentication token not set. Call authenticate first.")
            
        headers = {**self.headers}
        headers.update({
            'authorization': f'GitHub-Bearer {self.auth_token}',
            'copilot-integration-id': 'copilot-chat',
            'origin': 'https://github.com',
            'referer': 'https://github.com/',
        })
        return headers

    def get_latest_thread(self) -> str:
        """Get the ID of the latest chat thread.
        
        Returns:
            Thread ID
            
        Raises:
            CopilotAuthError: If not authenticated
            CopilotAPIError: If API request fails
        """
        try:
            response = self.session.get(
                f'{self.BASE_URL}/github/chat/threads', 
                headers=self._get_auth_headers()
            )
            response.raise_for_status()
            threads = response.json().get("threads", [])
            
            if not threads:
                logger.warning("No threads found")
                return self.create_new_thread()
                
            return threads[0]["id"]
        except CopilotAuthError:
            raise
        except Exception as e:
            logger.error(f"Error fetching threads: {e}")
            raise CopilotAPIError(f"Failed to get threads: {e}")
    
    def create_new_thread(self) -> str:
        """Create a new chat thread.
        
        Returns:
            New thread ID
            
        Raises:
            CopilotAuthError: If not authenticated
            CopilotAPIError: If API request fails
        """
        try:
            response = self.session.post(
                f'{self.BASE_URL}/github/chat/threads',
                headers=self._get_auth_headers(),
                json={}
            )
            response.raise_for_status()
            thread_id = response.json().get("id")
            logger.info(f"Created new thread: {thread_id}")
            return thread_id
        except CopilotAuthError:
            raise
        except Exception as e:
            logger.error(f"Error creating thread: {e}")
            raise CopilotAPIError(f"Failed to create thread: {e}")

    def delete_thread(self, thread_id: str) -> bool:
        """Delete a chat thread.
        
        Args:
            thread_id: The ID of the thread to delete
            
        Returns:
            True if thread was deleted successfully
            
        Raises:
            CopilotAuthError: If not authenticated
            CopilotAPIError: If API request fails
        """
        try:
            response = self.session.delete(
                f'{self.BASE_URL}/github/chat/threads/{thread_id}',
                headers=self._get_auth_headers()
            )
            
            if response.status_code == 204:
                logger.info(f"Thread {thread_id} deleted successfully")
                return True
            else:
                logger.error(f"Failed to delete thread {thread_id}: Status {response.status_code}")
                raise CopilotAPIError(f"Failed to delete thread: HTTP {response.status_code}")
                
        except CopilotAuthError:
            raise
        except Exception as e:
            logger.error(f"Error deleting thread {thread_id}: {e}")
            raise CopilotAPIError(f"Failed to delete thread: {e}")

    def get_models(self) -> List[Dict[str, str]]:
        """Get available models.
        
        Returns:
            List of available models with their IDs and names
            
        Raises:
            CopilotAuthError: If not authenticated
            CopilotAPIError: If API request fails
        """
        try:
            response = self.session.get(
                f'{self.BASE_URL}/models', 
                headers=self._get_auth_headers()
            )
            response.raise_for_status()
            data = response.json()
            
            models = [
                {"id": model.get("id", ""), "name": model.get("name", "")}
                for model in data.get("data", [])
            ]
            
            logger.debug(f"Available models: {models}")
            return models
        except CopilotAuthError:
            raise
        except Exception as e:
            logger.error(f"Error fetching models: {e}")
            raise CopilotAPIError(f"Failed to get models: {e}")
    
    def send_message(self, message: str, model_id: str, thread_id: Optional[str] = None,
                     streaming: bool = True) -> Generator[Dict[str, Any], None, None]:
        """Send a message to Copilot and stream the response.
        
        Args:
            message: The message content
            model_id: ID of the model to use
            thread_id: Optional thread ID. If not provided, uses latest thread.
            streaming: Whether to stream the response
            
        Yields:
            Dictionaries containing content or completion information
            
        Raises:
            CopilotAuthError: If not authenticated
            CopilotAPIError: If API request fails
        """
        if not thread_id:
            thread_id = self.get_latest_thread()
            
        headers = self._get_auth_headers()
        headers['content-type'] = 'text/event-stream'
        
        data = {
            "responseMessageID": str(uuid.uuid4()),
            "content": message,
            "intent": "conversation",
            "references": [],
            "context": [],
            "currentURL": "https://github.com/copilot",
            "streaming": streaming,
            "confirmations": [],
            "customInstructions": [],
            "model": model_id,
            "mode": "immersive",
            "parentMessageID": "root",
            "tools": [],
            "mediaContent": [],
            "skillOptions": {"deepCodeSearch": False}
        }

        try:
            response = self.session.post(
                f'{self.BASE_URL}/github/chat/threads/{thread_id}/messages',
                headers=headers,
                data=json.dumps(data),
                stream=True
            )
            response.raise_for_status()
            
            for line in response.iter_lines():
                if not line:
                    continue
                    
                line_text = line.decode('utf-8')
                if line_text.startswith('data: '):
                    try:
                        data = json.loads(line_text[6:])  # Remove 'data: ' prefix
                        
                        if data.get('type') == 'content':
                            yield {
                                'type': 'content',
                                'text': data.get('body', '')
                            }
                        elif data.get('type') == 'complete':
                            annotations = data.get('copilotAnnotations', {})
                            yield {
                                'type': 'complete',
                                'vulnerabilities': annotations.get('CodeVulnerability', []),
                                'references': annotations.get('PublicCodeReference', [])
                            }
                    except json.JSONDecodeError:
                        continue
        except CopilotAuthError:
            raise
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            raise CopilotAPIError(f"Failed to send message: {e}")

def run_cli_example():
    """Run an interactive CLI conversation with GitHub Copilot."""
    import inquirer
    from sys import exit
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
            exit(1)
        
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
                conversation_active = False
                console.print("[yellow]Exiting chat...[/yellow]")
                break
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
        exit(1)
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

# Only run the example if this file is executed directly
if __name__ == "__main__":
    run_cli_example()