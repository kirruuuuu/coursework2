import subprocess
import psutil
import socket
import time
import logging
import ctypes

# Configure logging
logging.basicConfig(filename="firewall_log.txt", level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

def is_admin():
    """Check if script is running as administrator."""
    return ctypes.windll.shell32.IsUserAnAdmin() != 0

if not is_admin():
    print("Please run this script as an administrator.")
    exit()

def list_firewall_rules():
    """Lists only important and user-enabled firewall rules."""
    try:
        result = subprocess.run(['netsh', 'advfirewall', 'firewall', 'show', 'rule', 'name=all'], 
                                capture_output=True, text=True, check=True)
        logging.info("Listed important and user-enabled firewall rules.")
        rules = result.stdout.split('\n')
        enabled_rules = []
        capture = False
        for line in rules:
            if "Rule Name:" in line:
                rule_name = line.strip()
                capture = False
            if "Enabled:" in line and "Yes" in line:
                capture = True
            if capture and ("Default" in rule_name or "User" in rule_name or "BlockIP_" in rule_name or "BlockPort_" in rule_name):
                enabled_rules.append(line)
            if line.strip() == "":
                capture = False
        print("\n".join(enabled_rules))
    except subprocess.CalledProcessError as e:
        logging.error(f"Error listing firewall rules: {e}")

def block_ip(ip_address):
    """Blocks a specific IP address with a unique rule name."""
    rule_name = f"BlockIP_{ip_address}"
    try:
        subprocess.run(['netsh', 'advfirewall', 'firewall', 'add', 'rule', 'name=' + rule_name, 'dir=in', 'action=block', 'remoteip=' + ip_address], check=True)
        logging.info(f"Blocked IP: {ip_address}")
        print(f"Blocked IP: {ip_address}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error blocking IP {ip_address}: {e}")

def unblock_ip(ip_address):
    """Unblocks a specific IP address."""
    rule_name = f"BlockIP_{ip_address}"
    try:
        subprocess.run(['netsh', 'advfirewall', 'firewall', 'delete', 'rule', 'name=' + rule_name], check=True)
        logging.info(f"Unblocked IP: {ip_address}")
        print(f"Unblocked IP: {ip_address}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error unblocking IP {ip_address}: {e}")

def list_active_connections():
    """Lists active network connections."""
    connections = psutil.net_connections()
    for conn in connections:
        try:
            laddr = f"{conn.laddr.ip}:{conn.laddr.port}"
            raddr = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A"
            print(f"Local Address: {laddr} -> Remote Address: {raddr} [Status: {conn.status}]")
        except Exception as e:
            logging.error(f"Error retrieving connection: {e}")

def scheduled_block(ip_address, duration):
    """Blocks an IP for a specified duration, then unblocks it."""
    block_ip(ip_address)
    time.sleep(duration)
    unblock_ip(ip_address)
    logging.info(f"Temporarily blocked {ip_address} for {duration} seconds.")

def menu():
    """Display menu options for the user."""
    print("\nFirewall Management Options:")
    print("1. List important and user-enabled firewall rules")
    print("2. Block an IP address")
    print("3. Unblock an IP address")
    print("4. List active network connections")
    print("5. Exit")

def main():
    """Main function to handle user input."""
    while True:
        menu()
        choice = input("Select an option (1-5): ")

        if choice == "1":
            list_firewall_rules()
        elif choice == "2":
            ip = input("Enter IP address to block: ")
            block_ip(ip)
        elif choice == "3":
            ip = input("Enter IP address to unblock: ")
            unblock_ip(ip)
        elif choice == "4":
            list_active_connections()
        elif choice == "5":
            print("Exiting firewall management script...")
            break
        else:
            print("Invalid option, please try again.")

if __name__ == "__main__":
    print("Firewall management script running...")
    main()