import click
import os
import subprocess
import json
import logging
import platform
import requests
import time
import sys
import re
from rapidfuzz import process
from colorama import Fore, Style
from rich.console import Console
from rich.text import Text

# AI Integration
import openai
import ollama

# ✅ Cross-platform readline fix
if sys.platform == "win32":
    import pyreadline3 as readline
else:
    import readline

console = Console()

def welcome_message():
    console.print("\n" + "=" * 50, style="bold cyan")  # Top glowing line
    message = "🌟 Welcome to SmartShell! 🌟"

    for i in range(1, len(message) + 1):  # Typewriter animation
        console.print(Text(message[:i], style="bold magenta"), end="\r")
        time.sleep(0.05)

    console.print("\n" + "=" * 50, style="bold cyan")  # Bottom glowing line

welcome_message()

# 📌 File Paths
TRANSLATIONS_FILE = os.path.join(os.path.dirname(__file__), "commands.json")
LOG_FILE = os.path.join(os.path.dirname(__file__), "smartshell.log")
USER_HISTORY_FILE = os.path.join(os.path.dirname(__file__), "user_history.json")

# 📝 Logging Setup
logging.basicConfig(filename=LOG_FILE, level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")

# 📌 Detect OS Type
is_windows = platform.system().lower() == "windows"

# 📌 Load Commands from JSON
def load_commands():
    if os.path.exists(TRANSLATIONS_FILE):
        with open(TRANSLATIONS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return {}

translations = load_commands()

# 🔍 Fuzzy Matching for Best Command
def find_best_match(command, translations):
    result = process.extractOne(command, translations.keys(), score_cutoff=85)
    return result[0] if result else None

# 🔍 Check Internet Connection
def is_online():
    try:
        requests.get("https://www.google.com", timeout=3)
        return True
    except requests.ConnectionError:
        return False

# ✅ AI System Prompt (Refined)
system_prompt = (
    "You are SmartShell, an intelligent shell assistant that accurately converts natural language into executable shell commands."
    "\n\n## 🌟 Guidelines:\n"
    "- **Always provide an exact and accurate command.**"
    "- **Detect the OS and use correct syntax (PowerShell for Windows, Bash for Linux/macOS).**"
    "- **For software installations, use the correct package manager:**\n"
    "  - Windows: `winget install <software>`\n"
    "  - Ubuntu: `sudo apt install <software>`\n"
    "  - Fedora: `sudo dnf install <software>`\n"
    "  - macOS: `brew install <software>`\n"
    "- **If a command is destructive (e.g., `rm -rf /`), warn the user.**"
)

# 🤖 AI-based Command Suggestion with Storytelling
def get_ai_suggestion(nl_command, explain=False):
    if is_online():
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "system", "content": system_prompt},
                          {"role": "user", "content": f"Convert this command: {nl_command} and explain it."}],
                temperature=0
            )
            suggestion = response["choices"][0]["message"]["content"].strip()
            if explain:
                explanation = suggestion.split('\n')[0]  # Extract the explanation part
                return suggestion, explanation
            return suggestion, None
        except Exception as e:
            logging.error(f"OpenAI API Error: {e}")
            return None, None
    else:
        try:
            response = ollama.chat(
                model="mistral",
                messages=[{"role": "system", "content": system_prompt},
                          {"role": "user", "content": f"Convert this command: {nl_command} and explain it."}]
            )
            suggestion = response["message"]["content"].strip()
            if explain:
                explanation = suggestion.split('\n')[0]
                return suggestion, explanation
            return suggestion, None
        except Exception as e:
            logging.error(f"Ollama Processing Error: {e}")
            return None, None

# 📌 Store and Retrieve Recent Commands for Context-Aware Suggestions
recent_commands = []

def load_user_history():
    if os.path.exists(USER_HISTORY_FILE):
        with open(USER_HISTORY_FILE, "r") as file:
            return json.load(file)
    return {}

def save_user_history(history):
    with open(USER_HISTORY_FILE, "w") as file:
        json.dump(history, file, indent=4)

# Track user's favorite or frequent commands
user_history = load_user_history()

def store_command(command):
    if len(recent_commands) >= 5:
        recent_commands.pop(0)  # Keep history to last 5 commands
    recent_commands.append(command)
    update_user_history(command)

def update_user_history(command):
    if command not in user_history:
        user_history[command] = 0
    user_history[command] += 1
    save_user_history(user_history)

def get_context_aware_suggestion(command):
    context = " ".join(recent_commands)
    return get_ai_suggestion(f"{command} considering previous actions: {context}")

# 🎛️ CLI Setup
@click.group()
def cli():
    """SmartShell: Convert Natural Language to Shell Commands.""" 
    pass

# 🔄 Translate & Execute Command
@cli.command()
@click.argument("nl_command", nargs=-1)
def translate(nl_command):
    """Convert natural language to a shell command and execute it."""
    
    if not nl_command:
        console.print("❌ Please enter a valid command.", style="bold red")
        return

    command = " ".join(nl_command).lower()
    best_match = find_best_match(command, translations)

    if best_match:
        command_info = translations.get(best_match)
        shell_command = command_info.get("windows" if is_windows else "linux")
    else:
        console.print("🤖 No match found! Asking AI for help...", style="bold cyan")
        shell_command, explanation = get_ai_suggestion(command, explain=True)

        if not shell_command:
            console.print("❌ AI could not generate a command. Try rewording.", style="bold red")
            return

        # Ensure explanation is returned and displayed
        if explanation:
            console.print(f"🔍 Explanation: {explanation}", style="bold green")
        else:
            console.print("❓ No explanation available.", style="bold yellow")

    # ✅ Remove ANSI escape sequences safely
    shell_command = re.sub(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])', '', shell_command)

    # ✅ Display final cleaned command
    console.print(f"⚡ Suggested command: {shell_command}", style="bold yellow")

    confirmation = input(f"🔹 Run this command? (y/n): ").strip().lower()
    if confirmation == "y":
        try:
            result = subprocess.run(shell_command, shell=True, capture_output=True, text=True)
            store_command(shell_command)  # Store executed command in history
            console.print(result.stdout if result.stdout else result.stderr, style="bold cyan")
        except Exception as e:
            logging.error(f"Command Execution Error: {e}")
            console.print("❌ An error occurred while executing the command.", style="bold red")
    else:
        console.print("❌ Command execution canceled.", style="bold red")


 # ➕ Add New Custom Commands
@cli.command()
@click.argument("nl_command")
@click.argument("windows_command")
@click.argument("linux_command", required=False)
def add(nl_command, windows_command, linux_command):
    """Add a new custom command for Windows and Linux."""
    translations[nl_command.lower()] = {
        "windows": windows_command,
        "linux": linux_command if linux_command else windows_command
    }
    
    print(Fore.GREEN + f"✅ Command '{nl_command}' added successfully!" + Style.RESET_ALL)

# ❌ Remove Custom Command
@cli.command()
@click.argument("nl_command")
def remove(nl_command):
    """Remove a custom command."""
    if nl_command.lower() in translations:
        del translations[nl_command.lower()]
       
        print(Fore.GREEN + f"✅ Command '{nl_command}' removed successfully!" + Style.RESET_ALL)
    else:
        print(Fore.RED + f"❌ Command '{nl_command}' not found." + Style.RESET_ALL)
       


# 🚀 Run CLI
if __name__ == "__main__":
    cli()
