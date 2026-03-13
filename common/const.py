import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PROMPT_DIR = os.path.join(BASE_DIR, 'src/awesome_chain/prompt/src')

SRC_DIR = os.path.join(BASE_DIR, 'src')

SRC_INPUT_DIR = os.path.join(SRC_DIR, 'input')
SRC_OUTPUT_DIR = os.path.join(SRC_DIR, 'output')
SRC_TMP_DIR = os.path.join(SRC_DIR, 'tmp')


ENV_FILE = os.path.join(BASE_DIR, 'env/.env')

class PromptKey:
    PRE_RESEARCH_ADVISOR = "pre_research"
    COPY_GENERATOR = "copy_generator"
    Evaluator = "native"
