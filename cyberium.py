import os
import platform
import socket
import shutil
import requests
import time
from collections import defaultdict
from operator import itemgetter

# Function to get OS details
def get_os_details():
    os_name = platform.system()
    os_version = platform.version()
    os_release = platform.release()
    return f"{os_name} {os_version} ({os_release})"

# Function to get network details
def get_network_details():
    hostname = socket.gethostname()
    private_ip = socket.gethostbyname(hostname)
    
    try:
        public_ip = requests.get('https://api.ipify.org').text
    except requests.RequestException as e:
        public_ip = f"Failed to retrieve public IP address: {e}"

    return hostname, private_ip, public_ip

# Function to get disk usage statistics
def get_disk_usage(path='/'):
    total, used, free = shutil.disk_usage(path)
    return total, used, free

# Function to find the largest directories
def get_largest_directories(root_dir='C:/', num_dirs=5):
    dir_sizes = defaultdict(int)

    for dirpath, dirnames, filenames in os.walk(root_dir):
        for f in filenames:
            try:
                fp = os.path.join(dirpath, f)
                dir_sizes[dirpath] += os.path.getsize(fp)
            except FileNotFoundError:
                pass

    largest_dirs = sorted(dir_sizes.items(), key=itemgetter(1), reverse=True)[:num_dirs]
    return largest_dirs

# Function to monitor CPU usage
def monitor_cpu_usage():
    if platform.system() == "Windows":
        cpu_usage = os.popen("wmic cpu get loadpercentage").read().strip().split("\n")[1]
    else:
        cpu_usage = os.popen("top -bn1 | grep 'Cpu(s)'").read().split('%')[0].split()[-1]
    return cpu_usage

# Main function to gather and display system information
def main():
    while True:
        # Display OS details
        os_details = get_os_details()
        print(f"Operating System: {os_details}\n")

        # Display network details
        hostname, private_ip, public_ip = get_network_details()
        print(f"Hostname: {hostname}")
        print(f"Private IP Address: {private_ip}")
        print(f"Public IP Address: {public_ip}\n")

        # Display disk usage statistics
        total, used, free = get_disk_usage()
        print(f"Total Disk Space: {total / (1024**3):.2f} GB")
        print(f"Used Disk Space: {used / (1024**3):.2f} GB")
        print(f"Free Disk Space: {free / (1024**3):.2f} GB\n")

        # Display largest directories
        largest_dirs = get_largest_directories()
        print("Top 5 Largest Directories:")
        for dir_path, size in largest_dirs:
            print(f"{dir_path}: {size / (1024**3):.2f} GB")
        print()

        # Display CPU usage
        cpu_usage = monitor_cpu_usage()
        print(f"CPU Usage: {cpu_usage}%\n")

        # Wait for 30 seconds before updating the information
        time.sleep(30)

# Run the main function
if __name__ == "__main__":
    main()
