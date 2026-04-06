def get_num_input(prompt, min_choice, max_choice):
    while True:
        # 사용자 입력 받기 + 공백 제거
        user_input = input(prompt).strip()
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


def get_text_input(prompt):
    while True:
        # 사용자 입력 받기 + 공백 제거
        user_input = input(prompt).strip()
        # 입력이 비어있다면 다시 입력받기
        if not user_input:
            print("입력이 비어있습니다. 다시 입력해주세요.")
            continue
        # 정상 입력이라면 반환
        return user_input
