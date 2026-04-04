def get_input(prompt, min_choice, max_choice):
    # 사용자 입력 받기 + 공백 제거
    user_input = input(prompt).strip()
    # 입력이 비어있다면 None 반환
    if not user_input:
        print("입력이 비어있습니다. 다시 입력해주세요.")
        return None
    # 숫자가 아니라면 None 반환
    elif not user_input.isdigit():
        print("숫자만 입력 가능합니다.")
        return None
    # min_choice ~ max_choice 이외의 값이라면 None 반환

    elif int(user_input) < min_choice or int(user_input) > max_choice:
        print(f"{min_choice}~{max_choice} 사이의 숫자를 입력해주세요.")
        return None
    # 정상 입력이라면 반환
    return int(user_input)
