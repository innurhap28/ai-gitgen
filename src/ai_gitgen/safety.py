# safe-mode / 민감 정보 마스킹
import re

def mask_secrets(text):
    """민감한 정보로 보이는 값을 마스킹"""
    patterns = [
        r'(?i)(API_KEY\s*=\s*)["\']?([^\s"\']+)["\']?',
        r'(?i)(TOKEN\s*=\s*)["\']?([^\s"\']+)["\']?',
        r'(?i)(PASSWORD\s*=\s*)["\']?([^\s"\']+)["\']?',
        r'(?i)(SECRET\s*=\s*)["\']?([^\s"\']+)["\']?',
    ]

    for pattern in patterns:
        text = re.sub(pattern, r'\1****', text)

    return text


def limit_diff(diff, max_files=10, max_lines=200):
    """diff에 포함할 파일 수와 줄 수를 제한"""
    lines = diff.splitlines()
    result = []
    file_count = 0
    line_count = 0

    for line in lines:
        if line.startswith("diff --git "):
            if file_count >= max_files:
                break
            file_count += 1

        if line_count >= max_lines:
            break

        result.append(line)
        line_count += 1

    return "\n".join(result)