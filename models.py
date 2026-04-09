import time
from constants import BENCHMARK_ITERATIONS, EPSILON


class NPUSimulator:
    def __init__(self, n, filter, pattern):
        self.n = n
        self.filter = filter
        self.pattern = pattern

    # 최적화 전 MAC 연산_2차원 배열
    def mac_operation_2d(self):
        result = 0
        for r in range(self.n):
            for c in range(self.n):
                result += self.filter[r][c] * self.pattern[r][c]
        return result

    # 성능 분석 함수
    def analyze_performance(self, iterations=BENCHMARK_ITERATIONS):
        start_time = time.perf_counter()
        for _ in range(iterations):
            result = self.mac_operation_2d()
        end_time = time.perf_counter()
        # 전체 소요 시간을 반복 횟수로 나누어 평균 측정 (ms 단위 변환)
        avg_time_ms = ((end_time - start_time) / iterations) * 1000
        return result, avg_time_ms

    # 두 MAC 점수를 비교하여 판정 결과를 반환
    @staticmethod
    def compare_results(mac_a, mac_b):
        if abs(mac_a - mac_b) < EPSILON:
            return "UNDECIDED"
        elif mac_a > mac_b:
            return "A"
        else:
            return "B"
