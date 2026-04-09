import json


# json 파일 로드 함수
def load_json(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"{file_path} 파일이 존재하지 않습니다.")
        return None
    except json.JSONDecodeError:
        print(f"{file_path} 파일 형식이 올바르지 않습니다.")
        return None


# 데이터 로드 및 전처리 함수
def load_and_preprocess(file_path):
    data = load_json(file_path)
    if data is None:
        return None
    # 필터 데이터 float으로 전처리
    filters = data.get("filters", {})
    for size_key in filters:
        for filter_type in filters[size_key]:
            filters[size_key][filter_type] = [
                [float(value) for value in row]
                for row in filters[size_key][filter_type]
            ]

    # 패턴 데이터 float으로 전처리
    patterns = data.get("patterns", {})
    for pattern_key in patterns:
        if "input" in patterns[pattern_key]:
            patterns[pattern_key]["input"] = [
                [float(value) for value in row]
                for row in patterns[pattern_key]["input"]
            ]
    return data


# 라벨 정규화 함수
def normalize_label(label):
    label = str(label).lower().strip()
    if label in ["+", "cross"]:
        return "Cross"
    if label in ["x"]:
        return "X"
    if label in ["undecided", "undecided_status"]:
        return "UNDECIDED"
    return label


# 키에서 사이즈 추출 함수
def extract_size_from_key(key):
    try:
        return int(key.split("_")[1])
    except (IndexError, ValueError):
        return None
