import tkinter as tk
from tkinter import messagebox
import time
import threading


# 进程控制块（PCB）
class Process:
    def __init__(self, pid, name, burst_time):
        self.pid = pid  # 进程ID
        self.name = name  # 进程名称
        self.burst_time = burst_time  # 运行所需时间
        self.status = "Ready"  # 初始状态为就绪


# 进程管理模块
class FCFS_Scheduler:
    def __init__(self):
        self.queue = []  # 进程队列
        self.running_process = None  # 当前正在运行的进程
        self.pid_counter = 1  # 自动生成进程ID

    def create_process(self, name, burst_time):
        process = Process(self.pid_counter, name, burst_time)
        self.queue.append(process)
        self.pid_counter += 1
        return process

    def run_all_processes(self):
        # 运行队列中的所有进程
        if not self.queue:
            return "没有等待的进程！"
        for process in self.queue:
            process.status = "Running"
            self.run_process(process)
            # 执行完后从队列中移除
            self.queue.remove(process)
        return "所有进程已执行完毕！"


# GUI 界面
class ProcessManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FCFS 进程管理模块")
        self.scheduler = FCFS_Scheduler()

        # 界面元素
        self.setup_ui()

    def setup_ui(self):
        # 左侧：创建进程
        frame_create = tk.Frame(self.root)
        frame_create.pack(side=tk.LEFT, padx=10, pady=10)

        tk.Label(frame_create, text="进程名称:").pack()
        self.entry_name = tk.Entry(frame_create)
        self.entry_name.pack()

        tk.Label(frame_create, text="运行时间:").pack()
        self.entry_time = tk.Entry(frame_create)
        self.entry_time.pack()

        self.btn_create = tk.Button(frame_create, text="创建进程", command=self.create_process)
        self.btn_create.pack(pady=10)

        self.btn_run = tk.Button(frame_create, text="运行进程队列", command=self.run_all_processes)
        self.btn_run.pack(pady=10)

        # 中间：进程队列
        frame_queue = tk.Frame(self.root)
        frame_queue.pack(side=tk.LEFT, padx=10, pady=10)

        tk.Label(frame_queue, text="进程队列").pack()
        self.text_queue = tk.Text(frame_queue, height=15, width=30)
        self.text_queue.pack()

        # 右侧：运行状态
        frame_status = tk.Frame(self.root)
        frame_status.pack(side=tk.LEFT, padx=10, pady=10)

        tk.Label(frame_status, text="当前运行的进程").pack()
        self.label_status = tk.Label(frame_status, text="无", fg="blue")
        self.label_status.pack(pady=10)

    def create_process(self):
        name = self.entry_name.get()
        burst_time = self.entry_time.get()

        if not name or not burst_time.isdigit():
            messagebox.showerror("输入错误", "请输入有效的进程名称和运行时间（数字）")
            return

        process = self.scheduler.create_process(name, int(burst_time))
        self.update_queue_display()
        messagebox.showinfo("进程创建成功", f"进程 {name} 已创建 (PID: {process.pid})")

    def run_all_processes(self):
        if not self.scheduler.queue:
            messagebox.showinfo("提示", "当前没有等待的进程！")
            self.label_status.config(text="无")
            return

        self.label_status.config(text="进程开始运行...")

        # 模拟运行队列中的所有进程
        threading.Thread(target=self.run_processes, daemon=True).start()

    def run_processes(self):
        # 依次执行队列中的所有进程
        while self.scheduler.queue:
            process = self.scheduler.queue[0]  # 获取队列中的第一个进程
            self.label_status.config(text=f"正在运行：{process.name} (PID: {process.pid})")
            self.run_process(process)
            self.scheduler.queue.remove(process)  # 运行完毕后从队列中移除
        self.label_status.config(text="所有进程完成！")
        self.update_queue_display()

    def run_process(self, process):
        for i in range(process.burst_time):
            time.sleep(1)  # 模拟1秒运行
            self.label_status.config(text=f"正在运行：{process.name} (剩余 {process.burst_time - i - 1} 秒)")

    def update_queue_display(self):
        self.text_queue.delete(1.0, tk.END)
        if not self.scheduler.queue:
            self.text_queue.insert(tk.END, "队列为空\n")
        for process in self.scheduler.queue:
            self.text_queue.insert(tk.END, f"PID: {process.pid}, 名称: {process.name}, 状态: {process.status}\n")


# 主程序入口
if __name__ == "__main__":
    root = tk.Tk()
    app = ProcessManagerApp(root)
    root.mainloop()
