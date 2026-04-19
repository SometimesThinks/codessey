import cli
import simulator
from dataset import load_and_preprocess, extract_size_from_key, normalize_label
import statistics


def run():
    mode = cli.display_menu()
    if mode == "1":
        run_user_mode()
    elif mode == "2":
        run_data_mode()


# 사용자 입력 모드
def run_user_mode():
    # 필터 행렬 A 입력
    cli.draw_section_title("필터 행렬 A")
    filter_a = cli.input_matrix(3)
    # 필터 행렬 B 입력
    cli.draw_section_title("필터 행렬 B")
    filter_b = cli.input_matrix(3)
    # 패턴 행렬 입력
    cli.draw_section_title("패턴 행렬")
    pattern = cli.input_matrix(3)

    # 입력된 데이터 확인
    cli.draw_section_title("입력 데이터 확인")
    cli.display_matrix("필터 A", filter_a)
    cli.display_matrix("필터 B", filter_b)
    cli.display_matrix("패턴", pattern)

    # MAC 점수 및 성능 분석
    mac_a, time_a = simulator.analyze_performance(3, filter_a, pattern)
    mac_b, time_b = simulator.analyze_performance(3, filter_b, pattern)

    # 평균 연산 시간 계산
    avg_time = statistics.mean([time_a, time_b])
    verdict = format_user_verdict(simulator.compare_results(mac_a, mac_b))

    # 통합 결과 출력
    cli.draw_section_title("MAC 결과")
    cli.display_result("A 점수", mac_a)
    cli.display_result("B 점수", mac_b)
    cli.display_performance(avg_time)
    cli.display_result("판정", verdict)
    cli.draw_line()


# data.json 데이터 분석 모드
def run_data_mode():
    # 0. 데이터 로드 및 전처리
    data = load_and_preprocess("data.json")
    if data is None:
        return

    # 1. 필터 로드 상태 출력
    cli.display_filter_load_status(data.get("filters", {}))

    # 2. 일괄 패턴 분석 수행
    results, perf_stats = execute_batch_simulations(
        data.get("filters", {}), data.get("patterns", {})
    )

    # 3. 성능 분석 결과 출력
    cli.draw_section_title("3. 성능 분석")
    cli.display_performance_table(perf_stats)

    # 4. 전체 결과 요약 출력
    cli.draw_section_title("4. 결과 요약")
    pass_cnt = sum(1 for r in results if r["status"] == "PASS")
    fail_cnt = len(results) - pass_cnt
    failures = [r for r in results if r["status"] == "FAIL"]

    cli.display_summary_report(len(results), pass_cnt, fail_cnt, failures)
    cli.draw_line()


# 일괄 패턴 분석 실행 및 결과 수집
def execute_batch_simulations(filters, patterns):
    cli.draw_section_title("2. 패턴 분석 (라벨 정규화 적용)")
    # results: [{"key": 패턴 키, "status": PASS/FAIL, "reason": 실패 사유}]
    results = []
    # perf_stats: {행렬 크기 N: [해당 크기 패턴들의 평균 연산 시간(ms), ...]}
    perf_stats = {}

    for p_key in sorted(
        patterns.keys(), key=lambda x: (int(x.split("_")[1]), int(x.split("_")[2]))
    ):
        # 패턴 데이터 추출
        p_data = patterns[p_key]
        # 패턴 키에서 행렬 크기 추출
        n = extract_size_from_key(p_key)
        # 기대값 정규화
        expected = normalize_label(p_data.get("expected", ""))
        # 패턴 행렬 추출
        pattern_matrix = p_data.get("input", [])

        # 검증: 필터 존재 여부 확인
        filter_set = filters.get(f"size_{n}")
        if not filter_set:
            record_failed_pattern(results, p_key, expected, "필터 데이터 없음")
            continue

        # 검증: 패턴 및 필터 행렬 크기 확인
        if len(pattern_matrix) != n or any(len(row) != n for row in pattern_matrix):
            record_failed_pattern(results, p_key, expected, "규격 불일치")
            continue

        # MAC 연산 및 시간 측정
        score_cross, time_cross = simulator.analyze_performance(
            n, filter_set["cross"], pattern_matrix
        )
        score_x, time_x = simulator.analyze_performance(
            n, filter_set["x"], pattern_matrix
        )
        avg_time = (time_cross + time_x) / 2

        # 성능 기록
        if n not in perf_stats:
            perf_stats[n] = []
        perf_stats[n].append(avg_time)

        # 판정 및 결과 분석
        raw_v = simulator.compare_results(score_cross, score_x)
        prediction, status, reason = evaluate_verdict(raw_v, expected)

        # 출력 및 결과 저장
        cli.display_pattern_analysis(
            p_key, score_cross, score_x, prediction, expected, status, reason
        )
        results.append({"key": p_key, "status": status, "reason": reason})

    return results, perf_stats


# 실패한 패턴 기록 함수
def record_failed_pattern(results, pattern_key, expected, reason):
    cli.display_pattern_analysis(pattern_key, 0.0, 0.0, "-", expected, "FAIL", reason)
    # 실패 케이스도 results에 동일한 형태로 저장해 최종 요약 계산에 사용
    results.append({"key": pattern_key, "status": "FAIL", "reason": reason})


# 판정 결과 평가 함수
def evaluate_verdict(raw_verdict, expected):
    if raw_verdict == "UNDECIDED":
        prediction = "UNDECIDED"
        if expected == "UNDECIDED":
            return prediction, "PASS", ""
        return prediction, "FAIL", "동점 발생"

    prediction = format_data_verdict(raw_verdict)
    if prediction == expected:
        return prediction, "PASS", ""
    return prediction, "FAIL", "결과 불일치"


# 사용자 입력 모드 판정명 변경 함수
def format_user_verdict(verdict):
    if verdict == "FIRST":
        return "A"
    if verdict == "SECOND":
        return "B"
    return "판정 불가(동점 발생)"


# data.json 분석 모드 판정명 변경 함수
def format_data_verdict(verdict):
    if verdict == "FIRST":
        return "Cross"
    if verdict == "SECOND":
        return "X"
    return "UNDECIDED"
