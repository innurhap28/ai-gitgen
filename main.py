# 프로그램 진입점
import sys
from src.ai_gitgen.cli import run_cli


def main():
    try:
        return run_cli()
    except KeyboardInterrupt:
        print("")
        return 130
    except EOFError:
        print("")
        return 0


if __name__ == "__main__":
    sys.exit(main())