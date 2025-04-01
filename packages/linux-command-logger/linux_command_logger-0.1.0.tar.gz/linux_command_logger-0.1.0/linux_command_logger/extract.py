import os
import platform

def extract_history(command_count=10):
    """Extracts the last `command_count` commands from history and saves them to a file."""
    history_file = os.path.join(os.path.dirname(__file__), "history_commands.txt")

    try:
        if platform.system() == "Windows":
            os.system(f'(Get-Content (Get-PSReadlineOption).HistorySavePath) | Select-Object -Last {command_count} > temp_history.txt')
        else:
            os.system(f"history | awk '{{print substr($0, index($0,$2))}}' | tail -n {command_count} > temp_history.txt")

        with open("temp_history.txt", "r", encoding="utf-8") as file:
            commands = list(set([line.strip() for line in file if line.strip()]))

        with open(history_file, "w", encoding="utf-8") as file:
            file.write("\n".join(commands))

        os.remove("temp_history.txt")
        print(f"✅ Extracted last {command_count} commands to {history_file}")

    except Exception as e:
        print(f"❌ Error extracting history: {str(e)}")

def main():
    """CLI entry point."""
    try:
        count = int(input("Enter number of recent commands to extract (default: 10): ") or 10)
        extract_history(count)
    except ValueError:
        print("❌ Invalid input! Please enter a valid number.")

if __name__ == "__main__":
    main()
