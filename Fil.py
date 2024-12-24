def read_disk_sequence(filename):
    # 从文件中读取磁道服务顺序
    with open(filename, 'r') as file:
        return list(map(int, file.read().split()))


def FCFS(sequence, initial_position):
    current_position = initial_position
    total_distance = 0
    for track in sequence:
        total_distance += abs(track - current_position)
        current_position = track
    return total_distance


def SSTF(sequence, initial_position):
    current_position = initial_position
    total_distance = 0
    remaining_tracks = sequence.copy()
    while remaining_tracks:
        # 找到距离当前磁头位置最近的磁道
        closest_track = min(remaining_tracks, key=lambda x: abs(x - current_position))
        total_distance += abs(closest_track - current_position)
        current_position = closest_track
        remaining_tracks.remove(closest_track)
    return total_distance


def SCAN(sequence, initial_position, direction='right'):
    sequence.sort()  # 磁道按照升序排列
    current_position = initial_position
    total_distance = 0
    left = [track for track in sequence if track < current_position]
    right = [track for track in sequence if track > current_position]

    # 如果方向是向右
    if direction == 'right':
        # 移动到最远的右端，然后返回
        total_distance += abs(current_position - right[-1])
        total_distance += abs(right[-1] - left[0]) if left else 0
    else:
        # 向左方向移动
        total_distance += abs(current_position - left[0])
        total_distance += abs(left[0] - right[-1]) if right else 0

    return total_distance


def main():
    filename = input("请输入磁道服务顺序的文件路径: ")  # 输入文件路径
    initial_position = int(input("请输入磁头的初始位置: "))  # 输入磁头的初始位置
    direction = input("请输入扫描方向 ('left' 或 'right'): ")  # 扫描方向

    # 从文件读取磁道服务顺序
    sequence = read_disk_sequence(filename)

    # 输出磁道服务顺序
    print(f"磁道服务顺序: {sequence}")

    # 先来先服务 FCFS
    fcfs_distance = FCFS(sequence, initial_position)
    print(f"FCFS 总移动道数: {fcfs_distance}")

    # 最短寻道优先 SSTF
    sstf_distance = SSTF(sequence, initial_position)
    print(f"SSTF 总移动道数: {sstf_distance}")

    # 电梯算法 SCAN
    scan_distance = SCAN(sequence, initial_position, direction)
    print(f"SCAN 总移动道数: {scan_distance}")


if __name__ == "__main__":
    main()
