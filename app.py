import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
import time
import subprocess
import logging

logging.basicConfig(
    level=logging.DEBUG,
    filename='app.log',
    filemode='w',
    format='%(asctime)s [%(levelname)s] %(name)s - %(message)s'
)

class StreamerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Stream Recorder")
        self.root.geometry("500x350")
        
        logging.info("Initializing StreamerApp...")

        self.config_file = 'config.json'
        self.config = self.load_config()
        
        # 读取或初始化“recent_links”和“past_records”
        if "recent_links" not in self.config:
            self.config["recent_links"] = []
        if "past_records" not in self.config:
            self.config["past_records"] = []

        self.save_config()
        self.create_widgets()

    def load_config(self):
        """加载配置文件，若无则返回空字典。"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    logging.info("Loaded config from file.")
                    return config
            except Exception as e:
                logging.error("Failed to load config: %s", str(e))
        return {}

    def save_config(self):
        """保存配置信息到 config.json。"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
            logging.info("Config saved successfully.")
        except Exception as e:
            logging.error(f"保存配置失败: {str(e)}")

    def create_widgets(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # 关于我
        about_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="关于我", menu=about_menu)
        about_menu.add_command(label="关于作者", command=self.show_about)

        # 记录菜单
        record_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="记录", menu=record_menu)
        record_menu.add_command(label="查看历史记录", command=self.show_records)

        tk.Label(self.root, text="推流链接:").pack(pady=5)
        self.link_var = tk.StringVar()
        self.link_combo = ttk.Combobox(self.root, textvariable=self.link_var, width=45)
        self.link_combo['values'] = self.config["recent_links"]
        self.link_combo.pack(pady=5)

        tk.Label(self.root, text="保存格式:").pack(pady=5)
        self.format_var = tk.StringVar(value="ts")
        format_combo = ttk.Combobox(self.root, textvariable=self.format_var, values=["ts", "mp4"], width=10)
        format_combo.pack(pady=5)

        tk.Label(self.root, text="保存到文件夹:").pack(pady=5)
        last_dir = self.config.get('last_record_dir', os.getcwd())
        self.output_dir_var = tk.StringVar(value=last_dir)

        dir_frame = ttk.Frame(self.root)
        dir_frame.pack(pady=5)
        dir_entry = ttk.Entry(dir_frame, textvariable=self.output_dir_var, width=30)
        dir_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(dir_frame, text="浏览", command=self.select_dir).pack(side=tk.LEFT, padx=5)

        ttk.Button(self.root, text="开始录制", command=self.start_record).pack(pady=15)

    def select_dir(self):
        selected = filedialog.askdirectory()
        if selected:
            self.output_dir_var.set(selected)

    def start_record(self):
        link = self.link_var.get().strip()
        output_dir = self.output_dir_var.get().strip()
        suffix = self.format_var.get()

        if not link:
            messagebox.showerror("错误", "请输入推流链接")
            return
        if not os.path.isdir(output_dir):
            messagebox.showerror("错误", "请选择有效的文件夹")
            return

        # 记录推流链接到recent_links
        if link and link not in self.config["recent_links"]:
            self.config["recent_links"].insert(0, link)  # 最近用的放在最前面
            self.config["recent_links"] = self.config["recent_links"][:10]

        self.config['last_record_dir'] = output_dir
        self.save_config()

        # 生成带时间戳的输出文件名
        time_str = time.strftime("%Y_%m_%d_%H_%M_%S")
        output_name = f"{time_str}_88output.{suffix}"
        output_path = os.path.join(output_dir, output_name)

        # mp4或ts
        if suffix == "ts":
            cmd = f'ffmpeg -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -i "{link}" -c copy "{output_path}"'
        else:
            cmd = f'ffmpeg -i "{link}" -c copy -timeout 10000000 -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 "{output_path}"'

        # 使用 /c 使录制结束后关闭命令行
        subprocess.Popen(f'start cmd /c {cmd}', shell=True)

        # 添加记录
        new_record = {
            "time": time_str,
            "file": output_path,
            "link": link,
            "suffix": suffix,
        }
        self.config["past_records"].append(new_record)
        self.save_config()

    def show_records(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("历史录制记录")
        dialog.geometry("500x300")

        columns = ("time", "file", "link")
        tree = ttk.Treeview(dialog, columns=columns, show='headings')
        tree.heading("time", text="时间")
        tree.heading("file", text="输出文件")
        tree.heading("link", text="推流链接")
        tree.column("time", width=100)
        tree.column("file", width=250)
        tree.column("link", width=120)
        tree.pack(fill=tk.BOTH, expand=True)

        for rec in self.config.get("past_records", []):
            tree.insert("", tk.END, values=(rec.get("time"), rec.get("file"), rec.get("link")))

        menu = tk.Menu(tree, tearoff=0)

        def open_folder():
            sel = tree.selection()
            if sel:
                item = tree.item(sel[0])["values"]
                file_path = item[1]
                folder_path = os.path.dirname(file_path).replace('/', '\\')
                if os.path.exists(folder_path):
                    subprocess.Popen(["explorer", f"/select,{file_path.replace('/', '\\')}"])

        def clear_records():
            self.config["past_records"] = []
            self.save_config()
            for child in tree.get_children():
                tree.delete(child)

        menu.add_command(label="打开文件夹", command=open_folder)

        def do_popup(event):
            row_id = tree.identify_row(event.y)
            menu.delete(0, tk.END)
            if row_id:
                # 如果点击到一条记录
                tree.selection_set(row_id)
                menu.add_command(label="打开文件夹", command=open_folder)
            else:
                # 空白区域提供"清除记录"功能
                menu.add_command(label="清除记录", command=clear_records)
            menu.post(event.x_root, event.y_root)

        tree.bind("<Button-3>", do_popup)

    def show_about(self):
        about_dialog = tk.Toplevel(self.root)
        about_dialog.title("关于作者")
        about_dialog.geometry("300x300")

        info_frame = ttk.Frame(about_dialog)
        info_frame.pack(expand=True, fill='both', padx=20, pady=20)

        ttk.Label(info_frame, text="作者: Lanlic Yuen", font=('Arial', 10)).pack(pady=5)
        ttk.Label(info_frame, text="个人研究开发", font=('Arial', 10)).pack(pady=5)
        ttk.Label(info_frame, text="联系方式: lanlic@hotmail.com", font=('Arial', 10)).pack(pady=5)
        ttk.Label(info_frame, text="版本: v1.1", font=('Arial', 10)).pack(pady=5)

        ttk.Button(about_dialog, text="关闭", command=about_dialog.destroy).pack(pady=10)

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = StreamerApp(root)
        root.mainloop()
    except Exception as e:
        logging.error(f"Application failed to start: {str(e)}")
        messagebox.showerror("错误", f"程序启动失败: {str(e)}")