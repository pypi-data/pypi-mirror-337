import os
import platform
from dotenv import load_dotenv
from google import genai

load_dotenv()  
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    print("❌ Error: Please set the GEMINI_API_KEY environment variable.")
    exit(1)

try:
    client = genai.Client(api_key=GEMINI_API_KEY)
except Exception as e:
    print(f"❌ Error initializing Gemini API client: {str(e)}")
    exit(1)

def fetch_recent_commands(command_count=10):
    """Fetch the last `command_count` commands dynamically without saving them to a file."""
    try:
        commands = []

        if platform.system() == "Windows":
            # PowerShell history is saved in a specific file in the user's profile
            history_file = os.path.expandvars(r"%USERPROFILE%\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadline\ConsoleHost_history.txt")
            if os.path.exists(history_file):
                with open(history_file, "r", encoding="utf-8") as file:
                    commands = file.readlines()

            # Get the last `command_count` commands
            commands = commands[-command_count:]

        else:
            # Bash/Zsh history
            cmd = f"history | awk '{{print substr($0, index($0,$2))}}' | tail -n {command_count}"
            stream = os.popen(cmd)
            commands = stream.read().strip().split("\n")

        # Remove empty commands and duplicates
        return list(set(cmd.strip() for cmd in commands if cmd.strip()))

    except Exception as e:
        print(f"❌ Error fetching command history: {str(e)}")
        return []

def get_explanation(command):
    """Fetch concise explanations for a given command using Gemini API, without an example."""
    try:
        # Request a brief explanation of the command, focusing only on its purpose
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=f"Provide a brief explanation of the Linux/Windows command `{command}`. Include its purpose only."
        )
        
        explanation = response.text.strip() if response.text else "No explanation found."
        
        # Return a concise, Markdown-formatted explanation
        return f"### `{command}`\n\n**Purpose:**\n{explanation}\n\n---\n"
    
    except Exception as e:
        return f"❌ Error explaining command `{command}`: {str(e)}\n\n"

def generate_markdown(command_count=10):
    """Dynamically fetch recent commands and generate a Markdown file with explanations."""
    commands = fetch_recent_commands(command_count)

    if not commands:
        print("❌ No recent commands found.")
        return

    markdown_content = "# 🔹 Linux & Windows Command Explanations\n\n"
    
    for cmd in sorted(commands):
        markdown_content += get_explanation(cmd)

    # Save the Markdown file
    output_file = "commands.md"
    with open(output_file, "w", encoding="utf-8") as md_file:
        md_file.write(markdown_content)

    print(f"✅ Documentation saved in {output_file}")

def main():
    """CLI entry point."""
    try:
        count = int(input("Enter number of recent commands to explain (default: 10): ") or 10)
        generate_markdown(count)
    except ValueError:
        print("❌ Invalid input! Please enter a valid number.")

if __name__ == "__main__":
    main()
