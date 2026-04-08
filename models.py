import time


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

    # 최적화 후 MAC 연산_1차원 배열
    # def mac_operation_1d(self, filter, pattern):
    #     pass

    # 성능 분석 함수
    def analyze_performance(self, iterations=100):
        start_time = time.perf_counter()

        for _ in range(iterations):
            result = self.mac_operation_2d()

        end_time = time.perf_counter()

        # 전체 소요 시간을 반복 횟수로 나누어 평균 측정 (ms 단위 변환)ㅌㅋ
        avg_time_ms = ((end_time - start_time) / iterations) * 1000

        return result, avg_time_ms
