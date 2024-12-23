import tkinter as tk
from tkinter import messagebox


class MemoryManager:
    def __init__(self):
        self.total_memory = 128  # 总内存128K
        self.os_memory = 4  # 操作系统占用4K
        self.free_memory = 124  # 可用内存124K（128K - 4K）
        self.allocated = []  # 已分配内存列表
        self.free_blocks = [{'start': 4, 'size': 124}]  # 初始未分配内存块（从4K开始，剩余124K）
        self.fixed_partition_size = 31  # 固定分区大小31K，设为31K作为示例

    def allocate_fixed_partition(self):
        """ 固定分区分配 """
        if self.free_memory < self.fixed_partition_size:
            return "内存不足！"

        for block in self.free_blocks:
            if block['size'] >= self.fixed_partition_size:
                self.allocated.append({'start': block['start'], 'size': self.fixed_partition_size})
                self.free_memory -= self.fixed_partition_size
                block['start'] += self.fixed_partition_size
                block['size'] -= self.fixed_partition_size
                if block['size'] == 0:
                    self.free_blocks.remove(block)
                return f"分配成功：{self.fixed_partition_size}K，起始地址：{block['start'] - self.fixed_partition_size}K"
        return "没有足够空间进行分配！"

    def allocate_variable_partition(self, size):
        """ 可变分区分配 """
        if size > self.free_memory:
            return "内存不足！"

        for block in self.free_blocks:
            if block['size'] >= size:
                self.allocated.append({'start': block['start'], 'size': size})
                self.free_memory -= size
                block['start'] += size
                block['size'] -= size
                if block['size'] == 0:
                    self.free_blocks.remove(block)
                return f"分配成功：{size}K，起始地址：{block['start'] - size}K"
        return "没有足够空间进行分配！"

    def release_fixed_partition(self, start):
        """ 释放指定起始地址的固定分区 """
        for alloc in self.allocated:
            if alloc['start'] == start and alloc['size'] == self.fixed_partition_size:
                self.allocated.remove(alloc)
                self.free_memory += alloc['size']
                # 合并回空闲块
                self.free_blocks.append({'start': alloc['start'], 'size': alloc['size']})
                return f"释放成功：{alloc['size']}K，起始地址：{alloc['start']}K"
        return "未找到该固定分区！"

    def release_variable_partition(self, start):
        """ 释放指定起始地址的可变分区 """
        for alloc in self.allocated:
            if alloc['start'] == start:
                self.allocated.remove(alloc)
                self.free_memory += alloc['size']
                # 合并回空闲块
                self.free_blocks.append({'start': alloc['start'], 'size': alloc['size']})
                return f"释放成功：{alloc['size']}K，起始地址：{alloc['start']}K"
        return "未找到该分区！"

    def get_allocated_memory(self):
        """ 获取已分配的内存信息 """
        return '\n'.join([f"起始地址：{alloc['start']}K，大小：{alloc['size']}K" for alloc in self.allocated])

    def get_free_memory(self):
        """ 获取剩余的内存信息 """
        return '\n'.join([f"起始地址：{block['start']}K，大小：{block['size']}K" for block in self.free_blocks])


class MemoryManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("内存管理系统")
        self.memory_manager = MemoryManager()

        # 设置窗口大小和位置
        self.root.geometry("400x400+500+200")  # 窗口大小400x400，居中显示
        self.root.config(bg="#f4f4f9")

        # GUI界面设置
        self.setup_ui()

    def setup_ui(self):
        # 创建主框架
        main_frame = tk.Frame(self.root, bg="#f4f4f9")
        main_frame.pack(expand=True, fill=tk.BOTH)

        # 创建按钮
        self.btn_fixed_partition = tk.Button(main_frame, text="固定分区", font=("Helvetica", 14), width=20, height=2,
                                             bg="#4CAF50", fg="white", command=self.show_fixed_partition_menu)
        self.btn_fixed_partition.pack(pady=20)

        self.btn_variable_partition = tk.Button(main_frame, text="可变分区", font=("Helvetica", 14), width=20, height=2,
                                                bg="#2196F3", fg="white", command=self.show_variable_partition_menu)
        self.btn_variable_partition.pack(pady=20)

        # 添加菜单
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # 添加主菜单
        self.menu_memory = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="内存管理", menu=self.menu_memory)
        self.menu_memory.add_command(label="固定分区", command=self.show_fixed_partition_menu)
        self.menu_memory.add_command(label="可变分区", command=self.show_variable_partition_menu)
        self.menu_memory.add_separator()
        self.menu_memory.add_command(label="退出", command=self.root.quit)

    def show_fixed_partition_menu(self):
        """ 显示固定分区菜单 """
        self.fixed_partition_window = tk.Toplevel(self.root)
        self.fixed_partition_window.title("固定分区管理")

        self.btn_fixed_allocate = tk.Button(self.fixed_partition_window, text="分配空间",
                                            command=self.allocate_fixed_partition)
        self.btn_fixed_allocate.pack(padx=10, pady=5)



        self.text_fixed_allocated = tk.Text(self.fixed_partition_window, height=10, width=40)
        self.text_fixed_allocated.pack(padx=10, pady=10)


        # 起始地址输入框
        self.label_fixed_release = tk.Label(self.fixed_partition_window, text="请输入起始地址(K):")
        self.label_fixed_release.pack(padx=10, pady=5)

        self.entry_fixed_start = tk.Entry(self.fixed_partition_window)
        self.entry_fixed_start.pack(padx=10, pady=5)

        self.btn_fixed_release = tk.Button(self.fixed_partition_window, text="释放空间",
                                           command=self.release_fixed_partition)
        self.btn_fixed_release.pack(padx=10, pady=5)



        self.update_fixed_memory_info()

    def show_variable_partition_menu(self):
        """ 显示可变分区菜单 """
        self.variable_partition_window = tk.Toplevel(self.root)
        self.variable_partition_window.title("可变分区管理")

        tk.Label(self.variable_partition_window, text="分配空间大小(K):").pack(padx=10, pady=5)
        self.entry_variable_size = tk.Entry(self.variable_partition_window)
        self.entry_variable_size.pack(padx=10, pady=5)

        self.btn_variable_allocate = tk.Button(self.variable_partition_window, text="分配空间",
                                               command=self.allocate_variable_partition)
        self.btn_variable_allocate.pack(padx=10, pady=5)





        self.text_variable_allocated = tk.Text(self.variable_partition_window, height=10, width=40)
        self.text_variable_allocated.pack(padx=10, pady=10)


        self.label_variabled_release = tk.Label(self.variable_partition_window, text="请输入起始地址(K):")
        self.label_variabled_release.pack(padx=10, pady=5)

        self.entry_variabled_start = tk.Entry(self.variable_partition_window)
        self.entry_variabled_start.pack(padx=10, pady=5)

        self.btn_variable_release = tk.Button(self.variable_partition_window, text="释放空间",
                                              command=self.release_variable_partition)
        self.btn_variable_release.pack(padx=10, pady=5)

        self.update_variable_memory_info()

    def allocate_fixed_partition(self):
        """ 固定分区分配 """
        result = self.memory_manager.allocate_fixed_partition()
        messagebox.showinfo("分配结果", result)
        self.update_fixed_memory_info()

    def allocate_variable_partition(self):
        """ 可变分区分配 """
        size = self.entry_variable_size.get()
        if not size.isdigit():
            messagebox.showerror("错误", "请输入有效的内存大小！")
            return
        result = self.memory_manager.allocate_variable_partition(int(size))
        messagebox.showinfo("分配结果", result)
        self.update_variable_memory_info()

    def release_fixed_partition(self):
        """ 固定分区释放 """
        start = self.entry_fixed_start.get()
        if not start.isdigit():
            messagebox.showerror("错误", "请输入有效的分区起始地址！")
            return
        result = self.memory_manager.release_fixed_partition(int(start))
        messagebox.showinfo("释放结果", result)
        self.update_fixed_memory_info()

    def release_variable_partition(self):
        """ 释放指定分区 """
        start = self.entry_variabled_start.get()
        if not start.isdigit():
            messagebox.showerror("错误", "请输入有效的分区起始地址！")
            return
        result = self.memory_manager.release_variable_partition(int(start))
        messagebox.showinfo("释放结果", result)
        self.update_variable_memory_info()

    def update_fixed_memory_info(self):
        """ 更新固定分区的内存信息 """
        allocated_memory = self.memory_manager.get_allocated_memory()
        self.text_fixed_allocated.delete(1.0, tk.END)
        self.text_fixed_allocated.insert(tk.END, allocated_memory)

    def update_variable_memory_info(self):
        """ 更新可变分区的内存信息 """
        allocated_memory = self.memory_manager.get_allocated_memory()
        self.text_variable_allocated.delete(1.0, tk.END)
        self.text_variable_allocated.insert(tk.END, allocated_memory)


if __name__ == "__main__":
    root = tk.Tk()
    app = MemoryManagerApp(root)
    root.mainloop()
