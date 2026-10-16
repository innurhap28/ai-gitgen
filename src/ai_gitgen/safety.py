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
    truncated_by_files = False
    truncated_by_lines = False

    for line in lines:
        if line.startswith("diff --git "):
            if file_count >= max_files:
                truncated_by_files = True
                break
            file_count += 1

        if len(result) >= max_lines:
            truncated_by_lines = True
            break

        result.append(line)

    if truncated_by_files or truncated_by_lines:
        result.append("")
        result.append(
            f"[Diff truncated: max_files={max_files}, max_lines={max_lines}]"
        )

    return "\n".join(result)