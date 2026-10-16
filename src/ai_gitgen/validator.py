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

    positions = []

    for section in required_sections:
        position = body.find(section)
        if position == -1:
            raise ValueError(
                f"PR 본문에 필수 섹션이 없습니다: {section}"
            )
        positions.append(position)

    if positions != sorted(positions):
        raise ValueError("PR 섹션 순서가 올바르지 않습니다.")

    for i, section in enumerate(required_sections):
        start = positions[i] + len(section)

        if i + 1 < len(required_sections):
            end = positions[i + 1]
        else:
            end = len(body)

        section_body = body[start:end]

        if not any(
            line.strip().startswith("- ")
            for line in section_body.splitlines()
        ):
            raise ValueError(
                f"{section} 섹션에 불릿이 없습니다."
            )

    if "```" in body:
        raise ValueError("PR 본문에 코드블록이 포함되었습니다.")

    return body

def clean_output(text):
    if not text:
        return ""

    text = text.strip()
    text = re.sub(r"^```[a-zA-Z0-9_-]*\s*\n?", "", text)
    text = re.sub(r"\n?```\s*$", "", text)

    return text.strip()