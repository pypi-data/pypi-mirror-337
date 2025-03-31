# 정규표현식을 사용해 마크다운 텍스트 내 코드블록을 JSON으로 바꾸기
import re
import json

def load_json(json_str):
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        print(f"JSON decoding 실패: {e}")
        return None

def markdown_to_json(markdown_str):
    # 정규 표현식을 사용하여 JSON 형식을 추출
    pattern = r'```json(.*?)```'
    match = re.search(pattern, markdown_str, flags=re.DOTALL)

    if match:
        json_str = match.group(0)
        json_str = json_str.replace("```json", "").replace("```", "")
        try:
            # 문자열을 JSON 객체로 변환
            json_data = load_json(json_str)
            return json_data
        except json.JSONDecodeError as e:
            print(f"JSON decoding 실패: {e}")
    else:
        print("매치되는 JSON 형식이 없습니다.")
        return None