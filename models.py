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
