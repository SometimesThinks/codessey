import os
import json
from random import shuffle
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
        self.best_score = None

    # 현재 사용할 퀴즈 리스트를 결정(내 퀴즈가 있으면 내 걸, 없으면 기본 퀴즈 반환)
    def get_current_quizzes(self):
        if self.quizzes:
            return self.quizzes
        return DEFAULT_QUIZZES

    # 메뉴 출력
    def show_menu(self):
        print("=" * 30)
        print("파이썬 기초 문법 퀴즈")
        print("=" * 30)
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 최고 점수 확인")
        print("5. 종료")
        print("=" * 30)

    # 퀴즈 불러오기
    def load_quizzes(self):
        if os.path.isfile(FILE_PATH):
            try:
                with open(FILE_PATH, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.quizzes = data["quizzes"]
                    self.best_score = data["best_score"]
            except Exception:
                print("파일을 불러오는 중 오류가 발생했습니다.")

    # 퀴즈 풀기
    def play_quiz(self):
        quizzes_to_play = self.get_current_quizzes()
        # 퀴즈 셔플
        shuffle(quizzes_to_play)
        # 퀴즈 시작
        print("=" * 30)
        print("퀴즈를 시작합니다!")
        print("=" * 30)
        score = 0
        for quiz in quizzes_to_play:
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
        print(f"정답 개수: {score}")
        # 최고 점수 업데이트
        if self.update_best_score(score):
            print("최고 점수 갱신!")
        print("=" * 30)

    # 퀴즈 추가
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
            data = {
                "best_score": self.best_score,
                "quizzes": self.quizzes,
            }
            with open(FILE_PATH, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            return True
        except Exception:
            return False

    # 퀴즈 목록
    def show_quizzes(self):
        quizzes_to_show = self.get_current_quizzes()
        print("=" * 30)
        print("퀴즈 목록")
        print("=" * 30)
        for i, quiz in enumerate(quizzes_to_show):
            print(f"{i + 1}. {quiz['question']}")
            for j, choice in enumerate(quiz["choices"]):
                print(f"   {j + 1}. {choice}")
            print(f"   정답: {quiz['answer']}")
            print()
        print("=" * 30)

    # 점수 확인
    def show_best_score(self):
        print("=" * 30)
        if self.best_score is None:
            print("아직 퀴즈 풀이 기록이 없습니다.")
        else:
            print(f"최고 점수 : {self.best_score}")
        print("=" * 30)

    # 최고 점수 업데이트
    def update_best_score(self, score):
        if self.best_score is None or score > self.best_score:
            self.best_score = score
            self.save_quizzes()
            return True
        return False
