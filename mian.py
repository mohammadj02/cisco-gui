import paramiko
import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime

# Establish connection to the router
def connect_to_router(hostname, port, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname, port, username, password)
    return client

# Execute command on the router
def execute_command(client, command):
    stdin, stdout, stderr = client.exec_command(command)
    return stdout.read().decode()

# Retrieve IP interface brief information
def get_ip_interface_brief(client):
    command = "show ip int brief"
    return execute_command(client, command)

# Retrieve ARP table
def get_running_config(client):
    command = "show arp"
    return execute_command(client, command)

# Retrieve running configuration interface
def get_running_config_interface(client):
    command = "show run interface"
    return execute_command(client, command)

# Retrieve running configuration VLAN
def get_running_config_vlan(client):
    command = "show run vlan"
    return execute_command(client, command)

# Retrieve IP routing table
def get_ip_route(client):
    command = "show ip route"
    return execute_command(client, command)

# Display the information in the GUI
def display_info(command_function):
    hostname = hostname_entry.get()
    port = int(port_entry.get())
    username = username_entry.get()
    password = password_entry.get()

    client = connect_to_router(hostname, port, username, password)
    info = command_function(client)
    client.close()

    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    output_text.config(state=tk.NORMAL)
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.INSERT, f"Time: {current_time}\n\n{info}")
    output_text.config(state=tk.DISABLED)

# Set up the GUI
root = tk.Tk()
root.title("Router Information")

# Styling
root.geometry("800x600")
root.configure(bg='#2c3e50')

# Labels and Entries
label_style = {'bg': '#2c3e50', 'fg': 'white', 'font': ('Arial', 12)}
entry_style = {'font': ('Arial', 12)}

tk.Label(root, text="Hostname:", **label_style).grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
hostname_entry = tk.Entry(root, **entry_style)
hostname_entry.grid(row=0, column=1, padx=10, pady=5, sticky=tk.EW)

tk.Label(root, text="Port:", **label_style).grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
port_entry = tk.Entry(root, **entry_style)
port_entry.grid(row=1, column=1, padx=10, pady=5, sticky=tk.EW)

tk.Label(root, text="Username:", **label_style).grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
username_entry = tk.Entry(root, **entry_style)
username_entry.grid(row=2, column=1, padx=10, pady=5, sticky=tk.EW)

tk.Label(root, text="Password:", **label_style).grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
password_entry = tk.Entry(root, show="*", **entry_style)
password_entry.grid(row=3, column=1, padx=10, pady=5, sticky=tk.EW)

# Buttons for commands
button_style = {'bg': '#3498db', 'fg': 'white', 'font': ('Arial', 12), 'activebackground': '#2980b9', 'activeforeground': 'white'}

tk.Button(root, text="Show IP Interface Brief", command=lambda: display_info(get_ip_interface_brief), **button_style).grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky=tk.EW)
tk.Button(root, text="Show ARP", command=lambda: display_info(get_running_config), **button_style).grid(row=5, column=0, columnspan=2, padx=10, pady=5, sticky=tk.EW)
tk.Button(root, text="Show Run Interface", command=lambda: display_info(get_running_config_interface), **button_style).grid(row=6, column=0, columnspan=2, padx=10, pady=5, sticky=tk.EW)
tk.Button(root, text="Show Run VLAN", command=lambda: display_info(get_running_config_vlan), **button_style).grid(row=7, column=0, columnspan=2, padx=10, pady=5, sticky=tk.EW)
tk.Button(root, text="Show IP Route", command=lambda: display_info(get_ip_route), **button_style).grid(row=8, column=0, columnspan=2, padx=10, pady=5, sticky=tk.EW)

# Output text area
output_text = scrolledtext.ScrolledText(root, width=80, height=20, state=tk.DISABLED, wrap=tk.WORD, font=('Arial', 12))
output_text.grid(row=9, column=0, columnspan=2, padx=10, pady=10, sticky=tk.NSEW)

# Make the columns expand
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(9, weight=1)

root.mainloop()
