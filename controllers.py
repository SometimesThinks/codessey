from cli import (
    display_menu,
    input_matrix,
    display_matrix,
    display_result,
    display_performance,
    display_pattern_analysis,
    display_performance_table,
    display_summary_report,
    display_loader_status,
    draw_section_title,
    draw_line,
    draw_sub_line,
)
from models import NPUSimulator
from utils import load_json, extract_size_from_key, normalize_label
import statistics


class Controller:
    def __init__(self):
        pass

    def run(self):
        mode = display_menu()
        if mode == "1":
            self.run_user_mode()
        elif mode == "2":
            self.run_data_mode()

    # 사용자 입력 모드
    def run_user_mode(self):
        # 필터 행렬 A 입력
        draw_section_title("필터 행렬 A")
        filter_a = input_matrix(3)
        # 필터 행렬 B 입력
        draw_section_title("필터 행렬 B")
        filter_b = input_matrix(3)
        # 패턴 행렬 입력
        draw_section_title("패턴 행렬")
        pattern = input_matrix(3)

        # 입력된 데이터 확인
        draw_section_title("입력 데이터 확인")
        display_matrix("필터 A", filter_a)
        display_matrix("필터 B", filter_b)
        display_matrix("패턴", pattern)

        # MAC 점수 및 성능 분석
        mac_a, time_a = NPUSimulator(3, filter_a, pattern).analyze_performance()
        mac_b, time_b = NPUSimulator(3, filter_b, pattern).analyze_performance()

        # 평균 연산 시간 계산
        avg_time = statistics.mean([time_a, time_b])
        verdict = NPUSimulator.compare_results(mac_a, mac_b)

        if verdict == "UNDECIDED":
            verdict_str = "판정 불가(동점 발생)"
        else:
            verdict_str = verdict

        # 통합 결과 출력
        draw_section_title("MAC 결과")
        display_result("A 점수", mac_a)
        display_result("B 점수", mac_b)
        display_performance(avg_time)
        display_result("판정", verdict_str)
        draw_line()

    # data.json 데이터 분석 모드
    def run_data_mode(self):
        # 0. 데이터 로드 및 전처리
        data = self._load_and_preprocess()
        if data is None:
            return

        # 1. 필터 로드 상태 출력
        self._display_loader_status(data.get("filters", {}))

        # 2. 일괄 패턴 분석 수행
        results, perf_stats = self._execute_batch_simulations(
            data.get("filters", {}), data.get("patterns", {})
        )

        # 3. 성능 분석 결과 출력
        draw_section_title("3. 성능 분석")
        display_performance_table(perf_stats)

        # 4. 전체 결과 요약 출력
        draw_section_title("4. 결과 요약")
        pass_cnt = sum(1 for r in results if r["pass"])
        fail_cnt = len(results) - pass_cnt
        failures = [r for r in results if not r["pass"]]

        display_summary_report(len(results), pass_cnt, fail_cnt, failures)
        draw_line()

    # 데이터 로드 및 float 전처리
    def _load_and_preprocess(self):
        data = load_json("data.json")
        if data is None:
            return None

        # 모든 필터 데이터를 float으로 미리 변환
        filters = data.get("filters", {})
        for s_key in filters:
            for f_type in filters[s_key]:
                filters[s_key][f_type] = [
                    [float(v) for v in row] for row in filters[s_key][f_type]
                ]

        # 모든 패턴 데이터를 float으로 미리 변환
        patterns = data.get("patterns", {})
        for p_key in patterns:
            if "input" in patterns[p_key]:
                patterns[p_key]["input"] = [
                    [float(v) for v in row] for row in patterns[p_key]["input"]
                ]
        return data

    # 필터 로드 상태 출력
    def _display_loader_status(self, filters):
        draw_section_title("1. 필터 로드")
        for size_key in sorted(filters.keys(), key=lambda x: int(x.split("_")[1])):
            available_types = ", ".join(
                [t.capitalize() for t in filters[size_key].keys()]
            )
            display_loader_status(size_key, f"필터 로드 완료 ({available_types})")

    # 일괄 패턴 분석 실행 및 결과 수집
    def _execute_batch_simulations(self, filters, patterns):
        draw_section_title("2. 패턴 분석 (라벨 정규화 적용)")
        results = []
        perf_stats = {}

        for p_key in sorted(
            patterns.keys(), key=lambda x: (int(x.split("_")[1]), int(x.split("_")[2]))
        ):
            p_data = patterns[p_key]
            n = extract_size_from_key(p_key)
            expected = normalize_label(p_data.get("expected", ""))
            pattern_matrix = p_data.get("input", [])

            # 필터 찾기
            filter_set = filters.get(f"size_{n}")
            if not filter_set:
                reason = "필터 데이터 없음"
                display_pattern_analysis(p_key, 0.0, 0.0, "-", expected, "FAIL", reason)
                results.append(
                    {"key": p_key, "pass": False, "status": "FAIL", "reason": reason}
                )
                continue

            # 사이즈 검증
            if len(pattern_matrix) != n or any(len(row) != n for row in pattern_matrix):
                reason = "규격 불일치"
                display_pattern_analysis(p_key, 0.0, 0.0, "-", expected, "FAIL", reason)
                results.append(
                    {"key": p_key, "pass": False, "status": "FAIL", "reason": reason}
                )
                continue

            # MAC 연산 및 시간 측정
            sim_cross = NPUSimulator(n, filter_set["cross"], pattern_matrix)
            sim_x = NPUSimulator(n, filter_set["x"], pattern_matrix)

            score_cross, time_cross = sim_cross.analyze_performance()
            score_x, time_x = sim_x.analyze_performance()
            avg_time = (time_cross + time_x) / 2

            # 성능 기록
            if n not in perf_stats:
                perf_stats[n] = []
            perf_stats[n].append(avg_time)

            # 판정 및 결과 분석
            raw_v = NPUSimulator.compare_results(score_cross, score_x)
            prediction, is_pass, status, reason = self._evaluate_verdict(
                raw_v, expected
            )

            # 출력 및 결과 저장
            display_pattern_analysis(
                p_key, score_cross, score_x, prediction, expected, status, reason
            )
            results.append(
                {"key": p_key, "pass": is_pass, "status": status, "reason": reason}
            )

        return results, perf_stats

    # 판정 결과 평가 함수
    def _evaluate_verdict(self, raw_verdict, expected):
        if raw_verdict == "UNDECIDED":
            prediction = "UNDECIDED"
            is_pass = expected == "UNDECIDED"
            if is_pass:
                return prediction, True, "PASS", ""
            else:
                return prediction, False, "FAIL", "동점 발생"
        else:
            prediction = "Cross" if raw_verdict == "A" else "X"
            is_pass = prediction == expected
            status = "PASS" if is_pass else "FAIL"
            reason = "" if is_pass else "결과 불일치"
            return prediction, is_pass, status, reason
