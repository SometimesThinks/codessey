from utils import smart_input, get_num_input
from constants import BENCHMARK_ITERATIONS


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

    # 행렬 출력 함수
    def display_matrix(self, label, matrix):
        print(f"[{label}]")
        for row in matrix:
            print("  ".join(f"{val:g}" for val in row))
        print()

    # 결과 출력 함수
    def display_result(self, label, value):
        print(f"{label}: {value}")

    # 성능 출력 함수
    def display_performance(self, time_ms):
        print(f"연산 시간(평균/{BENCHMARK_ITERATIONS}회): {time_ms:.6f} ms")

    # 데이터 로드 상태 출력 함수
    def display_loader_status(self, label, status_msg):
        print(f"✓ {label:7} {status_msg}")

    # 패턴 분석 결과 상세 출력
    def display_pattern_analysis(
        self, label, cross_score, x_score, prediction, expected, status, reason=""
    ):
        print(f"--- {label} ---")
        print(f"Cross 점수: {cross_score:g}")
        print(f"X 점수: {x_score:g}")
        final_status = status if not reason else f"{status} ({reason})"
        print(f"판정: {prediction} | 기대값: {expected} | 결과: {final_status}")

    # 전체 성능 분석 표 출력
    def display_performance_table(self, stats):
        print(f"{'크기':<10} {'평균 시간(ms)':<15} {'연산 횟수(N²)':<10}")
        print("-" * 40)
        for n in sorted(stats.keys()):
            avg_time = sum(stats[n]) / len(stats[n])
            print(f"{n:>2}x{n:<7} {avg_time:>12.6f} ms {n*n:>10}")
        print()

    # 최종 결과 요약 출력
    def display_summary_report(self, total, pass_cnt, fail_cnt, failures):
        print(f"총 테스트: {total}개")
        print(f"통과: {pass_cnt}개")
        print(f"실패: {fail_cnt}개")
        if failures:
            print("\n실패 케이스:")
            for f in failures:
                print(f"- {f['key']}: {f['status']}({f['reason']})")

    # 섹션 제목 그리기 함수
    def draw_section_title(self, title):
        self.draw_line()
        print(f"[{title}]")
        self.draw_line()

    # 구분선 그리기 함수
    def draw_line(self):
        print("=" * 30)

    # 보조 구분선
    def draw_sub_line(self):
        print("-" * 30)
