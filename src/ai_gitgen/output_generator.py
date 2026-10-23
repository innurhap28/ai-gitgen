from .ai_client import generate_text
from .validator import clean_output
from .prompt import build_retry_prompt

def generate_with_validation(prompt, validator, model, temperature, max_tokens, ask_retry):
    raw_result = generate_text(prompt, model=model, temperature=temperature, max_tokens=max_tokens)
    raw_result = clean_output(raw_result)

    try:
        return validator(raw_result)
    except ValueError as error:
        validation_error = str(error)
        if not ask_retry(error):
            raise ValueError(f"검증 실패: {error}\n생성 결과:\n{raw_result}") from error

    retry_prompt = build_retry_prompt(
        original_prompt=prompt,
        previous_result=raw_result,
        error=validation_error
    )
    retry_result = generate_text(retry_prompt, model=model, temperature=temperature, max_tokens=max_tokens)
    retry_result = clean_output(retry_result)

    try:
        return validator(retry_result)
    except ValueError as error:
        raise ValueError(f"재생성 결과가 검증에 실패했습니다: {error}\n생성 결과:\n{retry_result}") from error