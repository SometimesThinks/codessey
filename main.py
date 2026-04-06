import sys
from utils import get_input
from models import QuizGame


def main():
    game = QuizGame()
    game.load_quizzes()

    try:
        while True:
            game.show_menu()
            choice = get_input("메뉴를 선택하세요: ", 1, 7)
            if choice == "1":
                game.play_quiz()
            elif choice == "2":
                game.add_quiz()
            elif choice == "3":
                game.delete_quiz()
            elif choice == "4":
                game.show_quizzes()
            elif choice == "5":
                game.show_best_score()
            elif choice == "6":
                game.show_history()
            elif choice == "7":
                break
    # KeyboardInterrupt 예외 처리(Ctrl + C가 인터럽트를 의미하기 때문)
    except KeyboardInterrupt as e:
        print(f"\n{type(e).__name__}으로 인해 프로그램이 종료되었습니다.")
        sys.exit()
    # EOFError 예외 처리(Ctrl + D가 파일의 끝을 의미하기 때문)
    except EOFError as e:
        print(f"\n{type(e).__name__}으로 인해 프로그램이 종료되었습니다.")
        sys.exit()
    finally:
        game.save_quizzes()


if __name__ == "__main__":
    main()
