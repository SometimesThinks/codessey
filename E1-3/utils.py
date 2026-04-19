import sys


# 터미널 직접 입력, 파일 읽기 개행 보정 함수
def smart_input(prompt=""):
    try:
        user_input = input(prompt)
        # 파일 읽기 시, 수동 개행
        if not sys.stdin.isatty():
            print()
        return user_input.strip()
    except EOFError:
        return ""


# 숫자입력 함수
def get_num_input(prompt, min_choice, max_choice):
    while True:
        # 사용자 입력 받기 + 공백 제거
        user_input = smart_input(prompt).strip()
        # 입력이 비어있다면 다시 입력받기
        if not user_input:
            print("입력이 비어있습니다. 다시 입력해주세요.")
            continue
        # 숫자가 아니라면 다시 입력받기
        elif not user_input.isdigit():
            print("자연수만 입력 가능합니다.")
            continue
        # min_choice ~ max_choice 이외의 값이라면 다시 입력받기
        elif int(user_input) < min_choice or int(user_input) > max_choice:
            print(f"{min_choice}~{max_choice} 사이의 숫자를 입력해주세요.")
            continue
        # 정상 입력이라면 반환
        return user_input
