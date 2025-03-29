import google.generativeai as genai

# Initialize Gemini with API key
def init_gemini(api_key):
    """Configure Gemini API with the provided key."""
    genai.configure(api_key=api_key)

def clean_output(output):
    """Clean and format Gemini output to ensure it only contains a single shell command."""
    if not output:
        return "No valid command generated."
    # Remove markdown formatting and extra spaces
    output = output.strip().replace("```bash", "").replace("```", "").strip()
    command_lines = output.splitlines()
    
    # Ensure only one command is returned
    if len(command_lines) > 1:
        for line in command_lines:
            line = line.strip()
            if line:
                return line
    
    return output

def get_command(prompt):
    """Send natural language command to Gemini and get a clean shell command."""
    
    few_shot_prompt = (
    f"You are a professional shell assistant. "
    f"Your task is to generate a SINGLE, valid, and most probable shell command "
    f"based on the given natural language instruction. "
    f"Do NOT include any explanations, comments, markdown formatting, or text labels. "
    f"Strictly return ONLY the shell command itself.\n\n"

    f"### Examples:\n"
    
    # 🟢 Basic Commands
    f"Natural language: 'List all files in the current directory'\n"
    f"ls\n\n"

    f"Natural language: 'Create a new directory called myfolder'\n"
    f"mkdir myfolder\n\n"

    f"Natural language: 'Delete a file named data.txt'\n"
    f"rm data.txt\n\n"

    f"Natural language: 'Rename file.txt to newfile.txt'\n"
    f"mv file.txt newfile.txt\n\n"

    f"Natural language: 'Display the current working directory'\n"
    f"pwd\n\n"

    # 🔥 Complex Commands with Options
    f"Natural language: 'Find all .log files larger than 10MB and delete them'\n"
    f"find . -type f -name '*.log' -size +10M -exec rm -f {{}} \\;\n\n"

    f"Natural language: 'Search for the word ERROR in log.txt, case-insensitive'\n"
    f"grep -i 'ERROR' log.txt\n\n"

    f"Natural language: 'Move all .jpg files to the images folder'\n"
    f"mv *.jpg images/\n\n"

    f"Natural language: 'Show the last 20 lines of the system log'\n"
    f"tail -n 20 /var/log/syslog\n\n"

    f"Natural language: 'Copy all PDF files to the backup directory'\n"
    f"cp *.pdf backup/\n\n"

    f"Natural language: 'Display all running processes with detailed information'\n"
    f"ps aux\n\n"

    # 🔥 Advanced Commands
    f"Natural language: 'Get the current disk usage in human-readable format'\n"
    f"df -h\n\n"

    f"Natural language: 'Count the number of lines in script.sh'\n"
    f"wc -l script.sh\n\n"

    f"Natural language: 'Show memory usage in megabytes'\n"
    f"free -m\n\n"

    f"Natural language: 'Display the IP address of the current machine'\n"
    f"ip a\n\n"

    f"Natural language: 'Compress the directory logs into logs.tar.gz'\n"
    f"tar -czvf logs.tar.gz logs\n\n"

    # 🔥 Network and System Commands
    f"Natural language: 'Ping google.com 5 times'\n"
    f"ping -c 5 google.com\n\n"

    f"Natural language: 'Check if port 80 is open on 192.168.1.1'\n"
    f"nc -zv 192.168.1.1 80\n\n"

    f"Natural language: 'Download a file from example.com'\n"
    f"wget http://example.com/file.zip\n\n"

    f"Natural language: 'Show the current date and time'\n"
    f"date\n\n"

    f"Natural language: 'Show the current month’s calendar'\n"
    f"cal\n\n"

    f"Natural language: 'Kill all processes named firefox'\n"
    f"pkill firefox\n\n"

    f"Natural language: 'Show all open network ports'\n"
    f"netstat -tuln\n\n"

    f"Natural language: 'Check the system uptime'\n"
    f"uptime\n\n"

    # 🔥 Network and Port Commands
    f"Natural language: 'Kill the process running on port 8080'\n"
    f"fuser -k 8080/tcp\n\n"

    f"Natural language: 'Kill all processes using port 3000'\n"
    f"kill -9 $(lsof -t -i :3000)\n\n"

    f"Natural language: 'Find the PID of the process using port 8000'\n"
    f"lsof -t -i :8000\n\n"

    # 🔥 File and Data Manipulation
    f"Natural language: 'Extract all lines containing ERROR from log.txt and save them to errors.txt'\n"
    f"grep 'ERROR' log.txt > errors.txt\n\n"

    f"Natural language: 'Sort the contents of data.txt alphabetically'\n"
    f"sort data.txt\n\n"

    f"Natural language: 'Replace all occurrences of foo with bar in file.txt'\n"
    f"sed -i 's/foo/bar/g' file.txt\n\n"

    f"Natural language: 'Combine contents of file1.txt and file2.txt into combined.txt'\n"
    f"cat file1.txt file2.txt > combined.txt\n\n"

    # 🔥 Custom Prompt Execution
    f"Natural language: '{prompt}'\n"
)

    
    # Use the optimized flash model
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    try:
    
        response = model.generate_content(few_shot_prompt)
        command = clean_output(response.text) if response and response.text else "No valid command generated."

    except Exception as e:
        command = f"Error: {str(e)}"
    
    return command
