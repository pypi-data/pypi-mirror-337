🌟 SmartShell – AI-Powered Terminal Assistant
🚀 SmartShell is an AI-driven command-line tool that converts natural language into shell commands, making it easier to interact with your terminal.

🔹 Supports:
✅ Online Mode (Uses OpenAI API)
✅ Offline Mode (Uses Ollama for local LLM execution)

🎨 Built with: Click, Rich, Colorama, RapidFuzz, OpenAI, Ollama

📥 Installation
🔹 Install via pip
sh
Copy
Edit
pip install smartshell
🔹 Upgrade to the latest version
sh
Copy
Edit
pip install --upgrade smartshell
🚀 Usage
🔍 Convert Natural Language to Commands
sh
Copy
Edit
smartshell translate "list all files"
👉 SmartShell will convert it to:

sh
Copy
Edit
ls -la  # (Linux/macOS)
dir /a  # (Windows)
➕ Add Custom Commands
sh
Copy
Edit
smartshell add "show my IP" "ipconfig" "ifconfig"
❌ Remove Custom Commands
sh
Copy
Edit
smartshell remove "show my IP"
🔄 Update Commands from a Remote JSON
sh
Copy
Edit
smartshell update https://example.com/commands.json
⚙️ Features
✔ AI-Powered – Understands natural language queries
✔ Offline & Online Support – Uses OpenAI API online, Ollama for offline mode
✔ Fuzzy Matching – Finds the best matching command
✔ Cross-Platform – Works on Windows, macOS, and Linux
✔ Custom Commands – Add your own translations

🛠️ Requirements
Python 3.7+

pip install smartshell

