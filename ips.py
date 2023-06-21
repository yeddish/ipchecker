import tkinter as tk
import socket
import psutil
import requests
import tkinter.ttk as ttk
import threading

def get_local_ips():
    local_ips = []
    for iface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family == socket.AF_INET:
                local_ips.append((iface, addr.address))
    return local_ips

def get_external_ip():
    try:
        return requests.get('https://api.ipify.org').text
    except:
        return "Failed to get external IP. Check your internet connection."

def update_external_ip():
    external_ip = get_external_ip()

    # Clear the existing text
    ext_ip_text_widget.delete("1.0", tk.END)
    ext_ip_text_widget.insert(tk.END, f"External IP: {external_ip}\n")

def update_local_ips():
    local_ips = get_local_ips()

    local_ips_text_widget.delete("1.0", tk.END)
    local_ips_text_widget.insert(tk.END, "Interface IPs:\n")
    for iface, ip in local_ips:
        if checkboxes[iface].get():
            local_ips_text_widget.insert(tk.END, f"{iface}: {ip}\n")

def threaded_update_external_ip():
    threading.Thread(target=update_external_ip).start()

def threaded_update_local_ips():
    threading.Thread(target=update_local_ips).start()

root = tk.Tk()
root.title("IP Addresses")
root.geometry("300x800")

ext_ip_text_widget = tk.Text(root, wrap='word', height=1)
ext_ip_text_widget.pack(expand=0, fill='x')

update_ext_ip_button = tk.Button(root, text="Update External IP", command=threaded_update_external_ip, height=3)
update_ext_ip_button.pack()

local_ips_text_widget = tk.Text(root, wrap='word')
local_ips_text_widget.pack(expand=1, fill='both')

update_local_ips_button = tk.Button(root, text="Update Local IPs", command=threaded_update_local_ips, height=3)
update_local_ips_button.pack()

checkboxes = {}
for iface, _ in get_local_ips():
    var = tk.IntVar(value=0)  # Default checkboxes to checked
    checkboxes[iface] = var
    cb = ttk.Checkbutton(root, text=iface, variable=var, onvalue=1, offvalue=0)
    cb.pack()

root.mainloop()
