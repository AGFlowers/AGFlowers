#!/usr/bin/python3
"""
healthchk.py
Author: Alex Flowers (converted to Python)
Purpose: Quickly check and report health status of Linux systems
"""

import platform
import subprocess
import sys
import os
import socket
from datetime import datetime

# -----------------------------------------------------------------
def run_cmd(cmd):
    """Run a shell command and return stdout"""
    try:
        result = subprocess.run(cmd, shell=True, check=True,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                universal_newlines=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Error running {cmd}: {e.stderr.strip()}"

# -----------------------------------------------------------------
def os_details():
    """Detect OS, kernel, architecture"""
    print("\n=== Operating System Details ===")
    print(f"Hostname           : {socket.getfqdn()}")
    if os.path.exists("/etc/os-release"):
        os_info = run_cmd("grep PRETTY_NAME /etc/os-release | cut -d= -f2 | tr -d '\"'")
        print(f"Operating System   : {os_info}")
    else:
        print(f"Operating System   : {platform.system()} {platform.release()}")
    print(f"Kernel Version     : {platform.release()}")
    print(f"OS Architecture    : {platform.machine()}")

# -----------------------------------------------------------------
def uptime():
    print("\n=== System Uptime ===")
    print(run_cmd("uptime"))

# -----------------------------------------------------------------
def filesystem_usage():
    print("\n=== Filesystem Usage ===")
    print(run_cmd("df -PTh | egrep -iw 'ext4|ext3|xfs|gfs|gfs2|btrfs'"))

# -----------------------------------------------------------------
def inode_usage():
    print("\n=== Inode Usage ===")
    print(run_cmd("df -PThi | egrep -iw 'ext4|ext3|xfs|gfs|gfs2|btrfs'"))

# -----------------------------------------------------------------
def zombie_processes():
    print("\n=== Zombie Processes ===")
    zombies = run_cmd("ps -eo stat | grep -w Z | wc -l")
    if zombies.isdigit() and int(zombies) > 0:
        print(f"Number of zombies: {zombies}")
        print(run_cmd("ps -eo pid,ppid,user,stat,args | grep ' Z'"))
    else:
        print("No zombie processes found.")

# -----------------------------------------------------------------
def memory_usage():
    print("\n=== Memory Usage ===")
    print(run_cmd("free -h"))

# -----------------------------------------------------------------
def cpu_usage():
    print("\n=== CPU / Processor Info ===")
    print(run_cmd("lscpu"))
    print("\n--- mpstat output ---")
    print(run_cmd("mpstat | tail -2"))

# -----------------------------------------------------------------
def load_average():
    print("\n=== Load Average ===")
    print(run_cmd("uptime | grep -o 'load average.*'"))

# -----------------------------------------------------------------
def recent_events():
    print("\n=== Recent Reboots ===")
    print(run_cmd("last -x | grep reboot | head -3 || echo 'No reboot events found.'"))
    print("\n=== Recent Shutdowns ===")
    print(run_cmd("last -x | grep shutdown | head -3 || echo 'No shutdown events found.'"))

# -----------------------------------------------------------------
def top_processes():
    print("\n=== Top 5 Memory Hogs ===")
    print(run_cmd("ps -eo pmem,pcpu,pid,ppid,user,stat,args | sort -k 1 -r | head -6"))
    print("\n=== Top 5 CPU Hogs ===")
    print(run_cmd("ps -eo pcpu,pmem,pid,ppid,user,stat,args | sort -k 1 -r | head -6"))

# -----------------------------------------------------------------
def health_check():
    print("\n" + "*" * 40 + " Health Check Report " + "*" * 40)
    os_details()
    uptime()
    filesystem_usage()
    inode_usage()
    zombie_processes()
    memory_usage()
    cpu_usage()
    load_average()
    recent_events()
    top_processes()
    print("\n" + "*" * 100 + "\n")

# -----------------------------------------------------------------
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "-f":
        if len(sys.argv) < 3:
            print("Usage: ./healthchk.py -f serverlist.txt")
            sys.exit(1)
        with open(sys.argv[2], "r") as f:
            servers = [line.strip() for line in f if line.strip()]
        for server in servers:
            print(f"\n\n### Running health check on {server} ###")
            os.system(f"ssh {server} 'python3 - <<EOF\n{open(__file__).read()}\nEOF'")
    else:
        health_check()

