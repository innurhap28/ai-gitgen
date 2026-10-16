from src.ai_gitgen.ai_client import generate_text

def main():
    prompt = "다음 변경 사항에 적합한 짧은 Git 커밋 제목을 작성해 줘: 로그인 오류 수정"
    
    try:
        result = generate_text(
            prompt=prompt,
            temperature=0.3,
            max_tokens=100
        )
        print("AI 응답:")
        print(result)

    except Exception as e:
        print(f"테스트 실패: {type(e).__name__}: {e}")

if __name__ == "__main__":
    main()