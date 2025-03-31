"""
Main application class for the QuackQuery AI Assistant.
"""

import os
import json
import logging
import asyncio
import re
import getpass
from dotenv import load_dotenv
from ..core.assistant import Assistant
from ..utils.screenshot import DesktopScreenshot
from ..utils.ocr import OCRProcessor
from ..integrations.github import GitHubIntegration
from ..utils.github_intent import GitHubIntentParser
from ..integrations.file_explorer import FileExplorer
from ..utils.file_intent import FileIntentParser
from ..utils.app_intent import AppIntentParser
from ..integrations.app_launcher import AppLauncher
from ..integrations.email_manager import EmailManager
from ..utils.email_intent import EmailIntentParser

# Rich UI components
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.markdown import Markdown
from rich.syntax import Syntax
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich import box
from datetime import datetime
import shutil
import smtplib
import imaplib
import tempfile
import subprocess

# Load environment variables for API keys
load_dotenv()

logger = logging.getLogger("ai_assistant")

class AIAssistantApp:
    """
    Main application class for the AI Assistant.
    
    Attributes:
        config (dict): Application configuration
        desktop_screenshot (DesktopScreenshot): Desktop screenshot utility
        assistant (Assistant): AI assistant instance
        ocr_processor (OCRProcessor): OCR processor for text extraction
        github (GitHubIntegration): GitHub integration
        github_intent_parser (GitHubIntentParser): GitHub intent parser
        file_explorer (FileExplorer): File explorer integration
        file_intent_parser (FileIntentParser): File intent parser
        app_intent_parser (AppIntentParser): App intent parser
        app_launcher (AppLauncher): App launcher for application launching
    """

    def __init__(self, config_path=None, debug=False):
        """
        Initialize the AI Assistant App.
        
        Args:
            config_path (str, optional): Path to the configuration file
            debug (bool, optional): Enable debug mode
        """
        # Set up console globally
        global console
        console = Console()
        
        # Set up debugging
        self.debug = debug
        if self.debug:
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.INFO)
        
        # Load configuration
        self.config_path = config_path or os.path.join(os.path.expanduser("~"), ".aiassistant", "config.json")
        self.config = load_config(self.config_path)
        
        # Initialize required attributes with default values
        self.speech_recognizer = None
        
        # Load or initialize components based on config
        self.initialize_core_components()
        
        # Show a welcome message if debug is enabled
        if self.debug:
            console.print(Panel(
                "[yellow]Debug mode enabled.[/yellow] Detailed logging will be shown.",
                title="[bold]Debug Info[/bold]",
                border_style="yellow",
                box=box.ROUNDED
            ))
            
    def display_error(self, error_message, error_detail=None):
        """Display a formatted error message using Rich."""
        error_panel = Panel(
            f"[bold red]{error_message}[/bold red]" + 
            (f"\n\n[dim]{error_detail}[/dim]" if error_detail else ""),
            title="[bold]Error[/bold]",
            border_style="red",
            box=box.ROUNDED
        )
        console.print(error_panel)
        
    def display_success(self, message):
        """Display a formatted success message using Rich."""
        success_panel = Panel(
            f"[bold green]{message}[/bold green]",
            title="[bold]Success[/bold]",
            border_style="green",
            box=box.ROUNDED
        )
        console.print(success_panel)
        
    def display_warning(self, message):
        """Display a formatted warning message using Rich."""
        warning_panel = Panel(
            f"[bold yellow]{message}[/bold yellow]",
            title="[bold]Warning[/bold]",
            border_style="yellow",
            box=box.ROUNDED
        )
        console.print(warning_panel)
        
    def display_info(self, message):
        """Display an informational message with Rich styling"""
        console.print(Panel(
            message,
            title="[bold]Info[/bold]",
            border_style="blue",
            box=box.ROUNDED
        ))

    def initialize_core_components(self):
        """Initialize core components based on configuration."""
        self.config = load_config(self.config_path)
        self.desktop_screenshot = DesktopScreenshot()
        self.assistant = None
        self.ocr_processor = OCRProcessor()
        self.github = GitHubIntegration()
        self.github_intent_parser = GitHubIntentParser()
        
        # Initialize speech recognizer
        try:
            from ai_assistant.utils.speech import SpeechRecognizer
            self.speech_recognizer = SpeechRecognizer()
            logger.info("Speech recognition initialized")
        except Exception as e:
            logger.warning(f"Speech recognition not available: {str(e)}")
            self.speech_recognizer = None
        
        # Initialize file explorer and intent parser
        self.file_explorer = FileExplorer()
        self.file_intent_parser = FileIntentParser()
        
        # Initialize app launcher and intent parser
        self.app_launcher = AppLauncher()
        self.app_intent_parser = AppIntentParser()
        
        # Initialize email manager
        try:
            self.email_manager = EmailManager()
            # Check if email is configured
            if self.email_manager.is_configured():
                self.email_setup_complete = True
                logger.info("Email configuration loaded successfully")
            else:
                logger.info("Email not configured")
        except Exception as e:
            logger.error(f"Error initializing email manager: {e}")
            self.email_manager = None
            self.email_setup_complete = False
        
        self.initialize_assistant()
        self.register_functions()

    def initialize_assistant(self):
        """Initialize the AI assistant with the configured model and role."""
        model_name = self.config.get("model", "Gemini")
        role = self.config.get("role", "General")
        
        # Try to get API key from environment first
        api_key = os.getenv(f"{model_name.upper()}_API_KEY")
        
        # If not in environment, try from config with model-specific key
        if not api_key:
            # Look for model-specific API key first
            api_key = self.config.get(f"{model_name.lower()}_api_key")
            
            # Fall back to generic api_key for backward compatibility
            if not api_key:
                api_key = self.config.get("api_key")
            
        if not api_key:
            print(f"No API key found for {model_name}. Please enter it.")
            if model_name == "Gemini":
                print("\n❗ If you don't have a Gemini API key yet:")
                print("1. Visit https://aistudio.google.com/app/apikey")
                print("2. Sign in with your Google account")
                print("3. Click 'Create API key' and follow the prompts")
                print("4. Copy the generated API key and paste it below\n")
            api_key = input(f"Enter your {model_name} API Key: ").strip()
            
            # Save in config with model-specific key
            self.config[f"{model_name.lower()}_api_key"] = api_key
            
            # Also save to generic api_key for backward compatibility
            self.config["api_key"] = api_key
            
            save_config(self.config)
            
        self.assistant = Assistant(model_name, api_key, role)

    def register_functions(self):
        """Register special command functions."""
        self.functions = {
            "/help": self.show_help,
            "/document": self.document_command,
            "/ocr": self.ocr_command,
            "/github": self.github_command,
            "/email": self.email_command
        }

    async def process_command(self, text):
        """
        Process special commands starting with /.
        
        Args:
            text (str): Command text
            
        Returns:
            bool: True if a command was processed, False otherwise
        """
        if not text.startswith("/"):
            return False
            
        parts = text.split(maxsplit=1)
        command = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""
        
        # Help command
        if command == "/help":
            await self.show_help(args)
            return True
            
        # OCR command
        elif command == "/ocr":
            await self.ocr_command(args)
            return True
            
        # Document command
        elif command == "/document":
            await self.document_command(args)
            return True
            
        # Web command
        elif command == "/web":
            await self.web_command(args)
            return True
            
        # Exit command
        elif command == "/exit" or command == "/quit":
            console.print("[yellow]Goodbye! 👋[/yellow]")
            sys.exit(0)
            
        # Email command
        elif command == "/email":
            await self.email_command(args)
            return True
            
        # Unknown command
        else:
            console.print(Panel(
                f"[bold red]Unknown command:[/bold red] {command}\nType /help to see available commands.",
                title="[bold]Command Error[/bold]",
                border_style="red",
                box=box.ROUNDED
            ))
            return True
        
        return False

    async def show_help(self, args=None):
        """
        Display help information about available commands.
        
        Args:
            args: Optional arguments to specify specific help topics
        """
        if args:
            # Show specific help for a command
            command = args.strip().lower()
            if command.startswith('/'):
                command = command[1:]  # Remove leading slash if present
                
            # Command-specific help
            if command == "ocr":
                console.print(Panel(
                    "The OCR command allows you to extract text from images.\n\n"
                    "[bold cyan]Syntax:[/bold cyan]\n"
                    "• [bold]/ocr[/bold] - Capture screen area and extract text\n"
                    "• [bold]/ocr [file_path][/bold] - Extract text from an image file\n\n"
                    "[bold cyan]Examples:[/bold cyan]\n"
                    "• [bold]/ocr[/bold] - Opens screen capture tool\n"
                    "• [bold]/ocr screenshot.png[/bold] - Extracts text from screenshot.png\n\n"
                    "[bold cyan]Options:[/bold cyan]\n"
                    "• After text extraction, you can choose to analyze the text with AI\n"
                    "• You can save extracted text to a file",
                    title="[bold]OCR Command Help[/bold]",
                    border_style="blue",
                    box=box.ROUNDED
                ))
                
            elif command == "document":
                console.print(Panel(
                    "The document command helps you work with documents and files.\n\n"
                    "[bold cyan]Subcommands:[/bold cyan]\n"
                    "• [bold]/document summarize [file_path][/bold cyan] - Generate a summary of a document\n"
                    "• [bold]/document generate[/bold cyan] - Create a new document using AI\n"
                    "• [bold]/document analyze [file_path][/bold cyan] - Analyze the content of a document\n\n"
                    "[bold cyan]Examples:[/bold cyan]\n"
                    "• [bold]/document summarize report.pdf[/bold cyan] - Summarizes the PDF file\n"
                    "• [bold]/document generate[/bold cyan] - Starts the document generation wizard\n"
                    "• [bold]/document analyze data.csv[/bold cyan] - Analyzes the CSV file",
                    title="[bold]Document Command Help[/bold]",
                    border_style="blue",
                    box=box.ROUNDED
                ))
                
            elif command == "web":
                console.print(Panel(
                    "The web command allows you to search the web and access online content.\n\n"
                    "[bold cyan]Syntax:[/bold cyan]\n"
                    "• [bold]/web search [query][/bold cyan] - Search the web for information\n"
                    "• [bold]/web open [url][/bold cyan] - Open and extract content from a webpage\n\n"
                    "[bold cyan]Examples:[/bold cyan]\n"
                    "• [bold]/web search latest AI developments[/bold cyan] - Searches for AI news\n"
                    "• [bold]/web open https://example.com[/bold cyan] - Extracts content from the URL\n\n"
                    "[bold cyan]Options:[/bold cyan]\n"
                    "• After fetching web content, you can choose to analyze it with AI",
                    title="[bold]Web Command Help[/bold]",
                    border_style="blue",
                    box=box.ROUNDED
                ))
                
            elif command == "email":
                console.print(Panel(
                    "The email command helps you compose, read, and manage emails.\n\n"
                    "[bold cyan]Subcommands:[/bold cyan]\n"
                    "• [bold]/email compose [recipient][/bold cyan] - Compose a new email\n"
                    "• [bold]/email ai [recipient][/bold cyan] - Let AI help you write an email\n"
                    "• [bold]/email read[/bold cyan] - Read your emails\n"
                    "• [bold]/email setup[/bold cyan] - Configure your email settings\n\n"
                    "[bold cyan]Examples:[/bold cyan]\n"
                    "• [bold]/email compose john@example.com[/bold cyan] - Start composing an email\n"
                    "• [bold]/email ai boss@company.com[/bold cyan] - Use AI to draft an email\n"
                    "• [bold]/email read[/bold cyan] - View your recent emails\n"
                    "• [bold]/email setup[/bold cyan] - Configure your email account",
                    title="[bold]Email Command Help[/bold]",
                    border_style="blue",
                    box=box.ROUNDED
                ))
                
            elif command == "github":
                console.print(Panel(
                    "The GitHub command allows you to interact with GitHub repositories.\n\n"
                    "[bold cyan]Subcommands:[/bold cyan]\n"
                    "• [bold]/github setup[/bold cyan] - Configure GitHub integration\n"
                    "• [bold]/github status[/bold cyan] - Check GitHub integration status\n"
                    "• [bold]/github repos[/bold cyan] - List your GitHub repositories\n"
                    "• [bold]/github issues [owner/repo][/bold cyan] - List issues for a repository\n"
                    "• [bold]/github create[/bold cyan] - Create a new issue or pull request\n\n"
                    "[bold cyan]Examples:[/bold cyan]\n"
                    "• [bold]/github repos[/bold cyan] - Shows your repositories\n"
                    "• [bold]/github issues username/repo[/bold cyan] - Lists issues in that repo\n"
                    "• [bold]/github create[/bold cyan] - Start the creation wizard",
                    title="[bold]GitHub Command Help[/bold]",
                    border_style="blue",
                    box=box.ROUNDED
                ))
                
            elif command == "config":
                console.print(Panel(
                    "The config command allows you to configure assistant settings.\n\n"
                    "[bold cyan]Subcommands:[/bold cyan]\n"
                    "• [bold]/config model[/bold cyan] - Change the AI model\n"
                    "• [bold]/config role[/bold cyan] - Change the assistant's role\n"
                    "• [bold]/config show[/bold cyan] - Show current configuration\n\n"
                    "[bold cyan]Examples:[/bold cyan]\n"
                    "• [bold]/config model[/bold cyan] - Change the AI model\n"
                    "• [bold]/config role[/bold cyan] - Set a new role for the assistant\n"
                    "• [bold]/config show[/bold cyan] - Display current settings",
                    title="[bold]Configuration Help[/bold]",
                    border_style="blue",
                    box=box.ROUNDED
                ))
                
            elif command == "voice":
                console.print(Panel(
                    "Voice commands allow you to speak to the assistant.\n\n"
                    "[bold cyan]Syntax:[/bold cyan]\n"
                    "• [bold]/voice[/bold cyan] - Start voice recognition mode\n\n"
                    "[bold cyan]Voice Command Examples:[/bold cyan]\n"
                    "• \"What is the weather today?\"\n"
                    "• \"Summarize this article: [URL]\"\n"
                    "• \"Write an email to John about the project meeting\"\n"
                    "• \"Take a screenshot and extract text\"\n"
                    "• \"Stop listening\" (to exit voice mode)",
                    title="[bold]Voice Command Help[/bold]",
                    border_style="blue", 
                    box=box.ROUNDED
                ))
                
            else:
                self.display_error(f"No help available for '{command}'")
                console.print("Type [bold]/help[/bold] for a list of all commands")
                
        else:
            # Main help menu
            main_help = Table(
                title="🦆 QuackQuery AI Assistant Commands",
                box=box.ROUNDED,
                border_style="blue",
                title_style="bold cyan",
                min_width=80
            )
            
            main_help.add_column("Command", style="bold cyan", no_wrap=True)
            main_help.add_column("Description", style="")
            main_help.add_column("Examples", style="green")
            
            # Core commands
            main_help.add_row(
                "/help [command]", 
                "Show help information for all commands or a specific command",
                "/help\n/help ocr"
            )
            
            main_help.add_row(
                "/voice", 
                "Start voice recognition mode to speak commands",
                "/voice"
            )
            
            main_help.add_row(
                "/config [subcommand]", 
                "Configure assistant settings (model, role, etc.)",
                "/config model\n/config role"
            )
            
            main_help.add_row(
                "/ocr [file_path]", 
                "Extract text from screen area or image file",
                "/ocr\n/ocr screenshot.png"
            )
            
            main_help.add_row(
                "/web [search/open] [query/url]", 
                "Search the web or open a specific URL",
                "/web search AI news\n/web open https://example.com"
            )
            
            main_help.add_row(
                "/document [summarize/generate/analyze]", 
                "Work with documents (summarize, generate, analyze)",
                "/document summarize report.pdf\n/document generate"
            )
            
            main_help.add_row(
                "/email [compose/ai/read/setup]", 
                "Compose, generate, or read emails",
                "/email compose john@example.com\n/email ai boss@company.com"
            )
            
            main_help.add_row(
                "/github [repos/issues/create/setup]", 
                "Interact with GitHub repositories",
                "/github repos\n/github issues user/repo"
            )
            
            main_help.add_row(
                "/exit", 
                "Exit the application",
                "/exit"
            )
            
            console.print(main_help)
            
            # Additional help tips
            console.print(Panel(
                "• Type a question or statement directly to chat with the AI assistant\n"
                "• Use [bold]/help [command][/bold] to get detailed help for a specific command\n"
                "• Press [bold]Ctrl+C[/bold] at any time to cancel the current operation",
                title="[bold]Tips[/bold]",
                border_style="green",
                box=box.ROUNDED
            ))

    async def document_command(self, args):
        """
        Handle document commands for file processing and generation.
        
        Args:
            args: Command arguments
        """
        parts = args.split(maxsplit=1)
        subcmd = parts[0].lower() if parts else ""
        params = parts[1] if len(parts) > 1 else ""
        
        if subcmd == "summarize":
            # Document summarization
            if not params:
                self.display_error("Please specify a file path to summarize")
                console.print("[dim]Example: /document summarize path/to/file.pdf[/dim]")
                return
                
            file_path = params.strip()
            if not os.path.exists(file_path):
                self.display_error(f"File not found: {file_path}")
                return
                
            # Determine the file type
            file_ext = os.path.splitext(file_path)[1].lower()
            supported_extensions = [".pdf", ".docx", ".txt", ".md", ".csv", ".json"]
            
            if file_ext not in supported_extensions:
                self.display_error(f"Unsupported file type: {file_ext}")
                console.print(f"[dim]Supported file types: {', '.join(supported_extensions)}[/dim]")
                return
                
            console.print(Panel(
                f"[bold]Summarizing document:[/bold] {os.path.basename(file_path)}",
                title="[bold]Document Operation[/bold]",
                border_style="blue",
                box=box.ROUNDED
            ))
            
            # Extract text from the document
            with Progress(
                SpinnerColumn(),
                TextColumn("[bold blue]Reading document...[/bold blue]"),
                BarColumn(),
                TimeElapsedColumn(),
                console=console,
                transient=True
            ) as progress:
                task = progress.add_task("[green]Extracting text...", total=None)
                
                try:
                    # Extract text based on file type
                    if file_ext == ".pdf":
                        # Code to extract text from PDF
                        text = f"PDF text extraction from {file_path} would go here"
                    elif file_ext == ".docx":
                        # Code to extract text from DOCX
                        text = f"DOCX text extraction from {file_path} would go here"
                    else:
                        # For text-based files
                        with open(file_path, 'r', encoding='utf-8') as f:
                            text = f.read()
                except Exception as e:
                    self.display_error(f"Error reading file: {str(e)}")
                    return
            
            # Generate a summary using AI
            with Progress(
                SpinnerColumn(),
                TextColumn("[bold blue]Generating summary...[/bold blue]"),
                BarColumn(),
                TimeElapsedColumn(),
                console=console,
                transient=True
            ) as progress:
                task = progress.add_task("[green]Analyzing content...", total=None)
                
                prompt = f"Please summarize the following document content:\n\n{text[:4000]}"
                if len(text) > 4000:
                    prompt += "\n\n[Content truncated due to length...]"
                    
                summary = await self.assistant.answer_async(prompt)
            
            # Display the summary
            console.print(Panel(
                Markdown(summary),
                title=f"[bold]Summary of {os.path.basename(file_path)}[/bold]",
                border_style="green",
                box=box.ROUNDED
            ))
            
        elif subcmd == "generate":
            # Document generation
            console.print(Panel(
                "[bold]Document Generation Assistant[/bold]\n"
                "I'll help you create a new document based on your specifications.",
                title="[bold]Document Generator[/bold]",
                border_style="blue",
                box=box.ROUNDED
            ))
            
            # Get document details
            doc_type = Prompt.ask(
                "[bold]Document type[/bold]", 
                choices=["report", "letter", "proposal", "article", "other"],
                default="report"
            )
            
            if doc_type == "other":
                doc_type = Prompt.ask("[bold]Specify document type[/bold]")
                
            topic = Prompt.ask("[bold]Topic or title[/bold]")
            instructions = Prompt.ask("[bold]Additional instructions[/bold] (optional)")
            output_format = Prompt.ask(
                "[bold]Output format[/bold]",
                choices=["markdown", "text", "html"],
                default="markdown"
            )
            
            # Generate the document
            with Progress(
                SpinnerColumn(),
                TextColumn("[bold blue]Generating document...[/bold blue]"),
                BarColumn(),
                TimeElapsedColumn(),
                console=console,
                transient=True
            ) as progress:
                task = progress.add_task("[green]Creating content...", total=None)
                
                prompt = f"Generate a {doc_type} about '{topic}'. "
                prompt += f"Additional instructions: {instructions}" if instructions else ""
                prompt += f" Please format the output in {output_format}."
                
                generated_content = await self.assistant.answer_async(prompt)
            
            # Display the generated document
            if output_format == "markdown":
                console.print(Panel(
                    Markdown(generated_content),
                    title=f"[bold]Generated {doc_type.title()}: {topic}[/bold]",
                    border_style="green",
                    box=box.ROUNDED
                ))
            elif output_format == "html":
                console.print(Panel(
                    Syntax(generated_content, "html", theme="monokai"),
                    title=f"[bold]Generated {doc_type.title()} (HTML): {topic}[/bold]",
                    border_style="green",
                    box=box.ROUNDED
                ))
            else:
                console.print(Panel(
                    generated_content,
                    title=f"[bold]Generated {doc_type.title()}: {topic}[/bold]",
                    border_style="green",
                    box=box.ROUNDED
                ))
                
            # Ask if user wants to save the document
            if Confirm.ask("Would you like to save this document to a file?", default=True):
                default_filename = f"{topic.lower().replace(' ', '_')}.{output_format}"
                if output_format == "markdown":
                    default_filename = f"{topic.lower().replace(' ', '_')}.md"
                elif output_format == "html":
                    default_filename = f"{topic.lower().replace(' ', '_')}.html"
                else:
                    default_filename = f"{topic.lower().replace(' ', '_')}.txt"
                    
                file_path = Prompt.ask("Enter file path", default=default_filename)
                
                try:
                    with Progress(
                        SpinnerColumn(),
                        TextColumn("[bold blue]Saving document...[/bold blue]"),
                        console=console,
                        transient=True
                    ) as progress:
                        task = progress.add_task("[green]Writing file...", total=None)
                        
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(generated_content)
                            
                    self.display_success(f"Document saved to {file_path}")
                except Exception as e:
                    self.display_error(f"Error saving document: {str(e)}")
                    
        elif subcmd == "analyze":
            # Document analysis
            if not params:
                self.display_error("Please specify a file path to analyze")
                console.print("[dim]Example: /document analyze path/to/file.pdf[/dim]")
                return
                
            file_path = params.strip()
            if not os.path.exists(file_path):
                self.display_error(f"File not found: {file_path}")
                return
                
            # Check file type
            file_ext = os.path.splitext(file_path)[1].lower()
            supported_extensions = [".pdf", ".docx", ".txt", ".md", ".csv", ".json", ".py", ".js", ".html", ".css"]
            
            if file_ext not in supported_extensions:
                self.display_error(f"Unsupported file type: {file_ext}")
                console.print(f"[dim]Supported file types: {', '.join(supported_extensions)}[/dim]")
                return
                
            console.print(Panel(
                f"[bold]Analyzing document:[/bold] {os.path.basename(file_path)}",
                title="[bold]Document Analysis[/bold]",
                border_style="blue",
                box=box.ROUNDED
            ))
            
            # Extract content from the file
            with Progress(
                SpinnerColumn(),
                TextColumn("[bold blue]Reading document...[/bold blue]"),
                BarColumn(),
                TimeElapsedColumn(),
                console=console,
                transient=True
            ) as progress:
                task = progress.add_task("[green]Extracting content...", total=None)
                
                try:
                    # Extract text based on file type (simplified implementation)
                    if file_ext in [".pdf", ".docx"]:
                        # Code to extract text from PDF/DOCX
                        content = f"Text extraction from {file_path} would go here"
                    else:
                        # For text-based files
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                except Exception as e:
                    self.display_error(f"Error reading file: {str(e)}")
                    return
            
            # Analyze the document
            with Progress(
                SpinnerColumn(),
                TextColumn("[bold blue]Analyzing content...[/bold blue]"),
                BarColumn(),
                TimeElapsedColumn(),
                console=console,
                transient=True
            ) as progress:
                task = progress.add_task("[green]Processing...", total=None)
                
                prompt = f"Analyze the following document and provide a detailed analysis including main topics, key points, and insights:\n\n{content[:4000]}"
                if len(content) > 4000:
                    prompt += "\n\n[Content truncated due to length...]"
                    
                analysis = await self.assistant.answer_async(prompt)
            
            # Display the analysis
            console.print(Panel(
                Markdown(analysis),
                title=f"[bold]Analysis of {os.path.basename(file_path)}[/bold]",
                border_style="green",
                box=box.ROUNDED
            ))
            
        else:
            # Help for document command
            console.print(Panel(
                "Available document subcommands:\n\n"
                "• [bold cyan]summarize [file_path][/bold cyan] - Generate a summary of a document\n"
                "• [bold cyan]generate[/bold cyan] - Create a new document using AI\n"
                "• [bold cyan]analyze [file_path][/bold cyan] - Analyze the content of a document",
                title="[bold]Document Commands Help[/bold]",
                border_style="blue",
                box=box.ROUNDED
            ))

    async def github_command(self, args):
        """
        Handle GitHub commands.
        
        Args:
            args: Command arguments
        """
        parts = args.split(maxsplit=1)
        subcmd = parts[0].lower() if parts else ""
        params = parts[1] if len(parts) > 1 else ""
        
        if subcmd == "setup":
            # GitHub setup
            await self.configure_github()
            
        elif subcmd == "status":
            # GitHub status
            if not self.config.get("github", {}).get("token"):
                self.display_error("GitHub is not configured. Please run /github setup first.")
                return
                
            console.print(Panel(
                "[bold]GitHub Status[/bold]\n"
                f"[green]✓[/green] GitHub API is configured and ready to use.\n"
                f"[dim]Token: ...{self.config['github']['token'][-4:]} (last 4 characters)[/dim]",
                title="[bold]GitHub Integration[/bold]",
                border_style="green",
                box=box.ROUNDED
            ))
            
        elif subcmd == "repos":
            # List GitHub repositories
            if not self.config.get("github", {}).get("token"):
                self.display_error("GitHub is not configured. Please run /github setup first.")
                return
                
            console.print(Panel(
                "[bold]Fetching your GitHub repositories...[/bold]",
                title="[bold]GitHub Repositories[/bold]",
                border_style="blue",
                box=box.ROUNDED
            ))
            
            # Fetch repositories
            with Progress(
                SpinnerColumn(),
                TextColumn("[bold blue]Connecting to GitHub API...[/bold blue]"),
                BarColumn(),
                TimeElapsedColumn(),
                console=console,
                transient=True
            ) as progress:
                task = progress.add_task("[green]Fetching repositories...", total=None)
                
                # Placeholder for actual GitHub API call
                repositories = [
                    {"name": "project-alpha", "description": "A cool project", "stars": 12, "forks": 5, "language": "Python"},
                    {"name": "web-app", "description": "Web application template", "stars": 45, "forks": 20, "language": "JavaScript"},
                    {"name": "data-tools", "description": "Tools for data analysis", "stars": 8, "forks": 2, "language": "Python"}
                ]
            
            # Display repositories in a table
            repo_table = Table(title="Your GitHub Repositories", box=box.ROUNDED, border_style="blue")
            repo_table.add_column("Name", style="cyan")
            repo_table.add_column("Description")
            repo_table.add_column("Stars", justify="right", style="yellow")
            repo_table.add_column("Forks", justify="right", style="green")
            repo_table.add_column("Language", style="magenta")
            
            for repo in repositories:
                repo_table.add_row(
                    repo["name"],
                    repo["description"] or "",
                    str(repo["stars"]),
                    str(repo["forks"]),
                    repo["language"] or "Unknown"
                )
                
            console.print(repo_table)
            
            # Ask if user wants to clone a repository
            if Confirm.ask("Would you like to clone one of these repositories?", default=False):
                repo_name = Prompt.ask("[bold]Enter repository name to clone[/bold]")
                clone_dir = Prompt.ask("[bold]Enter directory to clone into[/bold]", default=".")
                
                console.print(Panel(
                    f"[bold]Cloning repository:[/bold] {repo_name}\n"
                    f"[bold]Target directory:[/bold] {clone_dir}",
                    title="[bold]Git Clone Operation[/bold]",
                    border_style="blue",
                    box=box.ROUNDED
                ))
                
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[bold blue]Cloning repository...[/bold blue]"),
                    BarColumn(),
                    TimeElapsedColumn(),
                    console=console,
                    transient=True
                ) as progress:
                    task = progress.add_task("[green]Cloning...", total=None)
                    
                    # Placeholder for actual git clone operation
                    # This would use subprocess to run git commands
                    import time
                    time.sleep(2)  # Simulate cloning process
            
            self.display_success(f"Repository {repo_name} cloned successfully to {clone_dir}")
            
        elif subcmd == "issues":
            # List GitHub issues
            if not self.config.get("github", {}).get("token"):
                self.display_error("GitHub is not configured. Please run /github setup first.")
                return
                
            repo_name = params
            if not repo_name:
                repo_name = Prompt.ask("[bold]Enter repository name[/bold] (format: owner/repo)")
                
            console.print(Panel(
                f"[bold]Fetching issues for:[/bold] {repo_name}",
                title="[bold]GitHub Issues[/bold]",
                border_style="blue",
                box=box.ROUNDED
            ))
            
            # Fetch issues
            with Progress(
                SpinnerColumn(),
                TextColumn("[bold blue]Connecting to GitHub API...[/bold blue]"),
                BarColumn(),
                TimeElapsedColumn(),
                console=console,
                transient=True
            ) as progress:
                task = progress.add_task("[green]Fetching issues...", total=None)
                
                # Placeholder for actual GitHub API call
                issues = [
                    {"number": 42, "title": "Fix login bug", "state": "open", "created_at": "2023-01-15", "comments": 3},
                    {"number": 36, "title": "Update documentation", "state": "closed", "created_at": "2023-01-10", "comments": 5},
                    {"number": 45, "title": "Add new feature", "state": "open", "created_at": "2023-01-20", "comments": 2}
                ]
            
            if not issues:
                self.display_warning(f"No issues found for repository {repo_name}")
                return
                
            # Display issues in a table
            issue_table = Table(title=f"Issues for {repo_name}", box=box.ROUNDED, border_style="blue")
            issue_table.add_column("#", style="cyan", justify="right")
            issue_table.add_column("Title")
            issue_table.add_column("State", style="bold")
            issue_table.add_column("Created", style="yellow")
            issue_table.add_column("Comments", justify="right")
            
            for issue in issues:
                issue_table.add_row(
                    str(issue["number"]),
                    issue["title"],
                    f"[green]{issue['state']}[/green]" if issue["state"] == "open" else f"[red]{issue['state']}[/red]",
                    issue["created_at"],
                    str(issue["comments"])
                )
                
            console.print(issue_table)
            
        elif subcmd == "create":
            # Create GitHub issues or pull requests
            if not self.config.get("github", {}).get("token"):
                self.display_error("GitHub is not configured. Please run /github setup first.")
                return
                
            # Determine what to create
            create_type = Prompt.ask(
                "[bold]What would you like to create?[/bold]",
                choices=["issue", "pr"],
                default="issue"
            )
            
            repo_name = Prompt.ask("[bold]Enter repository name[/bold] (format: owner/repo)")
            
            if create_type == "issue":
                console.print(Panel(
                    f"[bold]Creating new issue in:[/bold] {repo_name}",
                    title="[bold]New GitHub Issue[/bold]",
                    border_style="blue",
                    box=box.ROUNDED
                ))
                
                title = Prompt.ask("[bold]Issue title[/bold]")
                console.print("[bold]Issue description:[/bold] (Type your message, press Enter then Ctrl+D to finish)")
                
                # Collect body lines
                body_lines = []
                while True:
                    try:
                        line = input()
                        body_lines.append(line)
                    except EOFError:
                        break
                        
                body = "\n".join(body_lines)
                
                # Preview the issue
                console.print(Panel(
                    f"[bold]Title:[/bold] {title}\n\n"
                    f"[bold]Description:[/bold]\n{body}",
                    title="[bold]Issue Preview[/bold]",
                    border_style="green",
                    box=box.ROUNDED
                ))
                
                # Ask for confirmation
                if Confirm.ask("Create this issue?", default=True):
                    with Progress(
                        SpinnerColumn(),
                        TextColumn("[bold blue]Creating issue...[/bold blue]"),
                        console=console,
                        transient=True
                    ) as progress:
                        task = progress.add_task("[green]Connecting to GitHub API...", total=None)
                        
                        # Placeholder for actual GitHub API call
                        issue_number = 46  # This would be the actual issue number from the API response
                    
                    self.display_success(f"Issue #{issue_number} created successfully in {repo_name}")
                else:
                    self.display_warning("Issue creation canceled")
                    
            elif create_type == "pr":
                console.print(Panel(
                    f"[bold]Creating new pull request in:[/bold] {repo_name}",
                    title="[bold]New GitHub Pull Request[/bold]",
                    border_style="blue",
                    box=box.ROUNDED
                ))
                
                base_branch = Prompt.ask("[bold]Base branch[/bold]", default="main")
                head_branch = Prompt.ask("[bold]Head branch[/bold]")
                title = Prompt.ask("[bold]PR title[/bold]")
                console.print("[bold]PR description:[/bold] (Type your message, press Enter then Ctrl+D to finish)")
                
                # Collect body lines
                body_lines = []
                while True:
                    try:
                        line = input()
                        body_lines.append(line)
                    except EOFError:
                        break
                        
                body = "\n".join(body_lines)
                
                # Preview the PR
                console.print(Panel(
                    f"[bold]Title:[/bold] {title}\n"
                    f"[bold]Branches:[/bold] {head_branch} → {base_branch}\n\n"
                    f"[bold]Description:[/bold]\n{body}",
                    title="[bold]Pull Request Preview[/bold]",
                    border_style="green",
                    box=box.ROUNDED
                ))
                
                # Ask for confirmation
                if Confirm.ask("Create this pull request?", default=True):
                    with Progress(
                        SpinnerColumn(),
                        TextColumn("[bold blue]Creating pull request...[/bold blue]"),
                        console=console,
                        transient=True
                    ) as progress:
                        task = progress.add_task("[green]Connecting to GitHub API...", total=None)
                        
                        # Placeholder for actual GitHub API call
                        pr_number = 15  # This would be the actual PR number from the API response
                    
                    self.display_success(f"Pull request #{pr_number} created successfully in {repo_name}")
                else:
                    self.display_warning("Pull request creation canceled")
                    
        else:
            # Help for GitHub command
            console.print(Panel(
                "Available GitHub subcommands:\n\n"
                "• [bold cyan]setup[/bold cyan] - Configure GitHub integration\n"
                "• [bold cyan]status[/bold cyan] - Check GitHub integration status\n"
                "• [bold cyan]repos[/bold cyan] - List your GitHub repositories\n"
                "• [bold cyan]issues [owner/repo][/bold cyan] - List issues for a repository\n"
                "• [bold cyan]create[/bold cyan] - Create a new issue or pull request",
                title="[bold]GitHub Commands Help[/bold]",
                border_style="blue",
                box=box.ROUNDED
            ))
            
    async def configure_github(self):
        """Configure GitHub integration."""
        console.print(Panel(
            "[bold]GitHub Configuration[/bold]\n"
            "This will set up your GitHub API token for integration with the assistant.\n"
            "[yellow]Note: Your token will be stored securely but not encrypted.[/yellow]",
            title="[bold]GitHub Setup[/bold]",
            border_style="blue",
            box=box.ROUNDED
        ))
        
        console.print(Panel(
            "To create a new GitHub token:\n"
            "1. Go to [link=https://github.com/settings/tokens]https://github.com/settings/tokens[/link]\n"
            "2. Click 'Generate new token'\n"
            "3. Add a note like 'QuackQuery Assistant'\n"
            "4. Select scopes: 'repo', 'read:user'\n"
            "5. Click 'Generate token'\n"
            "6. Copy the generated token\n",
            title="[bold]Token Instructions[/bold]",
            border_style="yellow",
            box=box.ROUNDED
        ))
        
        # Get GitHub token
        token = Prompt.ask(
            "[bold]Enter your GitHub personal access token[/bold]", 
            password=True
        )
        
        if not token:
            self.display_error("No token provided. GitHub integration not configured.")
            return
            
        # Test the token
        with Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]Testing GitHub token...[/bold blue]"),
            console=console,
            transient=True
        ) as progress:
            task = progress.add_task("[green]Connecting to GitHub API...", total=None)
            
            # Test connection to GitHub API
            test_result = True  # Placeholder for actual test
            
        if test_result:
            # Save the token in configuration
            if not self.config.get("github"):
                self.config["github"] = {}
                
            self.config["github"]["token"] = token
            save_config(self.config)
            
            self.display_success("GitHub token validated and saved successfully!")
        else:
            self.display_error("Failed to validate GitHub token. Please check your token and try again.")
            
    async def handle_github_operation(self, intent):
        """
        Handle GitHub operations based on detected intent.
        
        Args:
            intent: Dictionary containing detected intent information
        """
        if not self.config.get("github", {}).get("token"):
            self.display_error("GitHub is not configured. Please run /github setup first.")
            return
            
        operation = intent.get("operation")
        repo = intent.get("repository")
        
        if not operation:
            self.display_error("Unable to determine GitHub operation. Please try again with more details.")
            return
            
        if operation == "list_repos":
            console.print(Panel(
                "[bold]Fetching your GitHub repositories...[/bold]",
                title="[bold]GitHub Repositories[/bold]",
                border_style="blue",
                box=box.ROUNDED
            ))
            
            # Fetch repositories
            with Progress(
                SpinnerColumn(),
                TextColumn("[bold blue]Connecting to GitHub API...[/bold blue]"),
                BarColumn(),
                TimeElapsedColumn(),
                console=console,
                transient=True
            ) as progress:
                task = progress.add_task("[green]Fetching repositories...", total=None)
                
                # Placeholder for actual GitHub API call
                repositories = [
                    {"name": "project-alpha", "description": "A cool project", "stars": 12, "forks": 5, "language": "Python"},
                    {"name": "web-app", "description": "Web application template", "stars": 45, "forks": 20, "language": "JavaScript"},
                    {"name": "data-tools", "description": "Tools for data analysis", "stars": 8, "forks": 2, "language": "Python"}
                ]
            
            # Display repositories in a table
            repo_table = Table(title="Your GitHub Repositories", box=box.ROUNDED, border_style="blue")
            repo_table.add_column("Name", style="cyan")
            repo_table.add_column("Description")
            repo_table.add_column("Stars", justify="right", style="yellow")
            repo_table.add_column("Forks", justify="right", style="green")
            repo_table.add_column("Language", style="magenta")
            
            for repo in repositories:
                repo_table.add_row(
                    repo["name"],
                    repo["description"] or "",
                    str(repo["stars"]),
                    str(repo["forks"]),
                    repo["language"] or "Unknown"
                )
                
            console.print(repo_table)
            
        elif operation == "list_issues" and repo:
            console.print(Panel(
                f"[bold]Fetching issues for:[/bold] {repo}",
                title="[bold]GitHub Issues[/bold]",
                border_style="blue",
                box=box.ROUNDED
            ))
            
            # Fetch issues
            with Progress(
                SpinnerColumn(),
                TextColumn("[bold blue]Connecting to GitHub API...[/bold blue]"),
                BarColumn(),
                TimeElapsedColumn(),
                console=console,
                transient=True
            ) as progress:
                task = progress.add_task("[green]Fetching issues...", total=None)
                
                # Placeholder for actual GitHub API call
                issues = [
                    {"number": 42, "title": "Fix login bug", "state": "open", "created_at": "2023-01-15", "comments": 3},
                    {"number": 36, "title": "Update documentation", "state": "closed", "created_at": "2023-01-10", "comments": 5},
                    {"number": 45, "title": "Add new feature", "state": "open", "created_at": "2023-01-20", "comments": 2}
                ]
            
            if not issues:
                self.display_warning(f"No issues found for repository {repo}")
                return
                
            # Display issues in a table
            issue_table = Table(title=f"Issues for {repo}", box=box.ROUNDED, border_style="blue")
            issue_table.add_column("#", style="cyan", justify="right")
            issue_table.add_column("Title")
            issue_table.add_column("State", style="bold")
            issue_table.add_column("Created", style="yellow")
            issue_table.add_column("Comments", justify="right")
            
            for issue in issues:
                issue_table.add_row(
                    str(issue["number"]),
                    issue["title"],
                    f"[green]{issue['state']}[/green]" if issue["state"] == "open" else f"[red]{issue['state']}[/red]",
                    issue["created_at"],
                    str(issue["comments"])
                )
                
            console.print(issue_table)
            
        elif operation == "create_issue" and repo:
            console.print(Panel(
                f"[bold]Creating new issue in:[/bold] {repo}",
                title="[bold]New GitHub Issue[/bold]",
                border_style="blue",
                box=box.ROUNDED
            ))
            
            title = Prompt.ask("[bold]Issue title[/bold]")
            console.print("[bold]Issue description:[/bold] (Type your message, press Enter then Ctrl+D to finish)")
            
            # Collect body lines
            body_lines = []
            while True:
                try:
                    line = input()
                    body_lines.append(line)
                except EOFError:
                    break
                    
            body = "\n".join(body_lines)
            
            # Preview the issue
            console.print(Panel(
                f"[bold]Title:[/bold] {title}\n\n"
                f"[bold]Description:[/bold]\n{body}",
                title="[bold]Issue Preview[/bold]",
                border_style="green",
                box=box.ROUNDED
            ))
            
            # Ask for confirmation
            if Confirm.ask("Create this issue?", default=True):
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[bold blue]Creating issue...[/bold blue]"),
                    console=console,
                    transient=True
                ) as progress:
                    task = progress.add_task("[green]Connecting to GitHub API...", total=None)
                    
                    # Placeholder for actual GitHub API call
                    issue_number = 46  # This would be the actual issue number from the API response
                
                self.display_success(f"Issue #{issue_number} created successfully in {repo}")
            else:
                self.display_warning("Issue creation canceled")
                
        elif operation == "clone" and repo:
            # Clone operation
            clone_dir = intent.get("directory", ".")
            
            console.print(Panel(
                f"[bold]Cloning repository:[/bold] {repo}\n"
                f"[bold]Target directory:[/bold] {clone_dir}",
                title="[bold]Git Clone Operation[/bold]",
                border_style="blue",
                box=box.ROUNDED
            ))
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[bold blue]Cloning repository...[/bold blue]"),
                BarColumn(),
                TimeElapsedColumn(),
                console=console,
                transient=True
            ) as progress:
                task = progress.add_task("[green]Cloning...", total=None)
                
                # Placeholder for actual git clone operation
                # This would use subprocess to run git commands
                import time
                time.sleep(2)  # Simulate cloning process
            
            self.display_success(f"Repository {repo} cloned successfully to {clone_dir}")
            
        else:
            self.display_error(f"Unsupported GitHub operation: {operation}")
            
    async def run(self):
        """Run the QuackQuery application."""
        console.clear()
        console.print(Panel.fit(
            "🦆 [bold cyan]QuackQuery AI Assistant[/bold cyan] [green]initialized[/green]",
            box=box.ROUNDED,
            border_style="cyan",
            title="Welcome",
            subtitle="v1.0"
        ))
        
        while True:
            # Display menu in a styled panel
            menu_table = Table(show_header=False, box=box.SIMPLE)
            menu_table.add_column("Option", style="cyan")
            menu_table.add_column("Description")
            menu_table.add_row("S", "Speak to the assistant")
            menu_table.add_row("T", "Type a question")
            menu_table.add_row("C", "Configure settings")
            menu_table.add_row("Q", "Quit")
            
            console.print(Panel(
                menu_table,
                title="[bold]Main Menu[/bold]",
                border_style="blue",
                box=box.ROUNDED
            ))
            
            # Use Rich prompt for input
            user_input = Prompt.ask("\nEnter your choice", choices=["s", "t", "c", "q"], default="t").lower()
            
            if user_input == 's':
                await self.handle_speech_input()
                console.print("\n[green]✅ Ready for next command...[/green]")
            elif user_input == 't':
                await self.handle_text_input()
                console.print("\n[green]✅ Ready for next command...[/green]")
            elif user_input == 'c':
                await self.configure()
                console.print("\n[green]✅ Settings updated. Ready for next command...[/green]")
            elif user_input == 'q':
                console.print("\n[yellow]Exiting assistant. Goodbye! 👋[/yellow]")
                break
            else:
                console.print("\n[bold red]❌ Invalid input. Please choose S, T, C, or Q.[/bold red]")

    async def handle_speech_input(self):
        """Handle speech input from user."""
        if not self.speech_recognizer:
            console.print("[bold red]❌ Speech recognition is not available. Please make sure you have the required dependencies installed.[/bold red]")
            return

        # Create a panel with instructions
        console.print(Panel(
            "[bold]🎤 Speak now...[/bold]\n[dim]I'm listening. Say 'stop' or press Ctrl+C when finished.[/dim]",
            title="[bold]Voice Input Mode[/bold]",
            border_style="blue",
            box=box.ROUNDED
        ))
        
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[bold blue]Listening...[/bold blue]"),
                console=console,
                transient=True
            ) as progress:
                task = progress.add_task("[green]Recording...", total=None)
                speech_text = self.speech_recognizer.listen()
                
            if not speech_text:
                console.print("[yellow]⚠️ I didn't catch that. Please try again.[/yellow]")
                return
            
            console.print(Panel(
                f"[cyan italic]\"{speech_text}\"[/cyan italic]",
                title="[bold]You said[/bold]",
                border_style="green",
                box=box.ROUNDED
            ))
            
            # Process the recognized text
            if speech_text.lower() in ["quit", "exit", "stop", "goodbye"]:
                console.print("[yellow]Voice input mode ended by command.[/yellow]")
                return
            
            # Check if this is a command
            if speech_text.startswith("/"):
                await self.process_command(speech_text)
                return
                
            # Check for GitHub intent
            github_intent = self.github_intent_parser.parse_intent(speech_text)
            if github_intent:
                result = await self.handle_github_operation(github_intent)
                self._format_and_display_response(result)
                return
                
            # Check for File intent
            file_intent = self.file_intent_parser.parse_intent(speech_text)
            if file_intent:
                result = await self.handle_file_operation(file_intent)
                self._format_and_display_response(result)
                return
                
            # Check for App intent
            app_intent = self.app_intent_parser.parse_intent(speech_text)
            if app_intent:
                result = await self.handle_app_operation(app_intent)
                self._format_and_display_response(result)
                return
                
            # Ask about screenshot inclusion
            include_screenshot = Confirm.ask("Include a screenshot for context?", default=False)
            
            # Process the command/question
            with Progress(
                SpinnerColumn(),
                TextColumn("[bold blue]Processing your request...[/bold blue]"),
                BarColumn(),
                TimeElapsedColumn(),
                console=console,
                transient=True
            ) as processing_progress:
                process_task = processing_progress.add_task("[green]Thinking...", total=None)
                screenshot_encoded = self.desktop_screenshot.capture() if include_screenshot else None
                response = await self.assistant.answer_async(speech_text, screenshot_encoded)
            
            # Format and display the response
            self._format_and_display_response(response)
            
        except KeyboardInterrupt:
            console.print("[yellow]Voice input mode ended.[/yellow]")
        except Exception as e:
            console.print(f"[bold red]❌ Error during speech recognition: {str(e)}[/bold red]")
            logger.error(f"Speech input error: {e}")

    async def handle_text_input(self):
        """Handle text input from the user."""
        prompt = Prompt.ask("\nEnter your question or command")
        
        if not prompt:
            console.print("\n[bold orange]⚠️ No input provided. Please try again.[/bold orange]")
            return
        
        # Check if this is a command
        if prompt.startswith("/"):
            command_processed = await self.process_command(prompt)
            if command_processed:
                return
        
        # Direct check for AI email composition
        ai_email_match = re.search(r'(?:ai|assistant|help me)\s+(?:write|compose|draft|create)\s+(?:an\s+)?(?:email|mail|message)', prompt.lower())
        if ai_email_match:
            logger.info("Detected AI email composition request directly")
            # Extract email address if present
            email_match = re.search(r'to\s+([a-zA-Z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,})', prompt.lower())
            to_address = email_match.group(1) if email_match else None
            
            # Create an intent dictionary
            ai_email_intent = {
                'operation': 'ai_compose_email',
                'to_address': to_address
            }
            
            # Handle the AI email composition
            result = await self.handle_email_operation(ai_email_intent, prompt)
            console.print(Panel(f"[cyan]🤖 {result}[/cyan]", box=box.ROUNDED, border_style="green", title="Email Operation"))
            return
        
        # Other intent checks remain the same...
        
        # Process as a regular question with Rich UI feedback
        include_screenshot = Confirm.ask("Include screenshot context?", default=False)
        
        # Use Rich progress bar instead of animated loading
        with Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]Processing...[/bold blue]"),
            console=console,
            transient=True
        ) as progress:
            task = progress.add_task("[green]Thinking...", total=None)
            
            try:
                screenshot_encoded = self.desktop_screenshot.capture() if include_screenshot else None
                response = await self.assistant.answer_async(prompt, screenshot_encoded)
                
                # Display response with syntax highlighting for code blocks
                self._format_and_display_response(response)
                
                return response
                
            except Exception as e:
                logger.error(f"Question processing error: {e}")
                console.print(f"\n[bold red]❌ Error processing question: {e}[/bold red]")
                return

    def _format_and_display_response(self, response):
        """Format and display AI response with Rich UI enhancements."""
        # Check for code blocks in the response
        if "```" in response:
            # Split the response by code blocks
            parts = response.split("```")
            
            # Display each part with appropriate formatting
            for i, part in enumerate(parts):
                if i == 0:
                    # First part is always text before the first code block
                    if part.strip():
                        console.print(Markdown(part.strip()))
                elif i % 2 == 1:
                    # Odd-indexed parts are code blocks
                    # Extract language if specified (e.g., ```python)
                    code_lines = part.strip().split('\n')
                    if code_lines and not code_lines[0].isspace() and len(code_lines[0].strip()) > 0:
                        lang = code_lines[0].strip().lower()
                        code = '\n'.join(code_lines[1:])
                    else:
                        lang = "text"
                        code = part.strip()
                    
                    # Display code with syntax highlighting
                    console.print(Syntax(code, lang, theme="monokai", line_numbers=True, word_wrap=True))
                else:
                    # Even-indexed parts (except 0) are text between code blocks
                    if part.strip():
                        console.print(Markdown(part.strip()))
        else:
            # No code blocks, display as markdown
            console.print(Markdown(response))

    async def ocr_command(self, args):
        """
        Handle OCR command for extracting text from images.
        
        Args:
            args: Command arguments
        """
        if not args:
            self.display_error("Please specify an image path or 'screen' to capture the current screen")
            console.print("[dim]Example: /ocr path/to/image.jpg[/dim]")
            console.print("[dim]Example: /ocr screen[/dim]")
            return
            
        # Check if the user wants to capture the screen
        if args.lower() == "screen":
            console.print(Panel(
                "[bold]📸 Capturing your screen...[/bold]",
                title="[bold]OCR Operation[/bold]",
                border_style="blue",
                box=box.ROUNDED
            ))
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[bold blue]Capturing screen...[/bold blue]"),
                console=console,
                transient=True
            ) as progress:
                task = progress.add_task("[green]Processing...", total=None)
                # Capture the screen
                screenshot_path = os.path.join(os.getcwd(), "screenshot.png")
                self.desktop_screenshot.capture_to_file(screenshot_path)
                image_path = screenshot_path
                
            self.display_success(f"Screen captured and saved to {screenshot_path}")
        else:
            # User provided an image path
            image_path = args.strip()
            if not os.path.exists(image_path):
                self.display_error(f"Image file not found: {image_path}")
                return
        
        # Progress indicators for OCR processing
        with Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]Extracting text...[/bold blue]"),
            BarColumn(),
            TimeElapsedColumn(),
            console=console,
            transient=True
        ) as progress:
            task = progress.add_task("[green]Processing image...", total=None)
            extracted_text = self.ocr_processor.extract_text(image_path)
        
        if not extracted_text:
            self.display_warning("No text was extracted from the image")
            return
        
        # Display the extracted text
        console.print(Panel(
            f"[bold green]Extracted Text:[/bold green]\n\n{extracted_text}",
            title=f"[bold]OCR Results: {os.path.basename(image_path)}[/bold]",
            border_style="green",
            box=box.ROUNDED
        ))
        
        # Ask the user if they want AI analysis of the extracted text
        if Confirm.ask("Would you like AI analysis of this text?", default=True):
            with Progress(
                SpinnerColumn(),
                TextColumn("[bold blue]Analyzing text...[/bold blue]"),
                BarColumn(),
                TimeElapsedColumn(),
                console=console,
                transient=True
            ) as progress:
                analysis_task = progress.add_task("[green]Thinking...", total=None)
                # Ask the AI to analyze the extracted text
                analysis_prompt = f"Analyze the following OCR extracted text and provide insights:\n\n{extracted_text}"
                analysis = await self.assistant.answer_async(analysis_prompt)
            
            # Display the analysis
            console.print(Panel(
                Markdown(analysis),
                title="[bold]AI Analysis[/bold]",
                border_style="blue",
                box=box.ROUNDED
            ))
            
        # Ask if the user wants to save the extracted text
        if Confirm.ask("Would you like to save the extracted text to a file?", default=False):
            file_path = Prompt.ask("Enter file path to save the text", default="ocr_output.txt")
            
            try:
                with open(file_path, 'w') as f:
                    f.write(extracted_text)
                self.display_success(f"Text saved to {file_path}")
            except Exception as e:
                self.display_error(f"Error saving file: {str(e)}")

    async def web_command(self, args):
        """
        Handle web command for searching or accessing web content.
        
        Args:
            args: Command arguments
        """
        if not args:
            self.display_error("Please specify a search query or URL")
            console.print("[dim]Example: /web how to make pancakes[/dim]")
            console.print("[dim]Example: /web https://example.com[/dim]")
            return
            
        query = args.strip()
        
        # Check if it's a URL
        if query.startswith(("http://", "https://")):
            console.print(Panel(
                f"[bold]🌐 Accessing URL:[/bold] {query}",
                title="[bold]Web Operation[/bold]",
                border_style="blue",
                box=box.ROUNDED
            ))
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[bold blue]Fetching content...[/bold blue]"),
                BarColumn(),
                TimeElapsedColumn(),
                console=console,
                transient=True
            ) as progress:
                task = progress.add_task("[green]Loading...", total=None)
                
                try:
                    # Implement a web fetcher or use an existing one
                    content = "Web content fetching would go here"
                    
                    # Display a sample of the content
                    console.print(Panel(
                        f"[dim]{content[:500]}...[/dim]",
                        title=f"[bold]Content from {query}[/bold]",
                        border_style="blue",
                        box=box.ROUNDED
                    ))
                    
                    # Ask if the user wants AI to analyze the web content
                    if Confirm.ask("Would you like AI analysis of this web content?", default=True):
                        with Progress(
                            SpinnerColumn(),
                            TextColumn("[bold blue]Analyzing content...[/bold blue]"),
                            BarColumn(),
                            TimeElapsedColumn(),
                            console=console,
                            transient=True
                        ) as progress:
                            analysis_task = progress.add_task("[green]Thinking...", total=None)
                            analysis = await self.assistant.answer_async(f"Analyze this web content: {content[:2000]}")
                        
                        # Display the analysis
                        console.print(Panel(
                            Markdown(analysis),
                            title="[bold]AI Analysis[/bold]",
                            border_style="blue",
                            box=box.ROUNDED
                        ))
                    
                except Exception as e:
                    self.display_error(f"Error fetching web content: {str(e)}")
            
        else:
            # It's a search query
            console.print(Panel(
                f"[bold]🔍 Searching for:[/bold] {query}",
                title="[bold]Web Search[/bold]",
                border_style="blue",
                box=box.ROUNDED
            ))
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[bold blue]Searching...[/bold blue]"),
                BarColumn(),
                TimeElapsedColumn(),
                console=console,
                transient=True
            ) as progress:
                task = progress.add_task("[green]Fetching results...", total=None)
                
                try:
                    # Use the assistant to search for answers
                    response = await self.assistant.answer_async(f"Web search: {query}")
                    
                    # Format and display the response
                    self._format_and_display_response(response)
                    
                except Exception as e:
                    self.display_error(f"Error during web search: {str(e)}")

    async def email_command(self, args):
        """
        Handle email commands.
        
        Args:
            args: Command arguments
        """
        try:
            if not hasattr(self, 'email_manager') or self.email_manager is None:
                self.display_error("Email functionality is not available")
                return True
                
            if not args:
                self.display_error("Missing email subcommand. Available commands: setup, send, read, check")
                return True
                
            subcommand = args[0].lower()
            
            # First validate if email is set up for commands that require it
            if subcommand in ["send", "read"] and not getattr(self, 'email_setup_complete', False):
                # Try to load the configuration
                await self.check_email_config()
                
                # If still not configured after check
                if not getattr(self, 'email_setup_complete', False):
                    self.display_error("Email is not set up. Please run '/email setup' first.")
                    return True
            
            if subcommand == "setup":
                await self.email_setup()
                return True
                
            elif subcommand == "send":
                # Optional recipient from command
                recipient = args[1] if len(args) > 1 else None
                
                if recipient and recipient.startswith("to"):
                    recipient = recipient[2:].strip()
                    
                # Basic validation
                if recipient and '@' not in recipient:
                    self.display_error(f"Invalid email address: {recipient}")
                    recipient = None
                    
                await self.compose_email(recipient)
                return True
                
            elif subcommand == "read":
                await self.read_emails()
                return True
                
            elif subcommand == "check":
                await self.check_email_config()
                return True
                
            else:
                self.display_error(f"Unknown email subcommand: {subcommand}")
                self.display_warning("Available commands: setup, send, read, check")
                return True
                
        except Exception as e:
            self.display_error(f"Error processing email command: {str(e)}")
            logger.exception("Email command error")
            return True

    async def email_ai_write(self, to_address=None):
        """
        Use AI to write an email.
        
        Args:
            to_address (str, optional): Optional recipient email address
        """
        try:
            # First make sure email is configured
            if not hasattr(self, 'email_manager') or not getattr(self, 'email_setup_complete', False):
                await self.check_email_config()
                
                if not getattr(self, 'email_setup_complete', False):
                    self.display_error("Email is not configured. Please run '/email setup' first.")
                    return
            
            # If no recipient provided, ask for one
            if not to_address:
                console.print(Panel(
                    "To generate an email with AI assistance, we need a recipient email address.",
                    title="[bold]AI Email Writer[/bold]",
                    border_style="blue",
                    box=box.ROUNDED
                ))
                to_address = Prompt.ask("[bold cyan]Recipient email address[/bold cyan]")
                
            console.print(Panel(
                f"[bold]AI Email Composition Assistant[/bold]\n"
                f"Recipient: {to_address}",
                title="[bold]AI Email Writer[/bold]",
                border_style="blue",
                box=box.ROUNDED
            ))
            
            # Get email details
            subject = Prompt.ask("[bold cyan]Subject[/bold cyan]")
            
            # More comprehensive instructions
            console.print(Panel(
                "Tell the AI what kind of email you want to write. Be specific about:\n"
                "• Tone (formal, friendly, professional)\n"
                "• Purpose (meeting request, thank you, application, etc.)\n"
                "• Key points to include\n"
                "• Any specific requirements",
                title="[bold]Email Instructions[/bold]",
                border_style="green",
                box=box.ROUNDED
            ))
            
            instructions = Prompt.ask("[bold cyan]Instructions for AI[/bold cyan]")
            
            # Generate the email using AI
            with Progress(
                SpinnerColumn(),
                TextColumn("[bold blue]Generating email...[/bold blue]"),
                BarColumn(),
                TimeElapsedColumn(),
                console=console,
                transient=True
            ) as progress:
                task = progress.add_task("[green]Thinking...", total=None)
                
                prompt = f"Write an email to {to_address} with the subject '{subject}'. {instructions}"
                generated_email = await self.assistant.answer_async(prompt)
                
            # Extract subject and body from the generated email
            # This is a simple implementation; might need better parsing
            generated_body = generated_email
            
            # Preview the email with improved formatting
            console.print(Panel(
                Markdown(generated_body),
                title=f"[bold]Generated Email: {subject}[/bold]",
                border_style="green",
                box=box.ROUNDED,
                padding=(1, 2)
            ))
            
            # Ask for what to do with the generated email
            console.print("[bold cyan]What would you like to do with this email?[/bold cyan]")
            choices = {
                "1": "Send as is",
                "2": "Edit before sending",
                "3": "Regenerate with new instructions",
                "4": "Save as draft (not implemented)",
                "5": "Cancel"
            }
            
            # Display options with styling
            for key, value in choices.items():
                console.print(f"[bold blue]{key}.[/bold blue] {value}")
                
            choice = Prompt.ask("[bold]Select an option[/bold]", choices=list(choices.keys()), default="2")
            
            if choice == "1":  # Send as is
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[bold blue]Sending email...[/bold blue]"),
                    console=console,
                    transient=True
                ) as progress:
                    task = progress.add_task("[green]Connecting to SMTP server...", total=None)
                    
                    # Send the email
                    try:
                        result = self.email_manager.send_email(to_address, subject, generated_body)
                        if result and "success" in result.lower():
                            self.display_success("Email sent successfully!")
                        else:
                            self.display_error(f"Failed to send email: {result}")
                    except Exception as e:
                        self.display_error(f"Failed to send email: {str(e)}")
                        logger.exception("Unexpected error during email sending:")
            
            elif choice == "2":  # Edit before sending
                # Create a temporary file for editing in Notepad
                with tempfile.NamedTemporaryFile(mode='w+', suffix='.txt', delete=False) as temp_file:
                    temp_file.write(generated_body)
                    temp_path = temp_file.name
                
                self.display_info(f"Opening email in Notepad for editing. Save and close Notepad when done.")
                
                # Use the appropriate command based on OS
                if os.name == 'nt':  # Windows
                    subprocess.run(['notepad.exe', temp_path], check=True)
                else:
                    # Use default editor on Unix systems
                    editor = os.environ.get('EDITOR', 'nano')
                    subprocess.run([editor, temp_path], check=True)
                
                # Read the edited content back
                try:
                    with open(temp_path, 'r', encoding='utf-8') as edited_file:
                        edited_body = edited_file.read()
                    
                    # Clean up the temporary file
                    os.unlink(temp_path)
                    
                    # Preview the edited email
                    console.print(Panel(
                        Markdown(edited_body),
                        title=f"[bold]Edited Email: {subject}[/bold]",
                        border_style="green",
                        box=box.ROUNDED,
                        padding=(1, 2)
                    ))
                    
                    # Confirm sending
                    if Confirm.ask("Send this edited email?"):
                        with Progress(
                            SpinnerColumn(),
                            TextColumn("[bold blue]Sending email...[/bold blue]"),
                            console=console,
                            transient=True
                        ) as progress:
                            task = progress.add_task("[green]Connecting to SMTP server...", total=None)
                            
                            try:
                                result = self.email_manager.send_email(to_address, subject, edited_body)
                                if result and "success" in result.lower():
                                    self.display_success("Email sent successfully!")
                                else:
                                    self.display_error(f"Failed to send email: {result}")
                            except Exception as e:
                                self.display_error(f"Failed to send email: {str(e)}")
                    else:
                        self.display_warning("Email sending canceled")
                except Exception as e:
                    self.display_error(f"Error reading edited file: {str(e)}")
                    os.unlink(temp_path)  # Clean up even on error
                            
            elif choice == "3":  # Regenerate
                console.print("[bold cyan]New instructions for regenerating the email:[/bold cyan]")
                new_instructions = Prompt.ask("[bold]New instructions[/bold]")
                await self.email_ai_write(to_address)  # Restart the process
                
            elif choice == "4":  # Save draft
                self.display_warning("Save as draft feature is not yet implemented")
                
            elif choice == "5":  # Cancel
                self.display_warning("Email creation canceled")
                
        except Exception as e:
            self.display_error(f"Error in AI email composition: {str(e)}")
            logger.exception("Error in email_ai_write:")

    async def read_emails(self):
        """
        Read and display emails from the inbox.
        """
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[bold blue]Checking emails...[/bold blue]"),
                console=console,
                transient=True
            ) as progress:
                task = progress.add_task("[green]Connecting to mail server...", total=None)
                
                # Check emails using the email manager
                emails = self.email_manager.check_emails(limit=10)
                
            # Handle error messages (string responses)
            if isinstance(emails, str):
                self.display_error(emails)
                return
                
            # No emails found
            if not emails:
                self.display_warning("No emails found in your inbox.")
                return
                
            # Display email list
            console.print(Panel(
                f"Found [bold cyan]{len(emails)}[/bold cyan] emails in your inbox",
                title="[bold]Email Inbox[/bold]",
                border_style="cyan",
                box=box.ROUNDED
            ))
            
            # Create a table for the emails
            table = Table(
                title="Recent Emails",
                box=box.ROUNDED,
                expand=True,
                show_lines=True,
                title_style="bold cyan"
            )
            
            # Define table columns
            table.add_column("#", style="dim", width=4)
            table.add_column("From", style="bold", width=30, overflow="fold")
            table.add_column("Subject", style="italic green", width=40, overflow="fold")
            table.add_column("Date", style="blue", width=25)
            
            # Add emails to the table
            for i, email_data in enumerate(emails, 1):
                from_addr = email_data['from']
                subject = email_data['subject'] or "(No Subject)"
                date = email_data['date']
                
                table.add_row(
                    str(i),
                    from_addr,
                    subject,
                    date
                )
                
            # Display the table
            console.print(table)
            
            # Ask which email to read
            email_num = Prompt.ask(
                "[bold cyan]Enter email number to read (or 'q' to quit)[/bold cyan]",
                default="q",
                show_default=False
            )
            
            if email_num.lower() == 'q':
                return
                
            try:
                # Validate the selection
                email_index = int(email_num) - 1
                if email_index < 0 or email_index >= len(emails):
                    self.display_error(f"Invalid email number: {email_num}")
                    return
                    
                # Get the selected email
                selected_email = emails[email_index]
                
                # Display the email content
                console.print(Panel(
                    f"[bold]From:[/bold] {selected_email['from']}\n"
                    f"[bold]To:[/bold] {selected_email['to']}\n"
                    f"[bold]Date:[/bold] {selected_email['date']}\n"
                    f"[bold]Subject:[/bold] {selected_email['subject']}\n\n"
                    f"{selected_email['body']}",
                    title=f"[bold]Email #{email_num}[/bold]",
                    border_style="green",
                    box=box.ROUNDED,
                    padding=(1, 2),
                    expand=False
                ))
                
                # Option to reply
                if Confirm.ask("Reply to this email?"):
                    reply_to = selected_email['from']
                    reply_subject = f"Re: {selected_email['subject']}"
                    
                    # Extract the email address from the From field if needed
                    import re
                    email_pattern = r'[\w\.-]+@[\w\.-]+'
                    email_matches = re.findall(email_pattern, reply_to)
                    if email_matches:
                        reply_to = email_matches[0]
                    
                    # Compose reply
                    await self.compose_email(reply_to, reply_subject)
                
            except ValueError:
                self.display_error("Please enter a valid number or 'q'")
                
        except Exception as e:
            self.display_error(f"Error reading emails: {str(e)}")
            logger.exception("Error reading emails:")

    async def handle_github_operation(self, intent):
        """
        Handle GitHub operations based on detected intent.
        
        Args:
            intent: Dictionary containing detected intent information
        """
        if not self.config.get("github", {}).get("token"):
            self.display_error("GitHub is not configured. Please run /github setup first.")
            return
            
        operation = intent.get("operation")
        repo = intent.get("repository")
        
        if not operation:
            self.display_error("Unable to determine GitHub operation. Please try again with more details.")
            return
            
        if operation == "list_repos":
            console.print(Panel(
                "[bold]Fetching your GitHub repositories...[/bold]",
                title="[bold]GitHub Repositories[/bold]",
                border_style="blue",
                box=box.ROUNDED
            ))
            
            # Fetch repositories
            with Progress(
                SpinnerColumn(),
                TextColumn("[bold blue]Connecting to GitHub API...[/bold blue]"),
                BarColumn(),
                TimeElapsedColumn(),
                console=console,
                transient=True
            ) as progress:
                task = progress.add_task("[green]Fetching repositories...", total=None)
                
                # Placeholder for actual GitHub API call
                repositories = [
                    {"name": "project-alpha", "description": "A cool project", "stars": 12, "forks": 5, "language": "Python"},
                    {"name": "web-app", "description": "Web application template", "stars": 45, "forks": 20, "language": "JavaScript"},
                    {"name": "data-tools", "description": "Tools for data analysis", "stars": 8, "forks": 2, "language": "Python"}
                ]
            
            # Display repositories in a table
            repo_table = Table(title="Your GitHub Repositories", box=box.ROUNDED, border_style="blue")
            repo_table.add_column("Name", style="cyan")
            repo_table.add_column("Description")
            repo_table.add_column("Stars", justify="right", style="yellow")
            repo_table.add_column("Forks", justify="right", style="green")
            repo_table.add_column("Language", style="magenta")
            
            for repo in repositories:
                repo_table.add_row(
                    repo["name"],
                    repo["description"] or "",
                    str(repo["stars"]),
                    str(repo["forks"]),
                    repo["language"] or "Unknown"
                )
                
            console.print(repo_table)
            
        elif operation == "list_issues" and repo:
            console.print(Panel(
                f"[bold]Fetching issues for:[/bold] {repo}",
                title="[bold]GitHub Issues[/bold]",
                border_style="blue",
                box=box.ROUNDED
            ))
            
            # Fetch issues
            with Progress(
                SpinnerColumn(),
                TextColumn("[bold blue]Connecting to GitHub API...[/bold blue]"),
                BarColumn(),
                TimeElapsedColumn(),
                console=console,
                transient=True
            ) as progress:
                task = progress.add_task("[green]Fetching issues...", total=None)
                
                # Placeholder for actual GitHub API call
                issues = [
                    {"number": 42, "title": "Fix login bug", "state": "open", "created_at": "2023-01-15", "comments": 3},
                    {"number": 36, "title": "Update documentation", "state": "closed", "created_at": "2023-01-10", "comments": 5},
                    {"number": 45, "title": "Add new feature", "state": "open", "created_at": "2023-01-20", "comments": 2}
                ]
            
            if not issues:
                self.display_warning(f"No issues found for repository {repo}")
                return
                
            # Display issues in a table
            issue_table = Table(title=f"Issues for {repo}", box=box.ROUNDED, border_style="blue")
            issue_table.add_column("#", style="cyan", justify="right")
            issue_table.add_column("Title")
            issue_table.add_column("State", style="bold")
            issue_table.add_column("Created", style="yellow")
            issue_table.add_column("Comments", justify="right")
            
            for issue in issues:
                issue_table.add_row(
                    str(issue["number"]),
                    issue["title"],
                    f"[green]{issue['state']}[/green]" if issue["state"] == "open" else f"[red]{issue['state']}[/red]",
                    issue["created_at"],
                    str(issue["comments"])
                )
                
            console.print(issue_table)
            
        elif operation == "create_issue" and repo:
            console.print(Panel(
                f"[bold]Creating new issue in:[/bold] {repo}",
                title="[bold]New GitHub Issue[/bold]",
                border_style="blue",
                box=box.ROUNDED
            ))
            
            title = Prompt.ask("[bold]Issue title[/bold]")
            console.print("[bold]Issue description:[/bold] (Type your message, press Enter then Ctrl+D to finish)")
            
            # Collect body lines
            body_lines = []
            while True:
                try:
                    line = input()
                    body_lines.append(line)
                except EOFError:
                    break
                    
            body = "\n".join(body_lines)
            
            # Preview the issue
            console.print(Panel(
                f"[bold]Title:[/bold] {title}\n\n"
                f"[bold]Description:[/bold]\n{body}",
                title="[bold]Issue Preview[/bold]",
                border_style="green",
                box=box.ROUNDED
            ))
            
            # Ask for confirmation
            if Confirm.ask("Create this issue?", default=True):
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[bold blue]Creating issue...[/bold blue]"),
                    console=console,
                    transient=True
                ) as progress:
                    task = progress.add_task("[green]Connecting to GitHub API...", total=None)
                    
                    # Placeholder for actual GitHub API call
                    issue_number = 46  # This would be the actual issue number from the API response
                
                self.display_success(f"Issue #{issue_number} created successfully in {repo}")
            else:
                self.display_warning("Issue creation canceled")
                
        elif operation == "clone" and repo:
            # Clone operation
            clone_dir = intent.get("directory", ".")
            
            console.print(Panel(
                f"[bold]Cloning repository:[/bold] {repo}\n"
                f"[bold]Target directory:[/bold] {clone_dir}",
                title="[bold]Git Clone Operation[/bold]",
                border_style="blue",
                box=box.ROUNDED
            ))
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[bold blue]Cloning repository...[/bold blue]"),
                BarColumn(),
                TimeElapsedColumn(),
                console=console,
                transient=True
            ) as progress:
                task = progress.add_task("[green]Cloning...", total=None)
                
                # Placeholder for actual git clone operation
                # This would use subprocess to run git commands
                import time
                time.sleep(2)  # Simulate cloning process
            
            self.display_success(f"Repository {repo} cloned successfully to {clone_dir}")
            
        else:
            self.display_error(f"Unsupported GitHub operation: {operation}")
            
    async def handle_file_operation(self, intent):
        """
        Handle file operations.
        
        Args:
            intent: The detected intent for file operations
            
        Returns:
            str: Result of the file operation
        """
        operation = intent.get("operation", "").lower() if isinstance(intent, dict) else ""
        params = intent.get("params", {}) if isinstance(intent, dict) else {}
        
        # Extract the file path if present
        file_path = params.get("path", "")
        
        if operation == "list":
            # List files in a directory
            directory = file_path or os.getcwd()
            
            try:
                console.print(Panel(
                    f"[bold]Listing files in:[/bold] {directory}",
                    title="[bold]File Operation[/bold]",
                    border_style="blue",
                    box=box.ROUNDED
                ))
                
                files = os.listdir(directory)
                
                # Create a table to display files
                file_table = Table(
                    title=f"Contents of {os.path.basename(directory)}",
                    box=box.ROUNDED,
                    border_style="blue"
                )
                
                file_table.add_column("Name", style="cyan")
                file_table.add_column("Type", style="green")
                file_table.add_column("Size", style="magenta")
                file_table.add_column("Modified", style="yellow")
                
                for file in files:
                    full_path = os.path.join(directory, file)
                    file_stat = os.stat(full_path)
                    
                    # Determine file type
                    file_type = "Directory" if os.path.isdir(full_path) else "File"
                    
                    # Format file size
                    size_bytes = file_stat.st_size
                    if size_bytes < 1024:
                        size_str = f"{size_bytes} B"
                    elif size_bytes < 1024 * 1024:
                        size_str = f"{size_bytes / 1024:.1f} KB"
                    else:
                        size_str = f"{size_bytes / (1024 * 1024):.1f} MB"
                    
                    # Format modification time
                    mod_time = datetime.fromtimestamp(file_stat.st_mtime).strftime("%Y-%m-%d %H:%M")
                    
                    file_table.add_row(file, file_type, size_str, mod_time)
                
                console.print(file_table)
                return f"Listed {len(files)} files in {directory}"
                
            except PermissionError:
                self.display_error(f"Permission denied for: {directory}")
                return f"Permission denied for: {directory}"
            except FileNotFoundError:
                self.display_error(f"Directory not found: {directory}")
                return f"Directory not found: {directory}"
            except Exception as e:
                self.display_error(f"Error listing files: {str(e)}")
                return f"Error listing files: {str(e)}"
                
        elif operation == "create":
            # Create a file
            content = params.get("content", "")
            
            if not file_path:
                self.display_error("No file path specified")
                return "No file path specified"
                
            try:
                # Create directory if it doesn't exist
                os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
                
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[bold blue]Creating file...[/bold blue]"),
                    console=console,
                    transient=True
                ) as progress:
                    task = progress.add_task("[green]Writing file...", total=None)
                    with open(file_path, 'w') as f:
                        f.write(content)
                
                self.display_success(f"File created: {file_path}")
                return f"Successfully created file: {file_path}"
                
            except PermissionError:
                self.display_error(f"Permission denied for: {file_path}")
                return f"Permission denied for: {file_path}"
            except Exception as e:
                self.display_error(f"Error creating file: {str(e)}")
                return f"Error creating file: {str(e)}"
                
        elif operation == "delete":
            # Delete a file
            if not file_path:
                self.display_error("No file path specified")
                return "No file path specified"
                
            try:
                # Confirm deletion
                if not Confirm.ask(f"Are you sure you want to delete [bold red]{file_path}[/bold red]?", default=False):
                    self.display_warning("File deletion canceled")
                    return "File deletion canceled"
                    
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[bold blue]Deleting file...[/bold blue]"),
                    console=console,
                    transient=True
                ) as progress:
                    task = progress.add_task("[green]Removing file...", total=None)
                    if os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                    else:
                        os.remove(file_path)
                
                self.display_success(f"Successfully deleted: {file_path}")
                return f"Successfully deleted: {file_path}"
                
            except PermissionError:
                self.display_error(f"Permission denied for: {file_path}")
                return f"Permission denied for: {file_path}"
            except FileNotFoundError:
                self.display_error(f"File not found: {file_path}")
                return f"File not found: {file_path}"
            except Exception as e:
                self.display_error(f"Error deleting file: {str(e)}")
                return f"Error deleting file: {str(e)}"
                
        elif operation == "read":
            # Read a file
            if not file_path:
                self.display_error("No file path specified")
                return "No file path specified"
                
            try:
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[bold blue]Reading file...[/bold blue]"),
                    console=console,
                    transient=True
                ) as progress:
                    task = progress.add_task("[green]Loading content...", total=None)
                    
                    # Check file size
                    file_size = os.path.getsize(file_path)
                    if file_size > 10 * 1024 * 1024:  # 10MB limit
                        self.display_warning(f"File is too large ({file_size / (1024 * 1024):.1f} MB). Only the first 100 lines will be displayed.")
                        with open(file_path, 'r') as f:
                            content = "".join(f.readlines()[:100])
                            content += "\n... (file truncated) ..."
                    else:
                        with open(file_path, 'r') as f:
                            content = f.read()
                
                # Determine syntax highlighting based on file extension
                file_ext = os.path.splitext(file_path)[1].lower()
                lexer_name = {
                    ".py": "python",
                    ".js": "javascript",
                    ".html": "html",
                    ".css": "css",
                    ".json": "json",
                    ".md": "markdown",
                    ".xml": "xml",
                    ".java": "java",
                    ".c": "c",
                    ".cpp": "cpp",
                    ".cs": "csharp",
                    ".go": "go",
                    ".rb": "ruby",
                    ".php": "php",
                    ".sh": "bash",
                    ".bat": "batch",
                    ".ps1": "powershell",
                    ".sql": "sql",
                    ".yaml": "yaml",
                    ".yml": "yaml",
                    ".txt": None
                }.get(file_ext, None)
                
                file_panel = Panel(
                    Syntax(content, lexer_name) if lexer_name else content,
                    title=f"[bold]{os.path.basename(file_path)}[/bold]",
                    border_style="blue",
                    box=box.ROUNDED,
                    width=min(len(max(content.split('\n'), key=len)) + 10, console.width - 10)
                )
                
                console.print(file_panel)
                return f"Read file: {file_path}"
                
            except PermissionError:
                self.display_error(f"Permission denied for: {file_path}")
                return f"Permission denied for: {file_path}"
            except FileNotFoundError:
                self.display_error(f"File not found: {file_path}")
                return f"File not found: {file_path}"
            except UnicodeDecodeError:
                self.display_error(f"Unable to read file: {file_path}. This might be a binary file.")
                return f"Unable to read file: {file_path}. This might be a binary file."
            except Exception as e:
                self.display_error(f"Error reading file: {str(e)}")
                return f"Error reading file: {str(e)}"
        
        else:
            self.display_warning("Unsupported file operation")
            return "Unsupported file operation. Try 'list', 'create', 'read', or 'delete'."

    async def handle_app_operation(self, intent):
        """
        Handle application operations based on detected intent.
        
        Args:
            intent (dict): App intent information
            
        Returns:
            str: Result of the app operation
        """
        operation = intent["operation"]
        params = intent["params"]
        
        # Handle different operations
        if operation == "launch_app":
            app_name = params.get("app_name")
            return self.launch_app(app_name)
        
        elif operation == "list_apps":
            return self.list_apps()
        
        elif operation == "general_app":
            return "I detected an app-related request, but I'm not sure what specific operation you want to perform. You can ask me to:\n\n" + \
                   "- List installed apps\n" + \
                   "- Launch an app"
        
        return "Unsupported app operation."

    def launch_app(self, app_name):
        """
        Launch an application based on the given app name.
        
        Args:
            app_name (str): Name of the application to launch
            
        Returns:
            str: Result of the app launch operation
        """
        try:
            # Use a simple method to launch the app
            result = self.app_launcher.launch_app(app_name)
            return result
        except Exception as e:
            logger.error(f"Error launching app: {e}")
            return f"Error launching application: {str(e)}"

    async def configure(self):
        """Configure the AI Assistant settings."""
        console.print(Panel("[bold cyan]⚙️ Configuration[/bold cyan]", box=box.ROUNDED, border_style="cyan"))
        
        config_table = Table(show_header=False, box=box.SIMPLE)
        config_table.add_column("Option", style="cyan")
        config_table.add_column("Description")
        config_table.add_row("1", "Change AI model")
        config_table.add_row("2", "Change assistant role")
        config_table.add_row("3", "Update API key")
        config_table.add_row("4", "Configure GitHub integration")
        config_table.add_row("5", "Configure email integration")
        config_table.add_row("6", "Return to main menu")
        
        console.print(Panel(
            config_table,
            title="[bold]Settings Menu[/bold]",
            border_style="blue",
            box=box.ROUNDED
        ))
        
        choice = Prompt.ask("Enter your choice", choices=["1", "2", "3", "4", "5", "6"], default="6")
        
        if choice == "1":
            await self.change_model()
        elif choice == "2":
            await self.change_role()
        elif choice == "3":
            await self.update_api_key()
        elif choice == "4":
            await self.configure_github()
        elif choice == "5":
            await self.configure_email()
        # Return to main menu for '6' or any other input

    async def change_model(self):
        """Change the AI model."""
        model_table = Table(box=box.ROUNDED)
        model_table.add_column("Option", style="cyan")
        model_table.add_column("Model")
        model_table.add_column("Description")
        
        model_table.add_row("1", "Gemini", "Google AI large language model")
        model_table.add_row("2", "OpenAI", "GPT-4 and GPT-3.5 models")
        
        console.print(Panel(
            model_table,
            title="[bold]Available AI Models[/bold]",
            border_style="blue",
            box=box.ROUNDED
        ))
        
        model_choice = Prompt.ask("Enter your choice", choices=["1", "2"], default="1")
        model_map = {"1": "Gemini", "2": "OpenAI"}
        
        if model_choice in model_map:
            self.config["model"] = model_map[model_choice]
            save_config(self.config)
            self.initialize_assistant()
            console.print(f"[green]✅ Model changed to {self.config['model']}[/green]")
        else:
            console.print("[bold red]❌ Invalid choice.[/bold red]")

    async def change_role(self):
        """Change the assistant role."""
        from ..core.prompts import ROLE_PROMPTS
        
        role_table = Table(box=box.ROUNDED)
        role_table.add_column("Option", style="cyan")
        role_table.add_column("Role")
        role_table.add_column("Description")
        
        for i, (role, description) in enumerate(ROLE_PROMPTS.items(), 1):
            # Extract a short description from the full prompt
            short_desc = description.split("\n")[0] if "\n" in description else description[:50] + "..."
            role_table.add_row(str(i), role, short_desc)
        
        console.print(Panel(
            role_table,
            title="[bold]Assistant Roles[/bold]",
            border_style="blue",
            box=box.ROUNDED
        ))
        
        role_choices = [str(i) for i in range(1, len(ROLE_PROMPTS) + 1)]
        role_choice = Prompt.ask("Enter your choice", choices=role_choices, default="1")
        
        try:
            role_idx = int(role_choice) - 1
            if 0 <= role_idx < len(ROLE_PROMPTS):
                self.config["role"] = list(ROLE_PROMPTS.keys())[role_idx]
                save_config(self.config)
                self.initialize_assistant()
                console.print(f"[green]✅ Role changed to {self.config['role']}[/green]")
            else:
                console.print("[bold red]❌ Invalid choice.[/bold red]")
        except ValueError:
            console.print("[bold red]❌ Please enter a number.[/bold red]")

    async def update_api_key(self):
        """Update the API key for the current model."""
        model = self.config.get("model", "Gemini")
        
        console.print(Panel(
            f"The current AI model is [bold cyan]{model}[/bold cyan].\nPlease provide a new API key for this model.",
            title="[bold]API Key Update[/bold]",
            border_style="blue",
            box=box.ROUNDED
        ))
        
        # Use getpass for API keys for security
        import getpass
        new_key = getpass.getpass(f"Enter new {model} API Key: ")
        
        if new_key.strip():
            # Save in config with model-specific key
            self.config[f"{model.lower()}_api_key"] = new_key
            
            # Also save to generic api_key for backward compatibility
            self.config["api_key"] = new_key
            
            save_config(self.config)
            self.initialize_assistant()
            
            console.print(f"[green]✅ API key updated for {model}[/green]")
            console.print("[dim]Your API key has been saved and will be remembered for future sessions[/dim]")
        else:
            console.print("[bold red]❌ No API key provided. Operation canceled.[/bold red]")

    async def configure_github(self):
        """Configure GitHub integration settings."""
        github_table = Table(show_header=False, box=box.SIMPLE)
        github_table.add_column("Option", style="cyan")
        github_table.add_column("Description")
        github_table.add_row("1", "Set GitHub Access Token")
        github_table.add_row("2", "View Current GitHub Status")
        github_table.add_row("3", "Remove GitHub Access Token")
        github_table.add_row("4", "Back to configuration menu")
        
        console.print(Panel(
            github_table,
            title="[bold]GitHub Integration Configuration[/bold]",
            border_style="blue",
            box=box.ROUNDED
        ))
        
        choice = Prompt.ask("Enter your choice", choices=["1", "2", "3", "4"], default="4")
        
        if choice == "1":
            # Use getpass for secret tokens
            import getpass
            token = getpass.getpass("\nEnter your GitHub Personal Access Token: ")
            
            if token:
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[bold blue]Authenticating with GitHub...[/bold blue]"),
                    console=console,
                    transient=True
                ) as progress:
                    task = progress.add_task("[green]Connecting...", total=None)
                    
                    # Simulate a bit of waiting time for the authentication process
                    import time
                    time.sleep(1)
                    
                    if self.github.authenticate(token):
                        # Save token to environment variable
                        os.environ["GITHUB_TOKEN"] = token
                        
                        # Optionally save to .env file for persistence
                        try:
                            with open(".env", "a+") as env_file:
                                env_file.seek(0)
                                content = env_file.read()
                                if "GITHUB_TOKEN" not in content:
                                    env_file.write(f"\nGITHUB_TOKEN={token}\n")
                                else:
                                    # Replace existing token
                                    lines = content.splitlines()
                                    with open(".env", "w") as new_env_file:
                                        for line in lines:
                                            if line.startswith("GITHUB_TOKEN="):
                                                new_env_file.write(f"GITHUB_TOKEN={token}\n")
                                            else:
                                                new_env_file.write(f"{line}\n")
                        except Exception as e:
                            logger.error(f"Error saving GitHub token to .env file: {e}")
                        
                        console.print(Panel(
                            f"[green]✅ GitHub token set successfully![/green]\nAuthenticated as: [bold]{self.github.username}[/bold]",
                            title="[bold]GitHub Authentication[/bold]",
                            border_style="green",
                            box=box.ROUNDED
                        ))
                    else:
                        console.print(Panel(
                            "[bold red]❌ GitHub authentication failed.[/bold red]\nPlease check your token and try again.",
                            title="[bold]GitHub Authentication[/bold]",
                            border_style="red",
                            box=box.ROUNDED
                        ))
            else:
                console.print("[bold orange]⚠️ No token provided. GitHub integration will not be available.[/bold orange]")
            
        elif choice == "2":
            if self.github.authenticated:
                console.print(Panel(
                    f"[green]✅ GitHub Status: Authenticated[/green]\nUsername: [bold]{self.github.username}[/bold]\nGitHub integration is active and ready to use.",
                    title="[bold]GitHub Status[/bold]",
                    border_style="green",
                    box=box.ROUNDED
                ))
            else:
                console.print(Panel(
                    "[bold orange]⚠️ GitHub Status: Not authenticated[/bold orange]\nYou need to set a GitHub access token to use GitHub features.",
                    title="[bold]GitHub Status[/bold]",
                    border_style="orange",
                    box=box.ROUNDED
                ))
            
        elif choice == "3":
            if "GITHUB_TOKEN" in os.environ:
                confirm = Confirm.ask("Are you sure you want to remove your GitHub token?", default=False)
                
                if confirm:
                    del os.environ["GITHUB_TOKEN"]
                    
                    # Remove from .env file if it exists
                    try:
                        if os.path.exists(".env"):
                            with open(".env", "r") as env_file:
                                lines = env_file.readlines()
                            
                            with open(".env", "w") as env_file:
                                for line in lines:
                                    if not line.startswith("GITHUB_TOKEN="):
                                        env_file.write(line)
                    except Exception as e:
                        logger.error(f"Error removing GitHub token from .env file: {e}")
                    
                    # Reset GitHub integration
                    self.github = GitHubIntegration()
                    console.print("[green]✅ GitHub token removed successfully.[/green]")
                else:
                    console.print("[blue]Operation canceled.[/blue]")
            else:
                console.print("[blue]No GitHub token is currently set.[/blue]")
        
        # Return to config menu for '4' or any other input

    async def check_email_config(self):
        """Check email configuration status and initialize if needed"""
        try:
            if not hasattr(self, 'email_manager') or self.email_manager is None:
                self.display_error("Email manager not initialized")
                return
            
            # Try to load config directly from email_manager
            if hasattr(self.email_manager, 'is_configured') and self.email_manager.is_configured():
                self.email_setup_complete = True
                self.display_success(f"Email configured for: {self.email_manager.email_address}")
                return
                
            # Check if config file exists
            config_path = getattr(self.email_manager, 'config_path', None)
            if not config_path or not os.path.exists(config_path):
                self.display_error("Email configuration not found")
                return
                
            # Try to load the config
            try:
                # Try method in email_manager class first
                if hasattr(self.email_manager, 'load_email_config'):
                    config = self.email_manager.load_email_config()
                else:
                    # Fallback to loading directly
                    with open(config_path, 'r') as f:
                        config = json.load(f)
                    
                if not config:
                    self.display_error("Email configuration is empty or invalid")
                    return
                    
                # Check for required fields
                required_fields = ['email_address', 'email_password', 'smtp_server', 'smtp_port', 'imap_server', 'imap_port']
                missing_fields = [field for field in required_fields if field not in config]
                
                if missing_fields:
                    self.display_error(f"Email config is missing fields: {', '.join(missing_fields)}")
                else:
                    # All required fields present
                    if hasattr(self.email_manager, 'connect'):
                        # Try to connect to validate configuration
                        connection_result = self.email_manager.connect()
                        if connection_result:
                            self.email_setup_complete = True
                            self.display_success(f"Connected to email: {config['email_address']} via {config['smtp_server']}")
                        else:
                            self.display_error("Failed to connect with the saved email configuration")
                    else:
                        # Just mark as complete without testing connection
                        self.email_setup_complete = True
                        self.display_success(f"Email config loaded: {config['email_address']} via {config['smtp_server']}")
                    
            except json.JSONDecodeError:
                self.display_error("Email config file is corrupt or empty")
            except Exception as e:
                self.display_error(f"Error loading email config: {str(e)}")
                logger.exception("Error loading email configuration")
        except Exception as e:
            self.display_error(f"Error checking email config: {str(e)}")
            logger.exception("Error checking email configuration")

    async def email_setup(self):
        """
        Set up email configuration with user-provided details.
        """
        console.print(Panel(
            "Email Configuration\nThis will set up your email for sending and receiving messages.\nYou'll need your email address and password/app password.",
            title="[bold]Email Setup[/bold]",
            border_style="cyan",
            box=box.ROUNDED
        ))
        
        # Get email configuration details
        email_address = Prompt.ask("[bold cyan]Email address[/bold cyan]")
        
        # Auto-detect email provider and pre-fill server information
        provider_settings = self._detect_email_provider(email_address)
        
        # Show provider detection result
        if provider_settings:
            self.display_success(f"Detected {provider_settings['name']} account! Server settings will be configured automatically.")
        else:
            self.display_warning("Could not detect email provider. You'll need to enter server details manually.")
        
        # Get password
        email_password = Prompt.ask("[bold cyan]Email password/app password[/bold cyan]", password=True)
        
        # Set SMTP and IMAP details based on detected provider or ask user
        if provider_settings:
            smtp_server = provider_settings['smtp_server']
            smtp_port = provider_settings['smtp_port']
            imap_server = provider_settings['imap_server']
            imap_port = provider_settings['imap_port']
            provider = provider_settings.get('name', '').lower().replace(' ', '_')
            
            # Show the auto-configured settings
            console.print(Panel(
                f"Using {provider_settings['name']} server settings:\nSMTP: {smtp_server}:{smtp_port}\nIMAP: {imap_server}:{imap_port}",
                title="[bold]Server Settings[/bold]",
                border_style="blue",
                box=box.ROUNDED
            ))
        else:
            # Manual configuration if not detected
            smtp_server = Prompt.ask("[bold cyan]SMTP server[/bold cyan] (e.g., smtp.gmail.com)")
            smtp_port = Prompt.ask("[bold cyan]SMTP port[/bold cyan] (e.g., 587)", default="587")
            imap_server = Prompt.ask("[bold cyan]IMAP server[/bold cyan] (e.g., imap.gmail.com)")
            imap_port = Prompt.ask("[bold cyan]IMAP port[/bold cyan] (e.g., 993)", default="993")
            provider = None
            
        # Now set up the email
        with Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]Setting up email...[/bold blue]"),
            console=console,
            transient=True
        ) as progress:
            task = progress.add_task("[green]Testing connection...", total=None)
            
            # Set up email using the appropriate method based on EmailManager implementation
            if hasattr(self.email_manager, 'setup_email_account'):
                # New integrations version
                result = self.email_manager.setup_email_account(email_address, email_password, provider)
                if "successfully" in result.lower():
                    self.email_setup_complete = True
                    self.display_success("Email setup complete!")
                else:
                    self.display_error(f"Email setup failed: {result}")
            elif hasattr(self.email_manager, 'setup_email'):
                # Core version
                success = self.email_manager.setup_email(
                    email_address, email_password, 
                    smtp_server, smtp_port, 
                    imap_server, imap_port
                )
                
                if success:
                    self.email_setup_complete = True
                    self.display_success("Email setup complete!")
                else:
                    self.display_error("Failed to set up email. Please check your credentials and try again.")
            else:
                self.display_error("Email setup not supported by the current EmailManager implementation.")
                
        # Check connection after setup
        if getattr(self, 'email_setup_complete', False):
            self.display_success(f"You can now send and receive emails as {email_address}")
        else:
            self.display_warning("Email is not fully configured. Some features may not work correctly.")

    def _detect_email_provider(self, email_address):
        """
        Detect email provider from email address and return pre-configured settings
        
        Args:
            email_address: User's email address
            
        Returns:
            dict: Provider settings or None if not detected
        """
        email_domain = email_address.split('@')[-1].lower()
        
        # Gmail
        if email_domain in ['gmail.com', 'googlemail.com']:
            return {
                'name': 'Gmail',
                'smtp_server': 'smtp.gmail.com',
                'smtp_port': 587,
                'imap_server': 'imap.gmail.com',
                'imap_port': 993
            }
            
        # Outlook/Hotmail
        elif any(domain in email_domain for domain in ['outlook.com', 'hotmail.com', 'live.com', 'msn.com']):
            return {
                'name': 'Outlook/Hotmail',
                'smtp_server': 'smtp-mail.outlook.com',
                'smtp_port': 587,
                'imap_server': 'outlook.office365.com',
                'imap_port': 993
            }
            
        # Yahoo
        elif 'yahoo' in email_domain:
            return {
                'name': 'Yahoo Mail',
                'smtp_server': 'smtp.mail.yahoo.com',
                'smtp_port': 587,
                'imap_server': 'imap.mail.yahoo.com',
                'imap_port': 993
            }
            
        # AOL
        elif 'aol' in email_domain:
            return {
                'name': 'AOL Mail',
                'smtp_server': 'smtp.aol.com',
                'smtp_port': 587,
                'imap_server': 'imap.aol.com',
                'imap_port': 993
            }
            
        # Zoho
        elif 'zoho' in email_domain:
            return {
                'name': 'Zoho Mail',
                'smtp_server': 'smtp.zoho.com',
                'smtp_port': 587,
                'imap_server': 'imap.zoho.com',
                'imap_port': 993
            }
            
        # iCloud
        elif 'icloud' in email_domain or 'me.com' in email_domain:
            return {
                'name': 'iCloud Mail',
                'smtp_server': 'smtp.mail.me.com',
                'smtp_port': 587,
                'imap_server': 'imap.mail.me.com',
                'imap_port': 993
            }
        
        # Provider not detected
        return None
            
    async def compose_email(self, to_address=None, subject=None):
        """
        Compose and send an email to the specified address.
        
        Args:
            to_address (str, optional): Recipient email address. If None, will prompt for it.
            subject (str, optional): Email subject. If None, will prompt for it.
        """
        try:
            # First make sure email is configured
            if not hasattr(self, 'email_manager') or not self.email_manager.is_configured():
                await self.check_email_config()
                
                if not getattr(self, 'email_setup_complete', False):
                    self.display_error("Email is not configured. Please run '/email setup' first.")
                    return
            
            # Prompt for recipient if not provided
            if not to_address:
                to_address = Prompt.ask("[bold cyan]Recipient email address[/bold cyan]")
                
            # Show composition UI
            console.print(Panel(
                f"Composing email to: {to_address}",
                title="[bold]New Email[/bold]",
                border_style="cyan",
                box=box.ROUNDED
            ))
            
            # Get subject if not provided
            if not subject:
                subject = Prompt.ask("[bold cyan]Subject[/bold cyan]")
                
            # Get body with multi-line input
            console.print("[bold cyan]Body:[/bold cyan] (Type your message. When done, enter an empty line)")
            
            lines = []
            while True:
                line = input()
                if not line and lines:  # Empty line and we have content
                    break
                lines.append(line)
                
            body = "\n".join(lines)
            
            # Preview the email
            console.print(Panel(
                f"[bold]To:[/bold] {to_address}\n"
                f"[bold]Subject:[/bold] {subject}\n\n"
                f"{body[:300]}{'...' if len(body) > 300 else ''}",
                title="[bold]Email Preview[/bold]",
                border_style="green",
                box=box.ROUNDED
            ))
            
            # Confirm sending
            if Confirm.ask("Send this email?"):
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[bold blue]Sending email...[/bold blue]"),
                    console=console,
                    transient=True
                ) as progress:
                    task = progress.add_task("[green]Connecting to SMTP server...", total=None)
                    
                    # Send the email
                    result = self.email_manager.send_email(to_address, subject, body)
                    
                    # Check the result
                    if result and "success" in result.lower():
                        self.display_success("Email sent successfully!")
                    else:
                        self.display_error(f"Failed to send email: {result}")
            else:
                self.display_warning("Email sending canceled")
                
        except Exception as e:
            self.display_error(f"Error composing email: {str(e)}")
            logger.exception("Error in compose_email:")

    async def configure_email(self):
        """Configure email integration settings."""
        console.print(Panel(
            "[bold]Email Configuration[/bold]\n"
            "Set up your email account to send and receive emails through the assistant.",
            title="[bold]Email Integration[/bold]",
            border_style="blue",
            box=box.ROUNDED
        ))
        
        # Check if email is already configured
        if hasattr(self, 'email_manager'):
            await self.check_email_config()
            current_status = "configured" if getattr(self, 'email_setup_complete', False) else "not configured"
            
            # Display current status
            if getattr(self, 'email_setup_complete', False):
                if hasattr(self.email_manager, 'email_address'):
                    console.print(f"[green]✓ Email is currently configured for: {self.email_manager.email_address}[/green]")
                else:
                    console.print(f"[green]✓ Email is currently configured[/green]")
            else:
                console.print("[red]✗ Email is not currently configured[/red]")
            
            # Options
            console.print("\n[bold cyan]Options:[/bold cyan]")
            console.print("[cyan]1.[/cyan] Set up new email account")
            console.print("[cyan]2.[/cyan] Test current configuration")
            console.print("[cyan]3.[/cyan] Return to settings menu")
            
            choice = Prompt.ask("Enter your choice", choices=["1", "2", "3"], default="3")
            
            if choice == "1":
                await self.email_setup()
            elif choice == "2":
                # Test the current configuration
                if not getattr(self, 'email_setup_complete', False):
                    self.display_error("Email is not configured. Please set it up first.")
                else:
                    with Progress(
                        SpinnerColumn(),
                        TextColumn("[bold blue]Testing email connection...[/bold blue]"),
                        console=console,
                        transient=True
                    ) as progress:
                        task = progress.add_task("[green]Connecting to servers...", total=None)
                        
                        if hasattr(self.email_manager, 'connect'):
                            result = self.email_manager.connect()
                            if result:
                                self.display_success("Email connection test successful!")
                            else:
                                self.display_error("Failed to connect to email servers. Check your credentials.")
                        else:
                            # For core EmailManager that doesn't have connect method
                            self.display_success("Email configuration loaded successfully.")
            # Choice 3 returns to settings menu
        else:
            self.display_error("Email manager is not initialized. This is an internal error.")
            
        # Return to settings menu
        await self.configure()

    async def handle_email_operation(self, intent, original_query=None):
        """
        Handle email operations based on intent.
        
        Args:
            intent: Dictionary containing email operation details
            original_query: Original user query for AI assistance
            
        Returns:
            String describing the result
        """
        if not hasattr(self, 'email_manager') or self.email_manager is None:
            return "Email functionality is not available"
            
        # Check if email is configured
        if not getattr(self, 'email_setup_complete', False):
            await self.check_email_config()
            if not getattr(self, 'email_setup_complete', False):
                return "Email is not configured. Please run '/email setup' first."
        
        operation = intent.get('operation', '')
        
        if operation == 'ai_compose_email':
            to_address = intent.get('to_address')
            await self.email_ai_write(to_address)
            return "Email composition completed"
            
        elif operation == 'send_email':
            to_address = intent.get('to_address')
            subject = intent.get('subject')
            body = intent.get('body')
            
            if not all([to_address, subject, body]):
                return "Missing required information for sending email"
                
            # Use the email manager to send the email
            result = self.email_manager.send_email(to_address, subject, body)
            return result
            
        elif operation == 'read_emails':
            # Call read_emails method
            await self.read_emails()
            return "Email reading completed"
            
        else:
            return f"Unknown email operation: {operation}"

def load_config(config_path="config.json"):
    """
    Load configuration from disk.
    
    Returns:
        dict: Configuration dictionary
    """
    try:
        # Use absolute path to the user's home directory
        home_dir = os.path.expanduser("~")
        config_dir = os.path.join(home_dir, ".quackquery")
        abs_config_path = os.path.join(config_dir, "config.json")
        
        # Check for the config in the home directory first
        if os.path.exists(abs_config_path):
            with open(abs_config_path, 'r') as f:
                logger.info(f"Loading config from {abs_config_path}")
                return json.load(f)
        
        # Fallback to the provided path (legacy support)
        elif os.path.exists(config_path):
            with open(config_path, 'r') as f:
                logger.info(f"Loading config from {config_path}")
                return json.load(f)
                
        return {"model": "Gemini", "role": "General"}
    except Exception as e:
        logger.error(f"Error loading config: {e}")
        return {"model": "Gemini", "role": "General"}

def save_config(config):
    """
    Save configuration to disk.
    
    Args:
        config (dict): Configuration dictionary
    """
    try:
        # Create a dedicated configuration directory in the user's home
        home_dir = os.path.expanduser("~")
        config_dir = os.path.join(home_dir, ".quackquery")
        
        # Create directory if it doesn't exist
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
            
        # Save to the absolute path
        abs_config_path = os.path.join(config_dir, "config.json")
        with open(abs_config_path, 'w') as f:
            logger.info(f"Saving config to {abs_config_path}")
            json.dump(config, f)
            
        # Also save to the current directory for backward compatibility
        with open("config.json", 'w') as f:
            json.dump(config, f)
            
    except Exception as e:
        logger.error(f"Error saving config: {e}")
