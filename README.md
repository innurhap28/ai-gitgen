
## 프로젝트 구조

```
ai-gitgen/
│
├── main.py
│
├── src/
│   └── ai_gitgen/
│       ├── __init__.py
│       ├── cli.py
│       ├── config.py           # 기본 설정값 및 환경변수
│       │
│       ├── git_manager.py      # git status / git diff 수집
│       ├── ai_client.py        # AI API 호출
│       ├── prompt.py           # Commit / PR 프롬프트 설계
│       ├── validator.py        # 생성 결과 검증 및 후처리
│       └── safety.py           # safe-mode / 민감정보 마스킹
│
├── tests/
│   ├── test_git_manager.py
│   ├── test_prompt.py
│   └── test_validator.py
│
├── docs/
│   └── design.md
│
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
└── pyproject.toml
```