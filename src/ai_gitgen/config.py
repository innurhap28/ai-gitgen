# 기본 설정값 및 환경변수
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.4-mini")

DEFAULT_TEMP = 0.3
DEFALUT_MAX_TOKEN = 500