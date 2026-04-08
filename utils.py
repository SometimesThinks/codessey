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


# NxN 크기의 Cross(+) 패턴 생성 (중심 행과 열이 1)
def generate_cross_matrix(n):
    matrix = [[0.0] * n for _ in range(n)]
    mid = n // 2
    for i in range(n):
        matrix[mid][i] = 1.0  # 가로줄
        matrix[i][mid] = 1.0  # 세로줄
    return matrix


# NxN 크기의 X 패턴 생성 (대각선이 1)
def generate_x_matrix(n):
    matrix = [[0.0] * n for _ in range(n)]
    for i in range(n):
        matrix[i][i] = 1.0  # 왼쪽 위 -> 오른쪽 아래
        matrix[i][n - 1 - i] = 1.0  # 오른쪽 위 -> 왼쪽 아래
    return matrix


# +, cross -> Cross / x, X -> X 로 정규화
def normalize_label(label):
    label = str(label).lower().strip()
    if label in ["+", "cross"]:
        return "Cross"
    if label in ["x"]:
        return "X"
    return label
