# 생성 결과 검증 및 후처리
import re

def validate_commit_message(message):
    if not message or not message.strip():
        raise ValueError("커밋 메시지가 비어 있습니다.")

    message = message.strip()
    first_line = message.splitlines()[0]

    if len(first_line) > 72:
        raise ValueError("커밋 메시지 제목이 72자를 초과하였습니다.")
    if first_line.lower().startswith("commit message"):
        raise ValueError("불필요한 라벨이 포함되었습니다.")
    if "```" in message:
        raise ValueError("커밋 메시지에 코드블럭이 포함되었습니다.")
    return message

def validate_pr_title(title):
    if not title or not title.strip():
        raise ValueError("PR 제목이 비어 있습니다.")

    title = title.strip()

    if title.startswith("TITLE:"):
        title = title.replace("TITLE:", "", 1).strip()
    if len(title) > 80:
        raise ValueError("PR 제목이 80자를 초과하였습니다.")
    if "```" in title:
        raise ValueError("PR 제목에 코드블럭이 포함되었습니다.")
    return title

def validate_pr_body(body):
    if not body or not body.strip():
        raise ValueError("PR 본문이 비어 있습니다.")

    body = body.strip()
    required_sections = [
        "## Why",
        "## What",
        "## How to Test",
    ]
    for section in required_sections:
        if section not in body:
            raise ValueError(f"PR 본문에 필수 섹션이 없습니다: {section}")

    if "```" in body:
        raise ValueError("PR 본문에 코드블럭이 포함되었습니다.")
    return body

def clean_output(text):
    if not text:
        return ""

    text = text.strip()

    text = re.sub(r"^```[a-zA-Z]*\n?", "", text)
    text = re.sub(r"\n?```$", "", text)

    return text.strip()