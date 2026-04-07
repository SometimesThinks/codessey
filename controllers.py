from views import TerminalView


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
        self.view.draw_line()
        # 필터 행렬 B 입력
        self.view.draw_section_title("필터 행렬 B")
        filter_b = self.view.input_matrix(3)
        self.view.draw_line()
        # 패턴 행렬 입력
        self.view.draw_section_title("패턴 행렬")
        pattern = self.view.input_matrix(3)
        self.view.draw_line()

    def run_data_mode(self):
        pass
