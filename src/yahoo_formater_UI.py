import random
import re
import requests
import tkinter as tk
from tkinter import filedialog, messagebox
import threading
from concurrent.futures import ThreadPoolExecutor

def load_proxies(proxy_file):
    with open(proxy_file, 'r') as file:
        proxies = [line.strip().split('|') for line in file]
    return proxies

def generate_user_agent():
    return "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0"

def test_proxy(proxy):
    ip, port, proxy_user, proxy_pass = proxy
    proxies = {
        "http": f"http://{proxy_user}:{proxy_pass}@{ip}:{port}",
        "https": f"https://{proxy_user}:{proxy_pass}@{ip}:{port}"
    }
    try:
        response = requests.get("http://www.google.com", proxies=proxies, timeout=5)
        return response.status_code == 200
    except:
        return False

def transform_line(line, proxy):
    parts = re.split(r'\s+', line.strip())
    if len(parts) < 2:
        return None
    email1, password = parts[0], parts[1]
    email2 = parts[2] if len(parts) > 2 else ""
    ip, port, proxy_user, proxy_pass = proxy[0], proxy[1], proxy[2], proxy[3]
    user_agent = generate_user_agent()
    return f"{email1}|{password}|{ip}|{port}|{proxy_user}|{proxy_pass}|{user_agent}|{email2}"

def transform_file(input_text, output_text, proxy_file, progress_text):
    proxies = load_proxies(proxy_file)
    proxy_index = 0
    lines = input_text.get("1.0", tk.END).strip().split('\n')
    total_lines = len(lines)
    processed_lines = 0

    def process_line(line):
        nonlocal proxy_index
        while not test_proxy(proxies[proxy_index]):
            proxy_index = (proxy_index + 1) % len(proxies)
        proxy = proxies[proxy_index]
        transformed_line = transform_line(line, proxy)
        proxy_index = (proxy_index + 1) % len(proxies)
        return transformed_line

    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(process_line, lines))
        for result in results:
            if result:
                output_text.insert(tk.END, result + '\n')
            processed_lines += 1
            progress_text.insert(tk.END, f"Processed {processed_lines}/{total_lines} lines\n")
            progress_text.see(tk.END)

    progress_text.insert(tk.END, "Processing complete.\n")
    messagebox.showinfo("Success", "Transformation complete.")

def select_proxy_file():
    proxy_file.set(filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")]))

def run_transformation():
    if not proxy_file.get():
        messagebox.showerror("Error", "Please select a proxy file.")
        return
    progress_text.delete(1.0, tk.END)
    output_text.delete(1.0, tk.END)
    threading.Thread(target=transform_file, args=(input_text, output_text, proxy_file.get(), progress_text)).start()
    messagebox.showinfo("Success", "Transformation started. Check the progress below.")

# Create the main window
root = tk.Tk()
root.title("Yahoo Formatter")

# Create StringVar variable to hold proxy file path
proxy_file = tk.StringVar()

# Create and place widgets
tk.Label(root, text="Proxy File:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
tk.Entry(root, textvariable=proxy_file, width=50).grid(row=0, column=1, padx=10, pady=5)
tk.Button(root, text="Browse...", command=select_proxy_file).grid(row=0, column=2, padx=10, pady=5)

tk.Label(root, text="Input:").grid(row=1, column=0, padx=10, pady=5, sticky="ne")
input_text = tk.Text(root, height=10, width=80)
input_text.grid(row=1, column=1, columnspan=2, padx=10, pady=5)

tk.Label(root, text="Output:").grid(row=2, column=0, padx=10, pady=5, sticky="ne")
output_text = tk.Text(root, height=10, width=80)
output_text.grid(row=2, column=1, columnspan=2, padx=10, pady=5)

tk.Button(root, text="Run", command=run_transformation).grid(row=3, column=0, columnspan=3, pady=10)

# Create a Text widget for displaying progress
progress_text = tk.Text(root, height=10, width=80)
progress_text.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

# Start the main event loop
root.mainloop()