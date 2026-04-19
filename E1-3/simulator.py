import time
from constants import BENCHMARK_ITERATIONS, EPSILON


# MAC 연산_2차원 배열(N^2)
def mac_operation(n, filter, pattern):
    result = 0
    for r in range(n):
        for c in range(n):
            result += filter[r][c] * pattern[r][c]
    return result


# 두 MAC 점수를 비교하여 판정 결과를 반환
def compare_results(first_score, second_score):
    if abs(first_score - second_score) < EPSILON:
        return "UNDECIDED"
    if first_score > second_score:
        return "FIRST"
    return "SECOND"


# 성능 분석 함수
def analyze_performance(n, filter, pattern, iterations=BENCHMARK_ITERATIONS):
    start_time = time.perf_counter()
    for _ in range(iterations):
        result = mac_operation(n, filter, pattern)
    end_time = time.perf_counter()
    # 전체 소요 시간을 반복 횟수로 나누어 평균 측정 (ms 단위 변환)
    avg_time_ms = ((end_time - start_time) / iterations) * 1000
    return result, avg_time_ms
