import datetime
import os
import re
import json
import openai


def get_client_cfg():
    return {
        "api_key": os.environ["API_KEY"],
        "base_url": os.environ["BASE_URL"]
    }


def get_gemini_config(name):
    return {
        "api_key": "Csc@1234.",
        "base_url": "https://ai.csc.hicoder.cn:8888/v1",
        "model_name": name
    }


def get_api_client(**kwargs):
    if not kwargs:
        cfg = get_client_cfg()
        client = AIClient(**cfg)
        client.set_model_name(get_model_name())
        return client
    client = AIClient(api_key=kwargs['api_key'], base_url=kwargs['base_url'])
    client.set_model_name(kwargs['model_name'])
    return client


class AIClient(openai.OpenAI):

    # def logs(self, **kwargs):
    #     return self.logs.list(**kwargs)

    def set_model_name(self, model_name):
        self._model_name = model_name

    def get_model_name(self):
        return self._model_name


def get_model_name():
    return os.environ.get("MODEL", )


def get_input_data():
    all_data = ""
    current_data = input(">:")
    if current_data.strip().upper() == "<EXIT>":
        return exit(0)  # 退出程序

    while current_data.strip().upper() not in ["<EOF>", "<QUIT>"]:
        if current_data.strip().upper() == "<EXIT>":
            return exit(0)  # 退出程序
        all_data += "\n" + current_data
        current_data = input(">:")

    if current_data.strip().upper() == "<QUIT>":
        return "<QUIT>"

    return all_data


def extract_and_parse_json(markdown_text):
    try:
        json_obj = json.loads(markdown_text)
        return json_obj
    except ValueError as ve:
        pass

    # 定义正则表达式来匹配 Markdown 代码块
    code_block_pattern = re.compile(r'.*```(?:json)?\s*([\s\S]*?)```.*')
    matches = code_block_pattern.findall(markdown_text)

    for match in matches:
        try:
            # 尝试将匹配到的内容解析为 JSON
            json_obj = json.loads(match)
            return json_obj
        except json.JSONDecodeError:
            # 如果解析失败，跳过该代码块
            continue

    return None


def get_llm_response(client, messages):
    for _ in range(3):
        try:
            # 调用 OpenAI API 进行对话
            response = client.chat.completions.create(
                model=client.get_model_name(),
                messages=messages,
                stream=True,  # 启用流式输出
                max_tokens=4096
            )
            content = ""
            think = ""
            # print(f"助手: ")
            for chunk in response:
                if hasattr(chunk.choices[0].delta, "reasoning_content") and chunk.choices[0].delta.reasoning_content:
                    think += chunk.choices[0].delta.reasoning_content
                    print(chunk.choices[0].delta.reasoning_content, end='')

                if chunk.choices[0].delta.content:
                    content += chunk.choices[0].delta.content
                    print(chunk.choices[0].delta.content, end='')
            _, content = extra_think_and_content(content)
            # print()
            # 将模型的回复添加到对话历史中
            messages.append({"role": "assistant", "content": content, "think": think})
            return messages, content
        except Exception as e:
            print(f"发生错误: {e}")

    raise Exception("重试次数超过限制")


def extra_think_and_content(content: str):
    """解析出think和输出"""
    think_start = False
    content_start = True
    think_list = []
    content_list = []
    for line in content.split("\n"):
        if line.split() == "<think>":
            think_start, content_start = True, False
            continue
        if line.split() == "</think>":
            think_start, content_start = False, True
            continue
        if think_start:
            think_list.append(line)

        if content_start:
            content_list.append(line)
    return "\n".join(think_list), "\n".join(content_list)


def get_time_tag():
    current_datetime = datetime.datetime.now()

    # 按照年月日时分秒的格式输出
    formatted_datetime = current_datetime.strftime("%m%d%H%M%S")
    return formatted_datetime


def read_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()


def save_to_excel(df, output_file="风险规则数据.xlsx"):
    """
    将DataFrame保存为Excel文件
    """
    try:
        df.to_excel(output_file, index=False, engine='openpyxl')
        print(f"Excel文件已成功保存到: {output_file}")
        print(f"共处理 {len(df)} 行数据")
    except Exception as e:
        print(f"保存Excel文件时出错: {e}")
