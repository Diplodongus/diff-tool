import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox, ttk
import os
import webbrowser
from config_parser import read_config_file, get_config_files
from config_comparator import compare_with_golden
from html_generator import generate_html_diff

class ConfigComparisonGUI:
    def __init__(self, master):
        self.master = master
        master.title("Config Comparison Tool")
        master.geometry("800x650")  # Increased height to accommodate new row

        # Golden Config
        tk.Label(master, text="Golden Config:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.golden_path = tk.StringVar()
        tk.Entry(master, textvariable=self.golden_path, width=50).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(master, text="Browse", command=self.browse_golden).grid(row=0, column=2, padx=5, pady=5)

        # Device Config Folder
        tk.Label(master, text="Device Config Folder:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.device_folder = tk.StringVar()
        tk.Entry(master, textvariable=self.device_folder, width=50).grid(row=1, column=1, padx=5, pady=5)
        tk.Button(master, text="Browse", command=self.browse_device_folder).grid(row=1, column=2, padx=5, pady=5)

        # Output Folder
        tk.Label(master, text="Output Folder:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.output_folder = tk.StringVar()
        tk.Entry(master, textvariable=self.output_folder, width=50).grid(row=2, column=1, padx=5, pady=5)
        tk.Button(master, text="Browse", command=self.browse_output_folder).grid(row=2, column=2, padx=5, pady=5)

        # Compare Button
        tk.Button(master, text="Compare", command=self.compare_configs).grid(row=3, column=1, pady=10)

        # Open Diff in Browser Button
        tk.Button(master, text="Open Diff in Browser", command=self.open_diff_in_browser).grid(row=3, column=2, pady=10)

        # Progress Bar
        self.progress = ttk.Progressbar(master, orient="horizontal", length=300, mode="determinate")
        self.progress.grid(row=4, column=0, columnspan=3, pady=10)

        # Results Area
        self.results_area = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=80, height=25)
        self.results_area.grid(row=5, column=0, columnspan=3, padx=5, pady=5)

    def browse_golden(self):
        filename = filedialog.askopenfilename(filetypes=[("Config files", "*.cfg"), ("All files", "*.*")])
        self.golden_path.set(filename)

    def browse_device_folder(self):
        folder = filedialog.askdirectory()
        self.device_folder.set(folder)

    def browse_output_folder(self):
        folder = filedialog.askdirectory()
        self.output_folder.set(folder)

    def compare_configs(self):
        golden_path = self.golden_path.get()
        device_folder = self.device_folder.get()
        output_folder = self.output_folder.get()

        if not golden_path or not device_folder or not output_folder:
            messagebox.showerror("Error", "Please select golden config file, device config folder, and output folder.")
            return

        try:
            golden_config = read_config_file(golden_path)
            config_files = get_config_files(device_folder)

            total_files = sum(len(files) for files in config_files.values())
            self.progress["maximum"] = total_files
            self.progress["value"] = 0

            self.results_area.delete(1.0, tk.END)
            self.results_area.insert(tk.END, f"Comparing {total_files} files...\n\n")

            self.diff_files = []  # Store paths to diff HTML files

            for os_type, files in config_files.items():
                self.results_area.insert(tk.END, f"Processing {os_type} configs:\n")
                for file in files:
                    device_config = read_config_file(file)
                    diff = compare_with_golden(device_config, golden_config)
                    html_diff = generate_html_diff(diff, os.path.basename(file), os.path.basename(golden_path))

                    # Save HTML diff to a file
                    output_file = f"{os.path.splitext(os.path.basename(file))[0]}_vs_golden_diff.html"
                    output_path = os.path.join(output_folder, output_file)
                    os.makedirs(output_folder, exist_ok=True)
                    with open(output_path, 'w', encoding='utf-8') as f:
                        f.write(html_diff)

                    self.diff_files.append(output_path)

                    self.results_area.insert(tk.END, f"  {file}: Diff saved to {output_path}\n")
                    self.results_area.insert(tk.END, f"    Added lines: {sum(1 for d in diff if d[0] == 'extra')}\n")
                    self.results_area.insert(tk.END, f"    Removed lines: {sum(1 for d in diff if d[0] == 'missing')}\n")
                    self.results_area.insert(tk.END, f"    Modified lines: {sum(1 for d in diff if d[0] == 'modified')}\n\n")
                    
                    self.results_area.see(tk.END)
                    self.progress["value"] += 1
                    self.master.update_idletasks()

            self.results_area.insert(tk.END, "Comparison completed for all files.")
            messagebox.showinfo("Complete", "Comparison completed for all files.")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def open_diff_in_browser(self):
        if not hasattr(self, 'diff_files') or not self.diff_files:
            messagebox.showinfo("Info", "Please run a comparison first.")
            return

        file_path = filedialog.askopenfilename(
            initialdir=self.output_folder.get(),
            title="Select a diff file to view",
            filetypes=[("HTML files", "*.html"), ("All files", "*.*")]
        )

        if file_path:
            webbrowser.open(f'file://{os.path.abspath(file_path)}')
        else:
            messagebox.showinfo("Info", "No file selected.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ConfigComparisonGUI(root)
    root.mainloop()