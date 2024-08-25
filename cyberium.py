import os
import platform
import socket
import shutil
import requests
import time
from collections import defaultdict

# this will get OS info
def os_info():
    return f"{platform.system()} {platform.release()}"

# Network info
def network_info():
    try:
        public_ip = requests.get('https://api.ipify.org').text #this api helps in fetching the public ip of the device
    except:
        public_ip = "Unavailable"
    return socket.gethostname(), socket.gethostbyname(socket.gethostname()), public_ip

# this helps in finding Disk space
def disk_space(path='/'):
    total, used, free = shutil.disk_usage(path)
    return total, used, free

# the function helps Largest folders
def large_dirs(root='C:/', count=5):
    sizes = defaultdict(int)
    for dirpath, _, filenames in os.walk(root):
        for f in filenames:
            try:
                fp = os.path.join(dirpath, f)
                if os.path.exists(fp):  # Ensure the file exists
                    sizes[dirpath] += os.path.getsize(fp)
            except Exception as e:
                # Catch all exceptions to avoid breaking the loop
                print(f"Error processing file {fp}: {e}")
                pass
    return sorted(sizes.items(), key=lambda x: x[1], reverse=True)[:count]

# this function helps in seeing the CPU usage
def cpu_usage():
    if platform.system() == "Windows":
        return os.popen("wmic cpu get loadpercentage").read().split("\n")[1]
    else:
        return os.popen("top -bn1 | grep 'Cpu(s)'").read().split('%')[0].split()[-1]

#this is  Main function
def main():
    while True:
        print(f"OS: {os_info()}\n")

        hostname, private_ip, public_ip = network_info()
        print(f"Hostname: {hostname}")
        print(f"Private IP: {private_ip}")
        print(f"Public IP: {public_ip}\n")

        total, used, free = disk_space()
        print(f"Total Disk: {total / (1024**3):.2f} GB")
        print(f"Used Disk: {used / (1024**3):.2f} GB")
        print(f"Free Disk: {free / (1024**3):.2f} GB\n")

        print("Largest Folders:")
        for dir_path, size in large_dirs():
            print(f"{dir_path}: {size / (1024**3):.2f} GB")
        print()

        print(f"CPU Usage: {cpu_usage()}%\n")

        time.sleep(30)

if __name__ == "__main__":
    main()
