import tkinter as tk

# 创建主窗口
root = tk.Tk()
root.title("主页面")
root.geometry("600x400")  # 增大窗口的大小

# 定义按钮的回调函数
def on_button_click(button_name):
    print(f"按钮 {button_name} 被点击了")

# 创建四个按钮，并使用 grid 布局排列
button1 = tk.Button(root, text="进程管理模块", command=lambda: on_button_click("进程管理模块"), font=("Arial", 14), height=2)
button1.grid(row=0, column=0, padx=20, pady=20, sticky="ew")

button2 = tk.Button(root, text="存贮器管理模块", command=lambda: on_button_click("存贮器管理模块"), font=("Arial", 14), height=2)
button2.grid(row=0, column=1, padx=20, pady=20, sticky="ew")

button3 = tk.Button(root, text="虚拟存储器管理模块", command=lambda: on_button_click("虚拟存储器管理模块"), font=("Arial", 14), height=2)
button3.grid(row=1, column=0, padx=20, pady=20, sticky="ew")

button4 = tk.Button(root, text="文件管理模块", command=lambda: on_button_click("文件管理模块"), font=("Arial", 14), height=2)
button4.grid(row=1, column=1, padx=20, pady=20, sticky="ew")

# 配置 grid 行列的权重，使得按钮在窗口大小变化时能够扩展
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# 运行主循环
root.mainloop()
