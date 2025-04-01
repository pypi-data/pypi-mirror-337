# DSRS CLI Chat 🚀                                                                                                         
                                                                                                                         
A lightweight, feature-rich, interactive AI chatbot for your command line, powered by OpenAI-compatible APIs.                           

                                                                                                                         
## Features                                                                                                                
                                                                                                                         
*   **Interactive Chat:** Engage in conversations with an AI model directly from your terminal.                            
*   **OpenAI Compatible:** Connects to any OpenAI-compatible API endpoint.                                                 
*   **Streaming Responses:** Watch the AI's response appear in real-time.                                                  
*   **Rich Output:** Uses `rich` for beautiful Markdown rendering, including code blocks with syntax highlighting.         
*   **Advanced Input:** Uses `prompt_toolkit` for:                                                                         
  *   Multi-line input (easy pasting).                                                                                   
  *   Persistent command history (Up/Down arrows).                                                                       
  *   Input clearing (`Ctrl+U`).                                                                                         
  *   Tab completion for model selection.                                                                                
*   **Interruptible Generation:** Stop the AI mid-response with `Ctrl+X`.                                                  
*   **Model Selection:** Choose from available models provided by the API endpoint.                                        
*   **Custom System Prompt:** View and modify the system prompt guiding the AI's behavior.                                 
*   **Credential Management:** Load API Key and Base URL securely from a `.env` file or enter them manually.               
*   **Useful Commands:** `clear`, `restart`, `model`, `system`, `instructions`, `exit`/`quit`.                             
*   **Exit Summary:** Displays the final context sent to the AI and its last response upon quitting.                       
*   **Cross-Platform:** Designed to work on Linux, macOS, and Windows.                                                     
                                                                                                                         
## Requirements                                                                                                            
                                                                                                                         
*   Python 3.7+                                                                                                            
*   Pip (Python package installer)                                                                                         
*   An API Key and Base URL for an OpenAI-compatible API endpoint.                                                         
                                                                                                                         

## Installation

To install, just run:
```bash
pip install dsrs-cli
```



## Configuration                                                                                                           
                                                                                                                         
The script needs your API Key and the Base URL for the AI service.                                                         
                                                                                                                         
*   **Using `.env` file (Recommended):**                                                                                   
  *   Create a file named `.env` in the same directory where you run the script (or where `dsrs_cli.py` is located if    
installing).                                                                                                               
  *   Add the following lines, replacing the placeholders with your actual credentials:                                  
      ```dotenv                                                                                                          
      OPENAI_API_KEY=...
      BASE_URL=...
      ```                                                                                                                
  *   When you run the script, choose 'y' when asked "Load API Key and Base URL from .env file?".                        
                                                                                                                         
*   **Manual Input:**                                                                                                      
  *   If you don't use a `.env` file or it's missing credentials, the script will prompt you to enter the API Key        
(hidden) and Base URL securely when it starts.                                                                             
                                                                                                                         
## Usage                                                                                                                   

After installing, run:

```bash                                                                                                                    
dsrs-chat                                                                                                                  
```

Interacting with the Chat:                                                                                                  
                                                                                                                         
* Type your message. For multi-line input, press Esc then Enter (or your terminal's default for submitting multi-line).    
* **Commands**:                                                                                                                
 * instructions: Show the welcome message and commands again.                                                            
 * model: Select a different AI model from the available list.                                                           
 * system: View the current system prompt and optionally change it.                                                      
 * clear: Clear the terminal screen.                                                                                     
 * restart: Restart the chat application.                                                                                
 * exit or quit: Exit the chat application.                                                                              
* **Shortcuts**:
 * Ctrl+X: Interrupt the AI while it's generating a response.                                                            
 * Ctrl+U: Clear the current input line.                                                                                 
 * Up/Down Arrows (on empty line): Navigate through input history.                                                       
 * Ctrl+C: Exit the application immediately.                                                                             
 * Ctrl+D (EOF): Exit the application gracefully.                                                                                        