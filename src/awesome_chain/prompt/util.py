# -*- coding: utf-8 -*-
import os
from common import utils
from common.const import PROMPT_DIR


def load_prompt(prompt_name):
    """
    加载prompt文件, PROMPT_DIR目录下的一个文件夹，文件夹下存在多个文件，每个文件都是一个prompt， 将文件信息加载到字典中去并返回
    :param prompt_name: prompt文件夹名称
    :return: 字典，key为文件名，value为文件内容
    """
    prompt_dir = os.path.join(PROMPT_DIR, prompt_name)
    prompt_files = utils.get_all_files_in_dir(prompt_dir)
    prompt_dict = {}
    for prompt_file in prompt_files:
        prompt_dict[os.path.basename(prompt_file).split('.')[0]] = utils.read_file(prompt_file)
    return prompt_dict


if __name__ == '__main__':
    prompt_dict_ = load_prompt('copy_generator')
    print(prompt_dict_)
