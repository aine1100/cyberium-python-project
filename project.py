import re
import subprocess
import platform
import time

# Define the path to the log file for Linux systems
log_file_path = '/var/log/auth.log'

# Function to parse the log file and extract relevant information for Linux
def parse_log_linux(log_file_path):
    with open(log_file_path, 'r') as file:
        logs = file.readlines()

    for line in logs:
        timestamp, user, command, action = extract_info_linux(line)
        if timestamp:
            print(f"Timestamp: {timestamp}")
            if user:
                print(f"User: {user}")
            if command:
                print(f"Command: {command}")
            if action:
                print(f"Action: {action}")
            print("-" * 20)

# Function to extract information from a log line on Linux
def extract_info_linux(line):
    timestamp = None
    user = None
    command = None
    action = None

    # Example regex patterns - adjust based on actual log format
    timestamp_match = re.match(r'(\w{3} \d{2} \d{2}:\d{2}:\d{2})', line)
    if timestamp_match:
        timestamp = timestamp_match.group(1)

    user_match = re.search(r'user (\w+)', line)
    if user_match:
        user = user_match.group(1)

    command_match = re.search(r'command: (\S+)', line)
    if command_match:
        command = command_match.group(1)

    # Custom actions and alerts
    if 'sudo' in line:
        action = 'sudo command executed'
        if 'failed' in line:
            action = 'ALERT! Failed sudo command'
    elif 'su' in line:
        action = 'su command used'
    elif 'password changed' in line:
        action = 'Password changed'

    return timestamp, user, command, action

# Function to monitor user authentication changes for Linux
def monitor_authentication_changes_linux(log_file_path):
    with open(log_file_path, 'r') as file:
        logs = file.readlines()

    for line in logs:
        if 'useradd' in line:
            timestamp = extract_timestamp(line)
            print(f"New user added at {timestamp}")
        elif 'userdel' in line:
            timestamp = extract_timestamp(line)
            print(f"User deleted at {timestamp}")
        elif 'passwd' in line:
            timestamp = extract_timestamp(line)
            print(f"Password changed at {timestamp}")
        elif 'su' in line:
            print(f"su command used: {line.strip()}")
        elif 'sudo' in line:
            if 'failed' in line:
                print(f"ALERT! Failed sudo command: {line.strip()}")
            else:
                print(f"sudo command executed: {line.strip()}")

# Function to extract timestamp from log line on Linux
def extract_timestamp(line):
    timestamp_match = re.match(r'(\w{3} \d{2} \d{2}:\d{2}:\d{2})', line)
    if timestamp_match:
        return timestamp_match.group(1)
    return 'Timestamp not found'

# Function to parse relevant information on Windows using command outputs
def parse_log_windows():
    # Example command: net user
    print("Executing: net user")
    result = subprocess.run(["net", "user"], capture_output=True, text=True)
    print(result.stdout)

    # Example command: checking users in Administrators group
    print("Executing: net localgroup Administrators")
    result = subprocess.run(["net", "localgroup", "Administrators"], capture_output=True, text=True)
    print(result.stdout)

    # Example command: querying event logs for user actions (password changes, etc.)
    print("Executing: wevtutil qe Security /rd:true /f:text /c:5 /q:\"*[System[EventID=4723]]\"")
    result = subprocess.run(
        ["wevtutil", "qe", "Security", "/rd:true", "/f:text", "/c:5", "/q:*[System[EventID=4723]]"],
        capture_output=True, text=True
    )
    print(result.stdout)

# Determine OS and run appropriate functions in a loop
if __name__ == "__main__":
    current_os = platform.system()

    while True:
        if current_os == "Linux":
            print("Parsing Log File on Linux:")
            parse_log_linux(log_file_path)
            print("\nMonitoring Authentication Changes on Linux:")
            monitor_authentication_changes_linux(log_file_path)
        elif current_os == "Windows":
            print("Parsing Information on Windows:")
            parse_log_windows()
        else:
            print(f"Unsupported OS: {current_os}")

        print("Waiting for 5 seconds before next update...\n")
        time.sleep(5)  # Wait for 5 seconds before the next update
