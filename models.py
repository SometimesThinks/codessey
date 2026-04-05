import os
import json
from utils import get_input
from constants import FILE_PATH, DEFAULT_QUIZZES


class Quiz:
    def __init__(self, question, choices, answer):
        self.question = question
        self.choices = choices
        self.answer = answer

    def display_quiz(self):
        print(self.question)
        for i, choice in enumerate(self.choices):
            print(f"{i + 1}. {choice}")

    def check_answer(self, answer):
        return self.answer == answer


class QuizGame:
    def __init__(self):
        self.quizzes = []
        self.best_score = 0

    def show_menu(self):
        print("=" * 30)
        print("파이썬 기초 문법 퀴즈")
        print("=" * 30)
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 종료")
        print("=" * 30)

    def load_quizzes(self):
        if os.path.isfile(FILE_PATH):
            try:
                pass
            except Exception:
                pass
        if not self.quizzes:
            self.quizzes = [quiz for quiz in DEFAULT_QUIZZES]

    def play_quiz(self):
        print("=" * 30)
        print("퀴즈를 시작합니다!")
        print("=" * 30)
        score = 0
        for quiz in self.quizzes:
            quiz = Quiz(**quiz)
            quiz.display_quiz()
            answer = input("정답: ")
            if quiz.check_answer(answer):
                print("정답입니다!")
                score += 1
            else:
                print("아쉽지만 오답입니다...")
            print()
        print("=" * 30)
        print(f"최종 점수: {score}")
        print("=" * 30)

    def add_quiz(self):
        print("=" * 30)
        print("퀴즈를 추가합니다!")
        print("=" * 30)
        question = input("문제: ")
        choices = []
        for i in range(4):
            choice = input(f"{i + 1}. ")
            choices.append(choice)
        answer = get_input("정답: ", 1, 4)
        self.quizzes.append(
            {"question": question, "choices": choices, "answer": answer}
        )
        # 퀴즈 변경 사항 저장(추가, 삭제)
        if self.save_quizzes():
            print("퀴즈가 추가되었습니다!")
        else:
            self.quizzes.pop()
            print("퀴즈 추가에 실패했습니다.")

    # 퀴즈 변경 사항 저장(추가, 삭제)
    def save_quizzes(self):
        try:
            with open(FILE_PATH, "w", encoding="utf-8") as f:
                json.dump(self.quizzes, f, ensure_ascii=False, indent=4)
            return True
        except Exception:
            return False
