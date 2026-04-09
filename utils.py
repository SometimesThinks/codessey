import sys
import json


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


# +, cross -> Cross / x, X -> X 로 정규화
def normalize_label(label):
    label = str(label).lower().strip()
    if label in ["+", "cross"]:
        return "Cross"
    if label in ["x"]:
        return "X"
    if label in ["undecided", "undecided_status"]:
        return "UNDECIDED"
    return label


# JSON 파일 로드 함수
def load_json(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"{file_path} 파일이 존재하지 않습니다.")
        return None
    except json.JSONDecodeError:
        print(f"{file_path} 파일 형식이 올바르지 않습니다.")
        return None


# 패턴 키에서 사이즈(N) 추출 함수 (예: size_5_1 -> 5)
def extract_size_from_key(key):
    try:
        return int(key.split("_")[1])
    except (IndexError, ValueError):
        return None
