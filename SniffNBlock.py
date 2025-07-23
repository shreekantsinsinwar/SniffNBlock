# main.py

import tkinter as tk
from tkinter import ttk, messagebox
import psutil
import socket
import threading

THEME_BG = "#7f0909"  # Gryffindor red
THEME_FG = "gold"

class SniffNBlock:
    def __init__(self, root):
        self.root = root
        self.root.title("SniffNBlock - Suspicious Network Monitor")
        self.root.geometry("800x500")
        self.root.configure(bg=THEME_BG)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background=THEME_BG, foreground=THEME_FG, fieldbackground=THEME_BG)
        style.map('Treeview', background=[('selected', '#ffcc00')])

        self.tab_control = ttk.Notebook(root)
        self.tab_control.pack(fill='both', expand=True)

        self.create_monitor_tab()
        self.create_help_tab()

    def create_monitor_tab(self):
        tab = tk.Frame(self.tab_control, bg=THEME_BG)
        self.tab_control.add(tab, text="🔍 Monitor Connections")

        tk.Button(tab, text="Refresh Connections", command=self.refresh_connections, bg='gold').pack(pady=10)

        columns = ("PID", "Process", "Local IP", "Remote IP", "Port", "Status")
        self.tree = ttk.Treeview(tab, columns=columns, show="headings", height=15)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        self.tree.pack(fill="both", padx=10, pady=10, expand=True)

        tk.Button(tab, text="❌ Terminate Selected Connection", command=self.terminate_connection, bg="gold").pack(pady=5)

    def create_help_tab(self):
        tab = tk.Frame(self.tab_control, bg=THEME_BG)
        self.tab_control.add(tab, text="📖 How to Use")

        help_text = """
⚡ SniffNBlock - Suspicious Network Sniffer & Blocker

🟡 Features:
- Scans your system’s active TCP/UDP connections
- Flags foreign/suspicious IPs
- Lets you terminate suspicious PIDs from GUI

🔐 Caution:
- Only terminate processes you know!
- Some connections may be from legitimate apps (e.g., browsers)

🛡️ This tool is built for awareness, not aggression.
"""
        tk.Label(tab, text=help_text, fg=THEME_FG, bg=THEME_BG, justify="left", font=("Georgia", 11), wraplength=760).pack(padx=10, pady=10)

    def refresh_connections(self):
        self.tree.delete(*self.tree.get_children())
        conns = psutil.net_connections(kind='inet')

        for conn in conns:
            if conn.raddr:
                try:
                    pid = conn.pid or 0
                    proc_name = psutil.Process(pid).name() if pid else "N/A"
                    local_ip = conn.laddr.ip
                    remote_ip = conn.raddr.ip
                    remote_port = conn.raddr.port
                    status = conn.status
                    self.tree.insert("", "end", values=(pid, proc_name, local_ip, remote_ip, remote_port, status))
                except Exception:
                    continue

    def terminate_connection(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Info", "Please select a connection first.")
            return
        item = self.tree.item(selected[0])
        pid = item['values'][0]
        try:
            proc = psutil.Process(pid)
            proc.terminate()
            messagebox.showinfo("Terminated", f"Process {pid} terminated.")
            self.refresh_connections()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to terminate process {pid}: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = SniffNBlock(root)
    root.mainloop()
