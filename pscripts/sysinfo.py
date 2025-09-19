#!/usr/bin/python3

import os
import subprocess

def check_package(package):
    try:
        subprocess.check_output(["which", package])
    except subprocess.CalledProcessError:
        print(f"\nError: Either \"{package}\" command is not available or \"{package}\" package is not properly installed. Please ensure this package is installed and working correctly, then run this script.\n\n")
        exit(1)

def print_system_info():
    S = "=" * 30
    D = "-" * 30

    print(f"{S} System Info Status Report {S}")
    print("\nOperating System Details")
    print(D)
    print(f"Hostname: {os.uname()[1]}")

    if os.path.exists("/usr/bin/lsb_release"):
        os_info = subprocess.check_output(["lsb_release", "-d"]).decode().split(":")[1].strip()
    else:
        os_info = open("/etc/system-release").read().strip()

    print(f"Operating System: {os_info}")
    print(f"Kernel Version: {os.uname()[2]}")
    print(f"OS Architecture: {'64 Bit OS' if 'x86_64' in os.uname() else '32 Bit OS'}")

def main():
    check_package("mpstat")
    print_system_info()

if __name__ == "__main__":
    main()
