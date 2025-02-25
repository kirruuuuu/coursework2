import subprocess
import psutil
import logging
import ctypes
import tkinter as tk
from tkinter import messagebox

# Configure logging
logging.basicConfig(filename="firewall_log.txt", level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

def is_admin():
    """Check if script is running as administrator."""
    return ctypes.windll.shell32.IsUserAnAdmin() != 0

if not is_admin():
    print("Please run this script as an administrator.")
    exit()

def block_ip(ip_address):
    """Blocks a specific IP address."""
    rule_name = f"BlockIP_{ip_address}"
    try:
        subprocess.run(['netsh', 'advfirewall', 'firewall', 'add', 'rule', 'name=' + rule_name, 'dir=in', 'action=block', 'remoteip=' + ip_address], check=True)
        logging.info(f"Blocked IP: {ip_address}")
        return f"Blocked IP: {ip_address}"
    except subprocess.CalledProcessError as e:
        logging.error(f"Error blocking IP {ip_address}: {e}")
        return f"Error blocking IP {ip_address}: {e}"

def unblock_ip(ip_address):
    """Unblocks a specific IP address."""
    rule_name = f"BlockIP_{ip_address}"
    try:
        subprocess.run(['netsh', 'advfirewall', 'firewall', 'delete', 'rule', 'name=' + rule_name], check=True)
        logging.info(f"Unblocked IP: {ip_address}")
        return f"Unblocked IP: {ip_address}"
    except subprocess.CalledProcessError as e:
        logging.error(f"Error unblocking IP {ip_address}: {e}")
        return f"Error unblocking IP {ip_address}: {e}"

class FirewallApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Firewall Management")
        self.root.geometry("400x300")

        # Title label
        self.label = tk.Label(self.root, text="Firewall Management", font=("Helvetica", 14))
        self.label.pack(pady=10)

        # Buttons
        self.block_button = tk.Button(self.root, text="Block IP Address", command=self.open_block_ip_window)
        self.block_button.pack(pady=5)

        self.unblock_button = tk.Button(self.root, text="Unblock IP Address", command=self.open_unblock_ip_window)
        self.unblock_button.pack(pady=5)

        self.exit_button = tk.Button(self.root, text="Exit", command=self.root.quit)
        self.exit_button.pack(pady=20)

    def open_block_ip_window(self):
        """Opens a new window to enter IP to block."""
        self.create_ip_entry_window("Block IP Address", block_ip)

    def open_unblock_ip_window(self):
        """Opens a new window to enter IP to unblock."""
        self.create_ip_entry_window("Unblock IP Address", unblock_ip)

    def create_ip_entry_window(self, title, action):
        """Creates a new pop-up window with an input field for IP address."""
        popup = tk.Toplevel(self.root)
        popup.title(title)
        popup.geometry("300x150")

        label = tk.Label(popup, text="Enter IP Address:")
        label.pack(pady=5)

        ip_entry = tk.Entry(popup)
        ip_entry.pack(pady=5)

        def on_submit():
            ip = ip_entry.get()
            if ip:
                result = action(ip)
                messagebox.showinfo(title, result)
                popup.destroy()

        submit_button = tk.Button(popup, text="Submit", command=on_submit)
        submit_button.pack(pady=10)

# Run the app
if __name__ == "__main__":
    print("Firewall management script running...")
    root = tk.Tk()
    app = FirewallApp(root)
    root.mainloop()
