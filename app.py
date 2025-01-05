import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import requests
from PIL import Image, ImageTk
import os
import time
from datetime import datetime
from bs4 import BeautifulSoup
from streaming import check_live_status  # 导入新的streaming模块

class StreamerApp:  # 修复这里的语法错误
    def __init__(self, root):
        self.root = root
        self.root.title("Live Stream Status Detector")
        self.root.geometry("500x600")
        
        # 初始化数据
        self.data_file = 'streamers.json'
        self.streamers = self.load_data()
        self.photos = []  # 存储图片引用
        
        # 创建主界面
        self.create_widgets()
        
        # 开始检测循环
        self.check_status()
    
    def load_data(self):
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
    
    def save_data(self):
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.streamers, f, ensure_ascii=False, indent=2)
    
    def create_widgets(self):
        # 创建工具栏
        toolbar = ttk.Frame(self.root)
        toolbar.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(toolbar, text="添加主播", command=self.add_streamer).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="刷新状态", command=self.refresh_streamers).pack(side=tk.LEFT, padx=5)
        
        # 创建主播列表框架
        self.streamer_frame = ttk.Frame(self.root)
        self.streamer_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 创建列表头
        columns = ['头像', '名称', '平台', '状态', '下次检测', '操作']
        for i, col in enumerate(columns):
            ttk.Label(self.streamer_frame, text=col).grid(row=0, column=i, padx=5, pady=5)
        
        self.refresh_streamers()
    
    def add_streamer(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("添加主播")
        dialog.geometry("400x300")
        
        tk.Label(dialog, text="名称:", anchor="w").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        name_entry = ttk.Entry(dialog, width=30)
        name_entry.grid(row=0, column=1, padx=5, pady=5)  # Fixed syntax error here
        
        # 平台
        tk.Label(dialog, text="平台:", anchor="w").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        platform_combo = ttk.Combobox(dialog, values=["SOOP"], state="readonly", width=28)
        platform_combo.grid(row=1, column=1, padx=5, pady=5)
        platform_combo.set("SOOP")  # 默认选择SOOP
        
        # 直播间链接
        tk.Label(dialog, text="直播间链接:", anchor="w").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        link_entry = ttk.Entry(dialog, width=30)
        link_entry.grid(row=2, column=1, padx=5, pady=5)
        
        # 当平台选择改变时的处理函数
        def on_platform_change(event):
            if platform_combo.get() == "SOOP":
                # 自动添加SOOP平台的基础URL
                link_text = link_entry.get()
                if not link_text.startswith("https://play.sooplive.co.kr/"):
                    link_entry.delete(0, tk.END)
                    link_entry.insert(0, "https://play.sooplive.co.kr/")
        
        platform_combo.bind("<<ComboboxSelected>>", on_platform_change)
        
        # 检测间隔
        tk.Label(dialog, text="检测间隔(分钟):", anchor="w").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        interval_entry = ttk.Entry(dialog, width=30)
        interval_entry.insert(0, "5")
        interval_entry.grid(row=3, column=1, padx=5, pady=5)
        
        # 头像
        tk.Label(dialog, text="头像:", anchor="w").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        avatar_path = tk.StringVar()
        avatar_entry = ttk.Entry(dialog, textvariable=avatar_path, width=30)
        avatar_entry.grid(row=4, column=1, padx=5, pady=5)
        tk.Button(dialog, text="浏览", 
                  command=lambda: self.select_avatar(avatar_path)).grid(row=4, column=2, padx=5, pady=5)

        # 保存按钮
        tk.Button(dialog, text="保存", 
                  command=lambda: self.save_new_streamer(
                      name_entry, platform_combo, link_entry, 
                      interval_entry, avatar_path, dialog)).grid(row=5, column=1, pady=10)

    def select_avatar(self, avatar_path):
        path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")])
        if path:
            avatar_path.set(path)  # Use set() for StringVar
    
    def save_new_streamer(self, name_entry, platform_combo, link_entry, interval_entry, avatar_path, dialog):
        name = name_entry.get().strip()
        platform = platform_combo.get()
        link = link_entry.get().strip()
        avatar = avatar_path.get().strip()
        
        try:
            interval = int(interval_entry.get())
        except ValueError:
            messagebox.showwarning("错误", "检测间隔必须是数字")
            return
            
        if name and platform and link and avatar and interval > 0:
            if platform == "SOOP" and not link.startswith("https://play.sooplive.co.kr/"):
                messagebox.showwarning("错误", "SOOP平台链接格式不正确")
                return
                
            self.streamers.append({
                "name": name,
                "platform": platform,
                "link": link,
                "avatar": avatar,
                "check_interval": interval,
                "last_check": 0,
                "status": "Unknown"
            })
            self.save_data()
            self.refresh_streamers()
            dialog.destroy()
        else:
            messagebox.showwarning("错误", "所有字段都必须填写，检测间隔必须大于0")
    
    def delete_streamer(self, index):
        if messagebox.askyesno("确认", "确定要删除这个主播吗？"):
            del self.streamers[index]
            self.save_data()
            self.refresh_streamers()
    
    def refresh_streamers(self):
        # 创建进度条窗口
        progress_window = tk.Toplevel(self.root)
        progress_window.title("正在刷新")
        progress_window.geometry("300x150")
        
        # 居中显示
        progress_window.transient(self.root)
        progress_window.grab_set()
        x = self.root.winfo_x() + (self.root.winfo_width() - 300) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - 150) // 2
        progress_window.geometry(f"+{x}+{y}")
        
        # 创建进度条
        progress_var = tk.DoubleVar()
        progress = ttk.Progressbar(progress_window, variable=progress_var, maximum=len(self.streamers))
        progress.pack(pady=20, padx=10, fill=tk.X)
        
        # 创建状态标签
        status_label = ttk.Label(progress_window, text="正在刷新中...")
        status_label.pack(pady=10)
        
        def update_progress(index, streamer):
            progress_var.set(index + 1)
            status_label.config(text=f"正在检查: {streamer['name']}")
            self.root.update()
        
        # 清理现有显示
        for widget in self.streamer_frame.winfo_children():
            widget.destroy()
        
        # 更新直播状态和UI
        for i, streamer in enumerate(self.streamers):
            try:
                update_progress(i, streamer)
                
                # 检查并显示头像
                avatar_image = Image.open(streamer["avatar"])
                avatar_image = avatar_image.resize((50, 50), Image.LANCZOS)
                
                # 实时检测直播状态
                status = check_live_status(streamer["link"])
                streamer["status"] = status  # 更新状态
                streamer["last_check"] = time.time()  # 更新检查时间
                
                # 仅当确认离线时转换为灰度图
                if status == "Offline":
                    avatar_image = avatar_image.convert('L')
                
                avatar_photo = ImageTk.PhotoImage(avatar_image)
                self.photos.append(avatar_photo)
                
                # 创建显示行
                ttk.Label(self.streamer_frame, image=avatar_photo).grid(row=i, column=0, padx=5, pady=5)
                ttk.Label(self.streamer_frame, text=streamer["name"]).grid(row=i, column=1, padx=5)
                ttk.Label(self.streamer_frame, text=streamer["platform"]).grid(row=i, column=2, padx=5)
                ttk.Label(self.streamer_frame, text=status).grid(row=i, column=3, padx=5)
                
                # 添加操作按钮
                ttk.Button(self.streamer_frame, text="编辑", 
                          command=lambda x=i: self.edit_streamer(x)).grid(row=i, column=4, padx=2)
                ttk.Button(self.streamer_frame, text="删除", 
                          command=lambda x=i: self.delete_streamer(x)).grid(row=i, column=5, padx=2)
                ttk.Button(self.streamer_frame, text="打开直播", 
                          command=lambda link=streamer["link"]: self.open_stream(link)).grid(row=i, column=6, padx=2)
                
            except Exception as e:
                print(f"Error processing streamer {streamer.get('name', '')}: {str(e)}")
        
        # 关闭进度窗口
        progress_window.destroy()
    
    def open_stream(self, link):
        try:
            import webbrowser
            webbrowser.open(link)
        except Exception as e:
            messagebox.showerror("Error", f"无法打开直播链接: {str(e)}")
    
    def check_status(self):
        if not self.streamers:  # 检查是否有主播
            self.root.after(300000, self.check_status)  # 如果没有主播，5分钟后再检查
            return
            
        current_time = time.time()
        for streamer in self.streamers:
            # 获取最新状态
            status = check_live_status(streamer["link"])
            # 更新状态和检查时间
            streamer["status"] = status
            streamer["last_check"] = current_time
        
        self.save_data()
        self.refresh_streamers()
        
        # 使用第一个主播的检查间隔或默认值
        check_interval = self.streamers[0].get("check_interval", 5) if self.streamers else 5
        # 设置定时检查
        self.root.after(int(check_interval * 60 * 1000), self.check_status)

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = StreamerApp(root)
        root.mainloop()
    except Exception as e:
        with open("error.log", "w") as f:
            f.write(str(e))