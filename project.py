import re
import subprocess
import platform
import time

user_log_file = '/var/log/auth.log'
#this function helps in getting info in the log file
def log_reader(user_log_file):
    with open(user_log_file, 'r') as file:
        logs = file.readlines()

    for line in logs:
        timestamp, user, command, action = linux_information(line)
        if timestamp:
            print(f"Timestamp: {timestamp}")#this gets the info about the timestamp
            if user:
                print(f"User: {user}")#this gets info about the user
            if command:
                print(f"Command: {command}")#this gets the command user
            if action:
                print(f"Action: {action}")
            print("-" * 20)

def linux_information(line):
    timestamp = None
    user = None
    command = None
    action = None

    # this is just seeing if the timestamp just meets
    timestamp_match = re.match(r'(\w{3} \d{2} \d{2}:\d{2}:\d{2})', line)
    if timestamp_match:
        timestamp = timestamp_match.group(1)

    user_match = re.search(r'user (\w+)', line)
    if user_match:
        user = user_match.group(1)

    command_match = re.search(r'command: (\S+)', line)
    if command_match:
        command = command_match.group(1)

    if 'sudo' in line:
        action = 'sudo command has been used perfectly'
        if 'failed' in line:
            action = 'ALERT! Failed to run sudo command'
    elif 'su' in line:
        action = 'su command has been used'
    elif 'password changed' in line:
        action = 'Password is changed'

    return timestamp, user, command, action

def authentication_linux(user_log_file):
    with open(user_log_file, 'r') as file:
        logs = file.readlines()

    for line in logs:
        timestamp = get_timestamp(line)
        if 'useradd' in line:
            print(f"New user added at {timestamp}")
        elif 'userdel' in line:
            print(f"User deleted at {timestamp}")
        elif 'passwd' in line:
            print(f"Password changed at {timestamp}")
        elif 'su' in line:
            print(f"su command used at {timestamp}: {line.strip()}")
        elif 'sudo' in line:
            if 'failed' in line:
                print(f"ALERT! Failed sudo command at {timestamp}: {line.strip()}")
            else:
                print(f"sudo command executed at {timestamp}: {line.strip()}")

def get_timestamp(line):
    timestamp_match = re.match(r'(\w{3} \d{2} \d{2}:\d{2}:\d{2})', line)
    if timestamp_match:
        return timestamp_match.group(1)
    return 'Timestamp not found'
#this is extracting the user info from windows
def log_windows():
    print("Working: net user")
    result = subprocess.run(["net", "user"], capture_output=True, text=True)
    print(result.stdout)

    print("Working: net localgroup Administrators")
    result = subprocess.run(["net", "localgroup", "Administrators"], capture_output=True, text=True)
    print(result.stdout)

    print("Working: wevtutil qe Security /rd:true /f:text /c:5 /q:\"*[System[EventID=4723]]\"")
    result = subprocess.run(
        ["wevtutil", "qe", "Security", "/rd:true", "/f:text", "/c:5", "/q:*[System[EventID=4723]]"],
        capture_output=True, text=True
    )
    print(result.stdout)

    print("\nSimulated Timestamps for Windows Events:")
    print("Timestamp: Simulated Timestamp")
#this main function just guess wether its for windows and then it performs its task and if its for linux it also gives information about linux
if __name__ == "__main__":
    current_os = platform.system()

    while True:
        if current_os == "Linux":
            print("Opening Log File on Linux:")
            log_reader(user_log_file)
            print("\nMonitoring Authentication Changes on Linux:")
            authentication_linux(user_log_file)
        elif current_os == "Windows":
            print("Parsing Information on Windows:")
            log_windows()
        else:
            print(f"Unsupported OS: {current_os}")

        print("Waiting for 5 seconds before next update...\n")
        time.sleep(5)
