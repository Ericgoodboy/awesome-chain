import os
import argparse
from dotenv import load_dotenv
from common import const


def load_env():
    parser = argparse.ArgumentParser(description='环境配置工具')
    parser.add_argument('--env', type=str, default=const.ENV_FILE, help='环境配置文件路径')
    args = parser.parse_args()
    load_dotenv(args.env, override=True)
    print("api_key: ****")
    print("base_url: {}".format(os.environ["BASE_URL"]))
    print("model: {}".format(os.environ["MODEL"]))


def do_load_env(path):
    load_dotenv(path, override=True)
    print("api_key: ****")
    print("base_url: {}".format(os.environ["BASE_URL"]))
    print("model: {}".format(os.environ["MODEL"]))
