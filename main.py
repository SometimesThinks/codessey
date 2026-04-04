from models import QuizGame

if __name__ == "__main__":
    game = QuizGame()
    while True:
        try:
            game.show_menu()
            # 앞뒤 공백 제거하며 입력 받기
            choice = input("메뉴를 선택하세요: ").strip()
            if choice == "1":
                game.play_quiz()
            elif choice == "2":
                game.add_quiz()
            elif choice == "3":
                game.show_quizzes()
            elif choice == "4":
                game.show_best_score()
            elif choice == "5":
                break
            # 빈 입력 예외 처리
            elif choice == "":
                print("메뉴 번호가 입력되지 않았습니다. 다시 입력해주세요.")
            # 숫자가 아닌 값 예외 처리
            elif not choice.isdigit():
                print("숫자만 입력 가능합니다.")
            # 1~5 이외의 값 예외 처리
            else:
                print("잘못된 메뉴입니다. 1~5 사이의 숫자를 입력해주세요.")
        # KeyboardInterrupt 예외 처리
        except KeyboardInterrupt as e:
            print(f"\n{type(e).__name__}으로 인해 프로그램이 종료되었습니다.")
            break
        # EOFError 예외 처리
        except EOFError as e:
            print(f"\n{type(e).__name__}으로 인해 프로그램이 종료되었습니다.")
            break
