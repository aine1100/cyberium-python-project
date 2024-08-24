import re
from datetime import datetime

# Define the path to the log file
log_file_path = '/var/log/auth.log'

# Function to parse the log file and extract relevant information
def parse_log(log_file_path):
    with open(log_file_path, 'r') as file:
        logs = file.readlines()

    for line in logs:
        timestamp, user, command, action = extract_info(line)
        if timestamp:
            print(f"Timestamp: {timestamp}")
            if user:
                print(f"User: {user}")
            if command:
                print(f"Command: {command}")
            if action:
                print(f"Action: {action}")
            print("-" * 20)

# Function to extract information from a log line
def extract_info(line):
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

# Function to monitor user authentication changes
def monitor_authentication_changes(log_file_path):
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

# Function to extract timestamp from log line
def extract_timestamp(line):
    timestamp_match = re.match(r'(\w{3} \d{2} \d{2}:\d{2}:\d{2})', line)
    if timestamp_match:
        return timestamp_match.group(1)
    return 'Timestamp not found'

# Run the parsing and monitoring functions
if __name__ == "__main__":
    print("Parsing Log File:")
    parse_log(log_file_path)

    print("\nMonitoring Authentication Changes:")
    monitor_authentication_changes(log_file_path)
