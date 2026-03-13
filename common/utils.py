# -*- coding: utf-8 -*-
"""
常用工具
"""
import os

def read_file(file_path):
    """
    读取文件内容
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def get_all_files_in_dir(dir_path):
    """
    获取目录下所有文件路径
    """
    return [os.path.join(dir_path, f) for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]
