# Small AI chatbot for the CLI                                                                                         
                                                                                                                     
# python ~/shared-dsrs/ai-models/dsrs-cli/dsrs-cli.py                                                                  
                                                                                                                     
ASCII = """[bold red]                                                                                                  
                                                                                                                     
                    ██████╗ ███████╗██████╗ ███████╗     ██████╗██╗     ██╗     ██████╗██╗  ██╗ █████╗ ████████╗     
                    ██╔══██╗██╔════╝██╔══██╗██╔════╝    ██╔════╝██║     ██║    ██╔════╝██║  ██║██╔══██╗╚══██╔══╝     
                    ██║  ██║███████╗██████╔╝███████╗    ██║     ██║     ██║    ██║     ███████║███████║   ██║        
                    ██║  ██║╚════██║██╔══██╗╚════██║    ██║     ██║     ██║    ██║     ██╔══██║██╔══██║   ██║        
                    ██████╔╝███████║██║  ██║███████║    ╚██████╗███████╗██║    ╚██████╗██║  ██║██║  ██║   ██║        
                    ╚═════╝ ╚══════╝╚═╝  ╚═╝╚══════╝     ╚═════╝╚══════╝╚═╝     ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝        
                                                                                                                     
[/bold red]"""                                                                                                        
                                                                                                                     
import sys                                                                                                             
import os                                                                                                              
import subprocess                                                                                                      
import threading                                                                                                       
import time                                                                                                            
from dotenv import load_dotenv                                                                                         
                                                                                                                     
# Platform specific imports for non-blocking TTY input                                                                 
if sys.platform == 'win32':                                                                                            
    import msvcrt                                                                                                    
else:                                                                                                                  
    import tty                                                                                                       
    import termios                                                                                                   
    import select                                                                                                    
                                                                                                                     
from openai import OpenAI                                                                                              
import tiktoken                                                                                                        
import re                                                                                                              
import json                                                                                                            
                                                                                                                     
from rich.console import Console                                                                                       
from rich.live import Live                                                                                             
from rich.markdown import Markdown                                                                                     
# from rich.prompt import Prompt, IntPrompt, Confirm # No longer using Rich prompts                                    
from rich.panel import Panel                                                                                           
                                                                                                                     
# --- Use prompt_toolkit for ALL interactive prompts ---                                                               
from prompt_toolkit import prompt                                                                                      
from prompt_toolkit.shortcuts import confirm  # For y/n questions                                                       
from prompt_toolkit.completion import WordCompleter                                                                    
from prompt_toolkit.key_binding import KeyBindings  # <-- Import KeyBindings                                            
from prompt_toolkit.history import InMemoryHistory                                                                     
from prompt_toolkit.validation import Validator, ValidationError                                                       
from prompt_toolkit.buffer import Buffer  # <-- Import Buffer for accept_handler type hint



# ===================================================================== #                                              
# Configuration / Constants                                                                                            
# ===================================================================== #                                              
DEFAULT_SYSTEM_PROMPT = """                                                                                            
You are a helpful AI assistant that can answer everything and help with anything.                                      
You are capable of reasoning, and are an amazing coder! Be concise and informative.                                    
                                                                                                                     
Your true identity is '{model}'.                                                                                       
"""



# ===================================================================== #                                              
# Functions                                                                                                            
# ===================================================================== #                                              


def restart_program():
    """Forcibly restarts the app (cross-platform"""
    python = sys.executable
    os.execl(python, python, *sys.argv)
                                                                                                                     


def check_for_interrupt(stop_event: threading.Event):
    """
    Listens for Ctrl+X in a non-blocking way and sets the stop_event.
    Runs in a separate thread.
    """
    try:
        if sys.platform == 'win32':
            while not stop_event.is_set():
                if msvcrt.kbhit():
                    char = msvcrt.getch()
                    # Ctrl+X is b'\x18'
                    if char == b'\x18':
                        stop_event.set()
                        break
                time.sleep(0.05)  # Prevent busy-waiting
        else:
            # Linux/macOS
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setcbreak(fd)  # Read characters immediately
                while not stop_event.is_set():
                    # Check if input is available with a timeout
                    if select.select([sys.stdin], [], [], 0.05) == ([sys.stdin], [], []):
                        char = sys.stdin.read(1)
                        # Ctrl+X is '\x18'
                        if char == '\x18':
                            stop_event.set()
                            break
            finally:
                # VERY IMPORTANT: Restore terminal settings
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    except Exception as e:
        # Log potential errors in the listener thread (optional)
        # console.print(f"[dim red]Error in input listener: {e}[/dim red]")
        pass  # Avoid crashing the main app due to listener errors
                                                                                                                     



def stream_response(stream, stop_event: threading.Event):
    """
    Displays the streamed response using rich.Live and checks the stop_event.
    """
    code_theme = "github"
    accumulated_text = ""
    interrupted = False

    # Start the interrupt listener thread
    listener_thread = threading.Thread(target=check_for_interrupt, args=(stop_event,), daemon=True)
    # Daemon=True ensures the thread exits if the main program exits
    listener_thread.start()

    panel = Panel(Markdown(accumulated_text),
                  title="[bold magenta]AI[/bold magenta]",
                  border_style="magenta")

    try:
        with Live(panel, refresh_per_second=10, console=console) as live:
            for c in stream:
                # --- Check for interrupt ---
                if stop_event.is_set():
                    live.update(Panel(Markdown(accumulated_text + "\n\n[bold red]Interrupted by user (Ctrl+X).[/bold red]"),
                                       title="[bold magenta]AI[/bold magenta]",
                                       border_style="red"), refresh=True)
                    interrupted = True
                    break  # Exit the loop

                text = c.choices[0].delta.content or ""
                accumulated_text += text

                # Update the panel content dynamically
                panel = Panel(Markdown(accumulated_text, code_theme=code_theme),
                              title="[bold magenta]AI[/bold magenta]",
                              border_style="magenta")
                live.update(panel, refresh=True)  # Refresh needed to show updates

    except Exception as e:
        console.print(f"\n[bold red]Error during streaming:[/bold red] {e}")
        # Ensure the event is set if streaming fails, so listener thread can exit
        stop_event.set()
        interrupted = True  # Treat errors as interruption of the full response
    finally:
        # --- Cleanup ---
        # Ensure the listener thread knows it should stop (if not already set by Ctrl+X)
        stop_event.set()
        # Wait briefly for the listener thread to finish cleaning up terminal settings
        listener_thread.join(timeout=0.5)

    # Return accumulated text *even if interrupted*
    return accumulated_text, interrupted
                                                                                                                     


def generate(user_input, chat_history, model, system_prompt):
    messages = [
        {
            "role": "system",
            # --- MODIFICATION: Use the passed system_prompt ---
            "content": system_prompt.format(model=model)  # Use .format() to insert model name
        }
    ]
    # --- Suggestion: More robust history merging ---
    # Check if chat_history is not empty before extending
    if chat_history:
        messages.extend(chat_history)

    messages.append({"role": "user",
                     "content": user_input})

    ai_response = ""
    interrupted = False
    stop_event = threading.Event()  # Create a new event for this generation

    try:
        stream = client.chat.completions.create(
            model=model,
            messages=messages,
            stream=True,
            # --- Suggestion: Consider adjusting max_tokens ---
            # 10k might be very large depending on the model/context limits
            max_tokens=10_000,
            temperature=0.6,
            top_p=0.95,
        )

        ai_response, interrupted = stream_response(stream, stop_event)

    except Exception as e:
        console.print(f"\n[bold red]An unexpected error occurred during generation:[/bold red] {e}")
        # Return the messages list as it was *before* the failed API call
        # The caller can decide if they want to retry or discard
        return None, messages[:-1], True  # Indicate an error occurred

    # --- MODIFICATION: Return the *full* messages list including the user input ---
    # This is useful for the exit summary
    return ai_response, messages, interrupted  # Return interruption status
                                                                                                                     


def chat_his(chat_history, user_prompt, ai_response):
    chat_history.append({"role": "user",
                         "content": user_prompt})
    if ai_response:
        chat_history.append({"role": "assistant",
                             "content": ai_response})
    return chat_history
                                                                                                                     


def select_model(client, console):
    """Fetches available models and prompts the user to select one using prompt_toolkit."""
    try:
        available_models_data = client.models.list().data
        if not available_models_data:
            console.print("[red]Error:[/red] No models available from the API endpoint.")
            return None  # Indicate failure

        # --- Process models OUTSIDE the 'if not' block ---
        available_models = sorted([m.id for m in available_models_data])
        if not available_models:  # Double check if the list ended up empty
            console.print("[red]Error:[/red] Model list was processed but is empty.")
            return None

        # --- Define completer and validator ---
        model_completer = WordCompleter(available_models, ignore_case=True)

        class ModelValidator(Validator):
            def validate(self, document):
                text = document.text
                if text not in available_models:
                    # --- Simpler message for now ---
                    msg = "Invalid model. Select from the list (use Tab)."
                    raise ValidationError(
                        message=msg,
                        cursor_position=len(text))
        # --- Perform prompting OUTSIDE the validator ---
        console.print("\nSelect Model [dim](start typing | Tab suggests | Enter confirms)[/dim]:")
        # --- Use prompt_toolkit for model selection ---
        chosen_model = prompt(
            "Model: ",
            completer=model_completer,
            complete_while_typing=True,
            validator=ModelValidator(),
            validate_while_typing=False  # Only validate on Enter
        )
        return chosen_model  # Return the selected model name

    # --- Catch KeyboardInterrupt during model selection ---
    except KeyboardInterrupt:
        console.print("\n[dim]Model selection cancelled.[/dim]")
        return None
    except Exception as e:
        console.print(f"[red]Error fetching/selecting models:[/red] {e}")
        # console.print_exception()  # Uncomment for full traceback during debugging
        return None  # Indicate failure
                                                                                                                     


def welcome_panel(model):
    welcome_panel = Panel(f"""
                                                                                                                     
[green]Multi-line input supported; copy-paste freely![/green]                                                        
Submit messages with: [code][italic]Esc -> Enter[/italic][/code] (or check your terminal's default)                  
                                                                                                                     
Type:                                                                                                                
- '[blue]instructions[/blue]' to print the instructions (this message)                                               
- '[yellow]model[/yellow]' to select a new AI model                                                                 
- '[magenta]system[/magenta]' to view/change the system prompt                                                            
- '[grey]clear[/grey]' to clear screen                                                                               
- 'exit'/'quit' to end                                                                                               
- '[red]restart[/red]' to restart the app                                                                            
                                                                                                                     
Press [bold red]Ctrl+X[/bold red] during AI response to interrupt.                                                     
Press [bold magenta]Ctrl+U[/bold magenta] to clear the current input line.
[dim]Use Up/Down arrows on empty line to navigate history.[/dim]
                                                                                                                     
Model: [bold]{model}[/bold]
""",
    title="DSRS CLI Chat 🚀 ",
    subtitle="DSRS CLI Chat 🚀 ",
    border_style="bold blue",
    expand=True)
    return welcome_panel
                                                                                                                     


# --- Validator for non-empty input ---                                                                                
class NotEmptyValidator(Validator):
    def validate(self, document):
        text = document.text.strip()
        if not text:
            raise ValidationError(
                message="Input cannot be empty.",
                cursor_position=len(document.text))  # Move cursor to end
                                                                                                                     


# --- NEW: Accept handler for prompt_toolkit ---                                                                       
def accept_if_not_empty(buffer: Buffer) -> bool:
    """Accept input only if it's not empty or just whitespace."""
    return bool(buffer.text.strip())
                                                                                                                     

# --- NEW: Key bindings for prompt_toolkit ---                                                                         
bindings = KeyBindings()
                                                                                                                     

@bindings.add('c-u')  # Bind Ctrl+U                                                                                     
def _clear_line(event):
    """ Clears the current input buffer. """
    event.app.current_buffer.reset()
                                                                                                                     




                                                                                                                     
# ===================================================================== #                                              
# App main loop                                                                                                        
# ===================================================================== #                                              

def main():
    global model, current_system_prompt, client, console, tokenizer
    
    chat_history = []
    messages = []
    last_ai_response = ""
    interrupted_generation = False
    chat_input_history = InMemoryHistory()
    
    # --- Display Welcome/Instructions ---
    console.print(welcome_panel(model))
                                                                                                                     
    while True:
        user_input = None  # Initialize user_input
        interrupted_generation = False  # Reset interrupt flag for the new prompt
                                                                                                                     
        try:
            # --- Use prompt_toolkit for multi-line input with history ---
            user_input = prompt(
                [('fg:ansigreen', 'You: ')],
                multiline=True,
                prompt_continuation="  > ",  # Prefix for continuation lines
                history=chat_input_history,  # Enable history
                key_bindings=bindings  # Add custom key bindings (Ctrl+U)
            )
        except EOFError:
            # Handle Ctrl+D (EOFError) gracefully
            console.print("\n[blue]EOF detected. Exiting chat.[/blue]")
            break
        except KeyboardInterrupt:
            # Handle Ctrl+C (KeyboardInterrupt) gracefully
            console.print("\n[blue]Interrupted by user (Ctrl+C).[/blue]")
            break

        # --- Process user input: trim whitespace and ignore empty messages ---
        user_input = user_input.strip()
        if not user_input:
            continue
                                                                                                                     
        # --- Check for commands ---
        if user_input.lower() == "clear":
            console.clear()
            console.print(welcome_panel(model))
            continue
                                                                                                                     
        if user_input.lower() in ["new", "new chat"]:
            console.clear()
            console.print(welcome_panel(model))
            chat_history = []
            messages = []  # Clear last message list too
            chat_input_history = InMemoryHistory()  # Reset history too
            continue
                                                                                                                     
        if user_input.lower() == "restart":
            console.print("Restarting app...")
            restart_program()
            # No continue needed, os.execl replaces the process
                                                                                                                     
        if user_input.lower() == "instructions":
            console.clear()
            console.print(welcome_panel(model))
            continue
                                                                                                                     
        if user_input.lower() in ["exit", "quit"]:
            break
                                                                                                                     
        if user_input.lower() == "model":
            # --- Handle potential Ctrl+C during model change ---
            try:
                new_model = select_model(client, console)  # Call the function again
                if new_model:
                    model = new_model
                    console.clear()
                    console.print(welcome_panel(model))  # Show updated panel
                elif model:  # Only print error if a model was already selected
                    console.print(f"Model selection cancelled or failed. Continuing with [bold]{model}[/bold].")
                else:
                    # This case should ideally not happen if initial selection worked
                    console.print("[red]Model selection failed. Cannot proceed.[/red]")
                    break  # Exit if no model is selected
            except KeyboardInterrupt:
                console.print("\nModel change cancelled.")
            continue  # Go back to the start of the loop for new input
                                                                                                                     
        # --- NEW: Handle 'system' command ---
        if user_input.lower() == "system":
            console.print("\n[magenta]System Prompt:[/magenta]")
            console.print(Panel(current_system_prompt.format(model=model), border_style="dim magenta", expand=False))
            try:
                console.print("[magenta]Enter new system prompt (Esc -> Enter to submit, Ctrl+C to cancel):[/magenta]")
                new_prompt_input = prompt(
                    "> ",
                    multiline=True,
                    prompt_continuation="  > ",
                    # You could add a validator here if needed
                )
                if new_prompt_input.strip():  # Only update if not empty
                    current_system_prompt = new_prompt_input

                    console.clear()
                    console.print(welcome_panel(model))
                    console.print("\n[magenta]System Prompt:[/magenta]")
                    console.print(Panel(current_system_prompt.format(model=model), border_style="dim magenta", expand=False))
                    

                
                else:
                    console.print("[dim]System prompt not changed (input was empty).[/dim]")
            except KeyboardInterrupt:
                console.print("\n[dim]System prompt change cancelled.[/dim]")
            except EOFError:
                console.print("\n[dim]System prompt change cancelled (EOF).[/dim]")
            continue  # Go back to the main prompt
                                                                                                                     
        # --- AI GENERATION ---
        # --- MODIFICATION: Pass current_system_prompt ---
        ai_response, current_messages, interrupted = generate(user_input, chat_history, model, current_system_prompt)
                                                                                                                     
        interrupted_generation = interrupted  # Store if this specific generation was interrupted
        messages = current_messages  # Store the messages list used for this generation
                                                                                                                     
        if ai_response is not None:
            # Add to history *only if* a response was generated (even partial)
            # Strip check prevents adding empty assistant messages if generation failed instantly
            if ai_response.strip() or interrupted:  # Add even if interrupted but got *some* text
                chat_history = chat_his(chat_history, user_input, ai_response)
                last_ai_response = ai_response  # Update last response
        else:
            # Handle case where generation failed entirely (already printed in generate)
            pass
                                                                                                                     
        # Small delay to ensure prompt appears after potential interrupt messages
        time.sleep(0.1)
                                                                                                                     
    # --- Improved Exit Message ---
    if messages:  # Check if 'messages' was populated by at least one successful/interrupted generation
        try:
            history_json = json.dumps(messages, indent=2)
            total_tokens = "N/A"
            try:
                total_tokens = len(tokenizer.encode(history_json))
            except Exception as enc_e:
                console.print(f"[dim yellow]Warning: Could not calculate token count: {enc_e}[/dim yellow]")
                                                                                                                     
            display_history = history_json
            max_len = 8000  # Max length to display to avoid overwhelming terminal
            if len(history_json) > max_len:
                half_len = max_len // 2
                display_history = history_json[:half_len] + "\n\n[dim]... (history truncated) ...[/dim]\n\n" + history_json[-half_len:]
                                                                                                                     
            final_panel_content = f"""
[bold]Final context sent to AI:[/bold]
----------------------------------------------------------------
{display_history}
----------------------------------------------------------------

[bold]AI's last response ({'partially shown' if interrupted_generation else 'fully shown'}):[/bold]
{last_ai_response if last_ai_response else '[No response generated or recorded]'}
            """
                                                                                                                     
            final_panel = Panel(final_panel_content,
                                title="Chat Summary",
                                subtitle=f"Total tokens in Last Context: {total_tokens}",
                                border_style="green",
                                expand=False)  # Use expand=False for better fitting
                                                                                                                     
            console.print(final_panel)
                                                                                                                     
        except Exception as e:
            console.print(f"[red]Could not display final chat history: {e}[/red]")
            # Fallback: print raw last response if panel fails
            if last_ai_response:
                console.print("\n[bold]AI's last response:[/bold]")
                console.print(last_ai_response)
    else:
        console.print("\n[dim]No chat interactions recorded.[/dim]")
                                                                                                                     
    console.print("\n[bold blue]Exiting DSRS CLI Chat. Goodbye! 👋[/bold blue]")






# ===================================================================== #                                                  
# Script Execution Guard                                                                                                   
# ===================================================================== #                                                  
if __name__ == "__main__":
                                       
    console = Console()                                                                                                                     
    console.clear()
    console.print(ASCII)                                                                      
    tokenizer = tiktoken.get_encoding("o200k_base")
                                                                                                                         
    openai_api_key = ""
    base_url = ""
    use_env = False
    model = None
    client = None
    current_system_prompt = DEFAULT_SYSTEM_PROMPT

    setup_successful = False
                                                                                                                         
    try:  # Wrapped initial setup in try/except for Ctrl+C
        
        # --- Use prompt_toolkit confirm ---                                                                                 
        use_env = confirm("Load API Key and Base URL from .env file?")
                                                                                                                         
        if use_env:
            console.print("[dim]Loading credentials from .env file...[/dim]")
            load_dotenv()
            openai_api_key = os.getenv("OPENAI_API_KEY", "")
            base_url = os.getenv("BASE_URL", "")
                                                                                                                         
            if not openai_api_key:
                console.print("[red]Warning: OPENAI_API_KEY not found in .env file.[/red]")
            if not base_url:
                console.print("[red]Warning: BASE_URL not found in .env file.[/red]")
        else:
            console.print("\n[dim]Please enter your credentials manually:")
            # --- Use prompt_toolkit for manual input ---                                                                    
            not_empty_validator = NotEmptyValidator()
                                                                                                                         
            while not openai_api_key:
                openai_api_key = prompt(
                    "OPENAI_API_KEY: ",
                    is_password=True,  # Hide input
                    validator=not_empty_validator,
                    validate_while_typing=False  # Validate only on Enter
                )
                openai_api_key = openai_api_key.strip().strip("'\"")# Strip potential quotes the user might paste
                
            while not base_url:
                base_url = prompt(
                    "BASE_URL: ",
                    validator=not_empty_validator,
                    validate_while_typing=False  # Validate only on Enter
                )
                base_url = base_url.strip().strip("'\"") # Strip potential quotes
                                                                                                                         
        # --- Check if credentials were successfully obtained ---                                                            
        if not openai_api_key or not base_url:
            console.print("[bold red]Error: API Key or Base URL missing or failed to load. Exiting.[/bold red]")
            sys.exit(1)
                                                                                                                         
        # --- Credentials obtained, proceed with using them ---                                                              
        console.print("[green]Credentials loaded successfully.[/green]")
        client = OpenAI(
            api_key=openai_api_key,
            base_url=base_url,
        )
                                                                                                                         
        # --- Initial Model Selection ---                                                                                    
        model = select_model(client, console)  # Assign to global 'model'
        if not model:
            console.print("[bold red]Failed to select an initial model. Double-check your credentials or try again.[/bold red] \n[dim]Exiting...[/dim]")
            sys.exit(1)

        # --- Successful setup ---                                                                                    
        setup_successful = True
                                                                                                                         
    # --- Catch Ctrl+C during initial setup/credential entry ---                                                           
    except KeyboardInterrupt:
        console.print("\nSetup interrupted by user (Ctrl+C). Exiting.")
        sys.exit(0)  # Use 0 for user-initiated exit
    # --- Catch other potential setup errors ---                                                                           
    except Exception as e:
        console.print(f"[bold red]Error during initial setup:[/bold red] {e}")
        sys.exit(1)



    
    # --- Run main() ONLY if setup was successful ---                                                                      
    if setup_successful:                                                                                                   
        try:                                                                                                               
            main()
        except KeyboardInterrupt:
            pass
        except Exception as e:                                                                                             
            # Catch unexpected errors during the main loop                                                                 
            console.print(f"\n[bold red]An unexpected error occurred in the main loop:[/bold red] {e}")                    
            # import traceback                                                                                             
            # traceback.print_exc()                                                                                        
            sys.exit(1) # Exit with error status                                                                                                                                                               











