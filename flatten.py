"""
将目标文件夹中所有子文件夹中的文件移动到根目录
"""

import os
import shutil
import argparse


def move2base(base_dir, current_dir=None):
    """
    递归的将一个文件夹下所有的文件移动到base_dir下
    参数列表
    param base_dir: str, 根目录，最终文件都会在这个目录下
    param current_dir: str, 递归寻找文件的起点，如果未指定则从base_dir中寻找
    """
    current_dir = current_dir if current_dir else base_dir
    for d in os.listdir(current_dir):
        full_d = os.path.join(current_dir, d)
        if os.path.isdir(full_d):
            # 如果是文件夹，递归移动
            move2base(base_dir, full_d)
            # 删除空文件夹
            os.rmdir(full_d)
        elif base_dir != current_dir:
            # 如果是文件，并且当前不是根目录，就移动
            while os.path.exists(os.path.join(base_dir, d)):
                # 如果有重名，在后面加上'(1)'
                d_name_pre_list, d_name_suffix = d.split('.')[:-1], d.split('.')[-1]
                d_name = ''.join(d_name_pre_list) + '(1).' + d_name_suffix
                d = d_name
            shutil.move(full_d, os.path.join(base_dir, d))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="将一个目录下的所有文件移动到根目录")
    parser.add_argument('base_dir', help="根目录，所有文件将会被移动到这里")
    parser.add_argument('-s', '--source', default=None, help="源路径，将在这个路径下寻找文件")
    args = parser.parse_args()

    move2base(args.base_dir, args.source)
