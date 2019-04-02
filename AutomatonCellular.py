# coding:utf-8
import numpy as np
from random import random
from matplotlib import pyplot as plt

# 常量定义
# 颜色
ROAD_COLOR = 1
INTER_COLOR = 0.4
CAR_COLOR = 0.6
GREEN = 0.1
YELLOW = 0.2
RED = 0.3

# 入口坐标
ENTER = [
    (10, 29), (11, 29), (12, 29), (13, 0), (14, 0), (15, 0),
    (26, 29), (27, 29), (28, 0), (29, 0),
    (40, 29), (41, 29), (42, 0), (43, 0),
    (54, 29), (55, 29), (56, 29), (57, 0), (58, 0), (59, 0),
    (0, 12), (0, 13), (0, 14),
    (69, 15), (69, 16), (69, 17)
    ]
# 信号灯时间信息
lighttime = [
    # 10
    [8, 1.8, 1.8, 30, 3.8, 55],
    [5, 3.6, 4.2, 28, 3.8, 55],
    [7, 3.6, 2.2, 34.7, 3.6, 49.3],
    [7, 3.6, 2.2, 34.7, 3.6, 49.3],
    # 11
    [0, 0, 0, 20.2, 3.6, 76.1],
    [0, 0, 0, 20.3, 3.6, 76.2],
    [0, 0, 0, 41.5, 3.2, 55.4],
    [0, 0, 0, 41.5, 3.2, 55.4],
    # 12
    [0, 0, 0, 27.3, 3.6, 69.2],
    [0, 0, 0, 27.3, 3.6, 69.2],
    [0, 0, 0, 60.9, 3.2, 35.7],
    [0, 0, 0, 61.4, 3.2, 35.7],
    # 14
    [9.8, 3.6, 87, 36.9, 3.7, 60.2],
    [0, 0, 0, 22.4, 3.7, 74],
    [8.8, 3.6, 3.6, 34.6, 3.2, 46.1],
    [11.6, 3.6, 0.5, 36.6, 3.2, 45.3]
]


class Car:
    def __init__(self, i, j):
        # 坐标
        self.i = i
        self.j = j
        self.d = None

        # 方向，按东西南北为0123表示
        if i == 0:
            self.d = 2
        elif i == 69:
            self.d = 3
        else:
            if i in [10, 11, 12, 26, 27, 40, 41, 54, 55, 56]:
                self.d = 1
            else:
                self.d = 0

        # 车道，使用012表示左转，直行，右转
        if j < 12 or j > 17:
            if i in [10, 15, 26, 29, 40, 43, 54, 59]:
                self.ri = 2
            elif i in [11, 14, 27, 28, 41, 42, 55, 58]:
                self.ri = 1
            else:
                self.ri = 0
        elif j == 12 or j == 17:
            self.ri = 2
        elif j == 13 or j == 16:
            self.ri = 1
        else:
            self.ri = 0

    def next(self):
        # 返回车下一步将要移动的坐标
        # 车在东西走向
        if self.j < 11 or self.j > 18:
            if self.d == 0:
                return (self.i, self.j+1, False)
            else:
                return (self.i, self.j-1, False)
        # 车在主干西侧
        elif self.j == 11:
            if self.d == 1:
                return (self.i, self.j-1, False)
            else:
                if self.ri == 2:
                    return (self.i + 1, self.j + 1, True)
                elif self.ri == 1:
                    return (self.i, 18, True)
                else:
                    return (self.i - 4, 15, True)
        # 车在主干东侧
        elif self.j == 18:
            if self.d == 0:
                return (self.i, self.j+1, False)
            else:
                if self.ri == 2:
                    return (self.i - 1, self.j - 1, True)
                elif self.ri == 1:
                    return (self.i, 11, True)
                else:
                    return (self.i + 4, 14, True)
        # 车在主干道上
        else:
            # 车在横路北侧
            if self.i in [9, 25, 39, 53]:
                if self.d == 3:
                    return (self.i-1, self.j, False)
                else:
                    if self.ri == 0:
                        if self.i == 9 or self.i == 53:
                            return (self.i+4, self.j+4, True)
                        else:
                            return (self.i+3, self.j+4, True)
                    elif self.ri == 1:
                        if self.i == 9 or self.i == 53:
                            return (self.i+7, self.j, True)
                        else:
                            return (self.i+5, self.j, True)
                    else:
                        return (self.i+1, self.j-1, True)
            # 车在横路南侧
            elif self.i in [16, 30, 44, 60]:
                if self.d == 2:
                    return (self.i+1, self.j, False)
                else:
                    if self.ri == 0:
                        if self.i == 16 or self.i == 60:
                            return (self.i-4, self.j-4, True)
                        else:
                            return (self.i-3, self.j-4, True)
                    elif self.ri == 1:
                        if self.i == 16 or self.i == 60:
                            return (self.i-7, self.j, True)
                        else:
                            return (self.i-5, self.j, True)
                    else:
                        return (self.i-1, self.j+1, True)
            # 车不在路口，直接走
            else:
                if self.d == 2:
                    return (self.i+1, self.j, False)
                else:
                    return (self.i-1, self.j, False)
    
    # 更新位置、方向
    def update(self, ni, nj):
        if ni > self.i:
            if nj > self.j:
                if self.ri == 0:
                    self.d = 0
                else:
                    self.d = 2
            elif nj < self.j:
                if self.ri == 0:
                    self.d = 2
                else:
                    self.d = 1
        elif ni < self.i:
            if nj > self.j:
                if self.ri == 0:
                    self.d = 3
                else:
                    self.d = 0
            elif nj < self.j:
                if self.ri == 0:
                    self.d = 1
                else:
                    self.d = 3
        self.i = ni
        self.j = nj


# 信号灯控制函数
def next_light(cross):
    for i, c in enumerate(cross):
        c[1] = c[1] - 1
        while c[1] < 0:
            c[0] = (c[0] + 1) % 6
            c[1] = lighttime[i][int(c[0])] + c[1]
        if c[2] > 0:
            c[2] = c[2] - 1
    return cross


# 查询即将过马路的车应该参考哪个信号灯
def which_light(i, j, d):
    # 确定是哪个路口
    if i < 20:
        ci = 3
    elif i < 35:
        ci = 2
    elif i < 50:
        ci = 1
    else:
        ci = 0

    # 确定信号灯编号
    return ci * 4 + d


# 变量定义
# 定义元胞
cells = np.zeros((70, 30))
# 定义一个列表，存储路口信息，状态分别为灯的状态，时间，等候队列
cross = np.zeros((16, 3))
# 车的列表
car_list = []

# 初始化视图
plt.figure(dpi=160, facecolor='lightgray')
plt.xticks([])
plt.yticks([])
plt.grid(linestyle=':')
plt.ion()
# 绘制路面
cells[10:16, :] = ROAD_COLOR
cells[26:30, :] = ROAD_COLOR
cells[40:44, :] = ROAD_COLOR
cells[54:60, :] = ROAD_COLOR
cells[:, 12:18] = ROAD_COLOR
# 绘制路口
cells[10:16, 12:18] = INTER_COLOR
cells[26:30, 12:18] = INTER_COLOR
cells[40:44, 12:18] = INTER_COLOR
cells[54:60, 12:18] = INTER_COLOR

# 模拟300秒
for ti in range(300):
    # 更新信号灯状态
    cross = next_light(cross)

    # 更新车的信息
    for ci, car in enumerate(car_list):
        (ni, nj, in_cross) = car.next()
        not_empty = False
        for tci, tcar in enumerate(car_list):
            if tci == ci:
                continue
            elif ni == tcar.i and nj == tcar.j:
                not_empty = True
        if not_empty:
            continue

        # 如果没有在过马路或者在右转，直接转弯
        if in_cross is False or car.ri == 2:
            # 还原路面
            cells[car.i, car.j] = ROAD_COLOR
            if ni < 0 or ni > 69 or nj < 0 or nj > 29:
                car_list.remove(car)
            # 更新车的位置
            car.update(ni, nj)
        else:
            # 此时在转弯
            li = which_light(car.i, car.j, car.d)
            if car.ri == 0:
                if cross[li, 0] == 0 and cross[li, 2] == 0:
                    # 还原路面
                    cells[car.i, car.j] = ROAD_COLOR
                    # 更新车的位置
                    car.update(ni, nj)
                    # 让后面的车等待
                    cross[li, 2] = 3
            elif car.ri == 1:
                if cross[li, 0] == 3 and cross[li, 2] == 0:
                    # 还原路面
                    cells[car.i, car.j] = ROAD_COLOR
                    # 更新车的位置
                    car.update(ni, nj)
                    # 让后面的车等待
                    cross[li, 2] = 3

    # 每个入口以1/3概率出现车
    for (i, j) in ENTER:
        if random() < 1/9:
            car_list.append(Car(i, j))

    # 更新显示
    # 倒计时
    plt.title('Time:{:>3}s'.format(ti))
    # 车
    for car in car_list:
        cells[car.i, car.j] = CAR_COLOR
    
    plt.imshow(cells, cmap='jet')
    plt.pause(1)
