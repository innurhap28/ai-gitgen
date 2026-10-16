# AI API 호출
from openai import OpenAI
from config import (OPENAI_API_KEY,OPENAI_BASE_URL,OPENAI_MODEL,DEFALUT_MAX_TOKEN,DEFAULT_TEMP)

def generate_text(prompt, temperature=DEFAULT_TEMP, max_tokens=DEFALUT_MAX_TOKEN):

    if not OPENAI_API_KEY:
        raise ValueError("환경변수에 API 키가 설정되지 않았습니다.")

    client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL)
    try:
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
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