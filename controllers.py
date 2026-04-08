from views import TerminalView
from models import NPUSimulator


class Controller:
    def __init__(self):
        self.view = TerminalView()

    def run(self):
        mode = self.view.display_menu()
        if mode == "1":
            self.run_user_mode()
        elif mode == "2":
            self.run_data_mode()

    def run_user_mode(self):
        # 필터 행렬 A 입력
        self.view.draw_section_title("필터 행렬 A")
        filter_a = self.view.input_matrix(3)
        # 필터 행렬 B 입력
        self.view.draw_section_title("필터 행렬 B")
        filter_b = self.view.input_matrix(3)
        # 패턴 행렬 입력
        self.view.draw_section_title("패턴 행렬")
        pattern = self.view.input_matrix(3)
        # MAC 점수 및 성능 분석
        mac_a, time_a = NPUSimulator(3, filter_a, pattern).analyze_performance()
        mac_b, time_b = NPUSimulator(3, filter_b, pattern).analyze_performance()
        # MAC 점수 결과 출력
        self.view.draw_section_title("MAC 결과")
        self.view.display_result("[필터 A] MAC 점수", mac_a)
        self.view.display_performance("필터 A", time_a)
        self.view.display_result("[필터 B] MAC 점수", mac_b)
        self.view.display_performance("필터 B", time_b)
        # 판정 결과 출력
        verdict = NPUSimulator.compare_results(mac_a, mac_b)
        self.view.display_result("최종 판정", verdict)
        self.view.draw_line()

    def run_data_mode(self):
        pass
