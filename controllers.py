from views import TerminalView
from models import NPUSimulator
from utils import load_json, extract_size_from_key, normalize_label
import statistics


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

        # 입력된 데이터 확인
        self.view.draw_section_title("입력 데이터 확인")
        self.view.display_matrix("필터 A", filter_a)
        self.view.display_matrix("필터 B", filter_b)
        self.view.display_matrix("패턴", pattern)

        # MAC 점수 및 성능 분석
        mac_a, time_a = NPUSimulator(3, filter_a, pattern).analyze_performance()
        mac_b, time_b = NPUSimulator(3, filter_b, pattern).analyze_performance()

        # 평균 연산 시간 계산
        avg_time = statistics.mean([time_a, time_b])
        verdict = NPUSimulator.compare_results(mac_a, mac_b)

        # 통합 결과 출력
        self.view.draw_section_title("MAC 결과")
        self.view.display_result("A 점수", mac_a)
        self.view.display_result("B 점수", mac_b)
        self.view.display_performance(avg_time)
        self.view.display_result("판정", verdict)
        self.view.draw_line()

    def run_data_mode(self):
        # data.json 파일 로드
        data = load_json("data.json")
        if data is None:
            return
        # 전처리: 모든 필터와 패턴 데이터를 float으로 미리 변환
        filters = data.get("filters", {})
        for s_key in filters:
            for f_type in filters[s_key]:
                filters[s_key][f_type] = [
                    [float(v) for v in row] for row in filters[s_key][f_type]
                ]

        patterns = data.get("patterns", {})
        for p_key in patterns:
            if "input" in patterns[p_key]:
                patterns[p_key]["input"] = [
                    [float(v) for v in row] for row in patterns[p_key]["input"]
                ]
        # 필터 로드 상태 출력
        self.view.draw_section_title("1. 필터 로드")
        filters = data.get("filters", {})
        for size_key in sorted(filters.keys(), key=lambda x: int(x.split("_")[1])):
            # 내부 필터 종류 확인 (cross, x)
            available_types = ", ".join(
                [t.capitalize() for t in filters[size_key].keys()]
            )
            self.view.display_loader_status(
                size_key, f"필터 로드 완료 ({available_types})"
            )

        # 3. 패턴 분석 (라벨 정규화 적용)
        self.view.draw_section_title("2. 패턴 분석 (라벨 정규화 적용)")
        patterns = data.get("patterns", {})
        # 각 케이스의 상세 결과 저장({key: p_key, pass: is_pass, status: status, reason: reason})
        results = []
        perf_stats = {}  # 사이즈별 연산 시간 저장 {size: [time1, time2, ...]}

        for p_key in sorted(
            patterns.keys(), key=lambda x: (int(x.split("_")[1]), int(x.split("_")[2]))
        ):
            p_data = patterns[p_key]
            n = extract_size_from_key(p_key)
            expected = normalize_label(p_data.get("expected", ""))
            pattern_matrix = p_data.get("input", [])

            # 필터 찾기
            filter_set_raw = filters.get(f"size_{n}")
            if not filter_set_raw:
                reason = "필터 데이터 없음"
                self.view.display_pattern_analysis(
                    p_key, 0, 0, "-", expected, "FAIL", reason
                )
                results.append(
                    {"key": p_key, "pass": False, "status": "FAIL", "reason": reason}
                )
                continue

            # 필터와 패턴 데이터 가져오기
            filter_cross = filter_set_raw["cross"]
            filter_x = filter_set_raw["x"]
            pattern_matrix = p_data.get("input", [])

            # 사이즈 검증 (n x n 인지 확인)
            if len(pattern_matrix) != n or any(len(row) != n for row in pattern_matrix):
                reason = "규격 불일치"
                self.view.display_pattern_analysis(
                    p_key, 0, 0, "-", expected, "FAIL", reason
                )
                results.append(
                    {"key": p_key, "pass": False, "status": "FAIL", "reason": reason}
                )
                continue

            # MAC 연산 수행 및 시간 측정
            sim_cross = NPUSimulator(n, filter_cross, pattern_matrix)
            sim_x = NPUSimulator(n, filter_x, pattern_matrix)

            score_cross, time_cross = sim_cross.analyze_performance()
            score_x, time_x = sim_x.analyze_performance()

            avg_time = (time_cross + time_x) / 2

            # 사이즈별 성능 통계 저장
            if n not in perf_stats:
                perf_stats[n] = []
            perf_stats[n].append(avg_time)

            # 판정 결과 도출
            raw_verdict = NPUSimulator.compare_results(score_cross, score_x)

            # 판정 상태(Status) 및 예측값 결정
            if raw_verdict == "UNDECIDED":
                prediction = "-"
                is_pass = expected == "UNDECIDED"
                # 기대값이 UNDECIDED인 경우만 PASS
                if is_pass:
                    status = "PASS"
                    reason = ""
                else:
                    status = "FAIL"
                    reason = "동점 발생"
            else:
                if raw_verdict == "A":
                    prediction = "Cross"
                else:
                    prediction = "X"

                is_pass = prediction == expected
                status = "PASS" if is_pass else "FAIL"
                reason = "결과 불일치" if not is_pass else ""

            self.view.display_pattern_analysis(
                p_key, score_cross, score_x, prediction, expected, status, reason
            )
            results.append(
                {"key": p_key, "pass": is_pass, "status": status, "reason": reason}
            )

        # 4. 성능 분석
        self.view.draw_section_title("3. 성능 분석")
        self.view.display_performance_table(perf_stats)

        # 5. 결과 요약
        self.view.draw_section_title("4. 결과 요약")
        pass_cnt = sum(1 for r in results if r["pass"])
        fail_cnt = len(results) - pass_cnt
        failures = [r for r in results if not r["pass"]]

        self.view.display_summary_report(len(results), pass_cnt, fail_cnt, failures)
        self.view.draw_line()
