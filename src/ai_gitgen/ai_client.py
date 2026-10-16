# AI API 호출

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

def generate_text(prompt, temperature=0.3, max_tokens=500):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("환경변수에 API 키가 설정되지 않았습니다.")

    base_url = os.getenv("OPENAI_BASE_URL")
    client = OpenAI(api_key=api_key, base_url=base_url)
    try:
        response = client.chat.completions.create(
            model="gpt-5.4-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens
        )
    except Exception as e:
        raise RuntimeError("AI API 호출에 실패했습니다.") from e

    content = response.choices[0].message.content
    if not content:
        raise RuntimeError("AI 응답이 비어 있습니다.")
    
    return content.strip()