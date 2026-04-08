from utils import smart_input, get_num_input


class TerminalView:
    def __init__(self):
        pass

    # 모드 선택 함수
    def display_menu(self):
        print("=" * 30)
        print("[모드 선택]")
        print("1. 사용자 입력(3x3)")
        print("2. data.json 데이터 분석")
        print("=" * 30)
        mode = get_num_input("원하는 모드를 선택하세요: ", 1, 2)
        return mode

    # 행렬 입력 함수
    def input_matrix(self, n):
        matrix = []
        print(f"{n}개의 숫자를 한 줄에 공백으로 구분하여 입력하세요.")
        # 행 입력
        for i in range(n):
            while True:
                try:
                    line = list(map(float, smart_input(f"{i + 1}번째 행: ").split()))
                    # 개수 체크
                    if len(line) != n:
                        print(f"{n}개의 숫자를 입력해야 합니다.")
                        continue
                    # 모든 숫자가 float이면 통과
                    matrix.append(line)
                    break
                except ValueError:
                    print("숫자로만 구성된 행을 입력해야 합니다.")
        return matrix

    # 결과 출력 함수
    def display_result(self, label, value):
        print(f"{label}: {value}")

    # 성능 출력 함수
    def display_performance(self, label, time_ms):
        print(f"[{label}] 평균 연산 시간: {time_ms:.6f} ms")

    # 구분선 그리기 함수
    def draw_line(self):
        print("=" * 30)

    # 섹션 제목 그리기 함수
    def draw_section_title(self, title):
        self.draw_line()
        print(f"[{title}]")
        self.draw_line()
