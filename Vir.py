from collections import deque, OrderedDict
import heapq


def read_page_sequence(filename):
    with open(filename, 'r') as file:
        # 读取页面序列，将其转换为整数列表
        return list(map(int, file.read().split()))


def FIFO(page_sequence, frames):
    page_faults = 0  # 初始化缺页次数为0,缺页次数用来统计在整个页面序列中发生的缺页事件。
    memory = deque()  # 用 deque 来模拟内存页框，初始为空
    page_fault_list = []  # 用于记录淘汰的页面，便于输出

    # 遍历页面序列中的每一个页面
    for page in page_sequence:
        # 如果页面不在内存中（即发生缺页）
        # print(f"内存:{memory}")
        # print(f"此时已经读到页面序列:{page}")
        if page not in memory:
            page_faults += 1  # 增加缺页次数
            if len(memory) == frames:  # 如果内存中已经存满了页面
                # 淘汰队头页面（FIFO算法的特点：先到先淘汰）
                print(f"内存:{memory}")
                print(f"此时已经读到页面序列:{page}")
                # 左端弹出
                removed_page = memory.popleft()
                page_fault_list.append(removed_page)  # 记录淘汰的页面
                print(f"淘汰页面: {removed_page}")  # 输出淘汰的页面
            memory.append(page)  # 将新页面加入内存
    # print(f"淘汰总页面: {page_fault_list}")
    # 返回淘汰页面的列表和缺页总次数
    return page_fault_list, page_faults


def LRU(page_sequence, frames):
    page_faults = 0
    memory = OrderedDict()  # 使用 OrderedDict 来保持页面的插入顺序
    page_fault_list = []

    for page in page_sequence:
        if page not in memory:
            page_faults += 1
            if len(memory) == frames:
                print(f"内存:{memory}")
                print(f"此时已经读到页面序列:{page}")
                # 淘汰最久未使用的页面
                removed_page, _ = memory.popitem(last=False)
                page_fault_list.append(removed_page)
                print(f"淘汰页面: {removed_page}")  # 输出淘汰的页面
        else:
            # 将页面移到字典的末尾表示最近使用
            del memory[page]
        memory[page] = None

    return page_fault_list, page_faults


def LFU(page_sequence, frames):
    page_faults = 0
    memory = {}  # 记录页面
    frequency = {}  # 记录页面频率
    page_fault_list = []

    for page in page_sequence:
        if page not in memory:
            page_faults += 1
            if len(memory) == frames:
                # 淘汰访问频率最少的页面
                min_freq = min(frequency.values())
                lfu_pages = [p for p, f in frequency.items() if f == min_freq]
                if len(lfu_pages) == 1:
                    page_to_remove = lfu_pages[0]
                else:
                    print(f"内存:{memory}")
                    print(f"此时已经读到页面序列:{page}")
                    # 处理多个频率相同的页面时选择最早被访问的
                    page_to_remove = lfu_pages[0]
                del memory[page_to_remove]
                del frequency[page_to_remove]
                page_fault_list.append(page_to_remove)
                print(f"淘汰页面: {page_to_remove}")  # 输出淘汰的页面

        # 更新页面的频率
        memory[page] = None
        frequency[page] = frequency.get(page, 0) + 1

    return page_fault_list, page_faults


def main():
    filename = 'page_sequence.txt'  # 输入文件名
    page_sequence = read_page_sequence(filename)
    frames = int(input("Enter number of frames: "))  # 物理内存的页面框架数

    # FIFO调度算法
    print("FIFO:")
    fifo_result, fifo_faults = FIFO(page_sequence, frames)
    print("缺页总数: ", fifo_faults)

    # LRU调度算法
    print("\nLRU:")
    lru_result, lru_faults = LRU(page_sequence, frames)
    print("缺页总数: ", lru_faults)

    # LFU调度算法
    print("\nLFU:")
    lfu_result, lfu_faults = LFU(page_sequence, frames)
    print("缺页总数: ", lfu_faults)


if __name__ == '__main__':
    main()
