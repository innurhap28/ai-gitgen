# git status / git diff 수집

import subprocess

GIT_NOT_FOUND_MSG = "Git 명령어를 찾을 수 없습니다. Git 설치 여부를 확인하세요."
GIT_STATUS_ERR_MSG = "Git 상태를 가져오지 못했습니다."
GIT_DIFF_ERR_MSG = "Git 변경 사항을 가져오지 못했습니다."


def check_git_repository():
    """
    Git 저장소인지 확인
    저장소가 아니면 False
    Git 명령어 자체가 없으면 예외 발생
    """
    try:
        subprocess.run(["git", "rev-parse", "--show-toplevel"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        return False
    except FileNotFoundError as e:
        raise RuntimeError(GIT_NOT_FOUND_MSG) from e

def get_git_status():
    """
    Git 상태 문자열 반환
    출력 메시지는 담당하지 않음
    """
    try:
        git_status = subprocess.run(["git", "status", "--short"], check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return git_status.stdout.rstrip("\n")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(GIT_STATUS_ERR_MSG) from e
    except FileNotFoundError as e:
        raise RuntimeError(GIT_NOT_FOUND_MSG) from e

def get_git_diff():
    """
    Git diff 문자열 반환
    git add가 된 파일에 대한 변경사항만
    출력 메시지는 담당하지 않음
    """
    try:
        git_diff = subprocess.run(["git", "diff", "--cached"], check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return git_diff.stdout
    except subprocess.CalledProcessError as e:
        raise RuntimeError(GIT_DIFF_ERR_MSG) from e
    except FileNotFoundError as e:
        raise RuntimeError(GIT_NOT_FOUND_MSG) from e

def get_current_branch():
    """현재 브랜치 이름 반환"""
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        raise RuntimeError("현재 브랜치 정보를 가져오지 못했습니다.") from e
    except FileNotFoundError as e:
        raise RuntimeError(GIT_NOT_FOUND_MSG) from e