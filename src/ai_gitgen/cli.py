# CLI 명령어 처리
import argparse
from .git_manager import *
from .safety import *
from .prompt import *
from .ai_client import generate_text
from .validator import *
from .config import *
from .output_generator import generate_with_validation

def parse_args():
    parser = argparse.ArgumentParser(prog="ai-gitgen")
    subparsers = parser.add_subparsers(dest="command", required=True)

    commit_parser = subparsers.add_parser("commit")
    commit_parser.add_argument("--model", default=OPENAI_MODEL)
    commit_parser.add_argument("--temperature", type=float, default=DEFAULT_TEMP)
    commit_parser.add_argument("--max-tokens", type=int, default=DEFAULT_MAX_TOKENS)
    commit_parser.add_argument("--safe-mode", action="store_true")

    pr_parser = subparsers.add_parser("pr")
    pr_parser.add_argument("--model", default=OPENAI_MODEL)
    pr_parser.add_argument("--temperature", type=float, default=DEFAULT_TEMP)
    pr_parser.add_argument("--max-tokens", type=int, default=DEFAULT_MAX_TOKENS)
    pr_parser.add_argument("--safe-mode", action="store_true")

    return parser.parse_args()

def run_cli():
    args = parse_args()

    try:
        if args.command == "commit":
            result = run_commit(args)
            if result is not None:
                print_result(result, mode="commit")
        elif args.command == "pr":
            result = run_pr(args)
            if result is not None:
                print_result(result, mode="pr")
    except (RuntimeError, ValueError) as e:
        print(f"오류: {e}")

def run_commit(args):
    if not check_git_repository():
        raise RuntimeError("Git 저장소가 아닙니다.")

    diff_text = get_git_diff()
    if not diff_text.strip():
        print("스테이징된 변경 사항이 없습니다. git add를 먼저 실행하세요.")
        return None
    status_text = get_git_status()
    masked_diff = mask_secrets(diff_text)

    if args.safe_mode:
        masked_diff = limit_diff(masked_diff, max_files=MAX_DIFF_FILES, max_lines=MAX_DIFF_LINES)

    prompt = build_commit_prompt(status_text, masked_diff)
    result = generate_with_validation(
        prompt=prompt,
        validator=validate_commit_message,
        model=args.model,
        temperature=args.temperature,
        max_tokens=args.max_tokens,
        ask_retry=ask_retry,
    )

    return result

def run_pr(args):
    if not check_git_repository():
        raise RuntimeError("Git 저장소가 아닙니다.")

    diff_text = get_git_diff()
    if not diff_text.strip():
        print("스테이징된 변경 사항이 없습니다. git add를 먼저 실행하세요.")
        return None
    status_text = get_git_status()
    masked_diff = mask_secrets(diff_text)

    if args.safe_mode:
        masked_diff = limit_diff(masked_diff, max_files=MAX_DIFF_FILES, max_lines=MAX_DIFF_LINES)
    
    prompt = build_pr_prompt(status_text, masked_diff)
    result = generate_with_validation(
        prompt=prompt,
        validator=validate_pr_response,
        model=args.model,
        temperature=args.temperature,
        max_tokens=args.max_tokens,
        ask_retry=ask_retry,
    )

    return result

def print_result(result, mode):
    if mode == "commit":
        print("--- Commit Message ---")
        print(result)
        print("----------------------")

    elif mode == "pr":
        print("--- PR Title ---")
        print(result["title"])
        print()
        print("--- PR Body ---")
        print(result["body"])
        print("----------------")

def ask_retry(error):
    print(f"검증 실패: {error}")
    answer = input("추가 API 요청으로 재생성할까요? [y/n]: ").strip().lower()
    return answer == "y"