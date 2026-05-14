import json
from pathlib import Path

output = Path(r"C:\Users\leeju\Projects\videosubX\test\output")

def read_dict_from_json(parent_path: str, file_name: str) -> dict:
    """딕셔너리 반환. 존재 안하면 빈 딕셔너리"""
    file_path = f"{parent_path}\\{file_name}" if file_name.split(".")[-1] == "json" \
        else f"{parent_path}\\{file_name}.json"
    if not os.path.exists(file_path):
        return {}
    else:  # 존재하면 읽어오기
        with open(file_path, 'r', encoding='utf-8') as json_file:
            info_dict: dict = json.load(json_file)
        return info_dict
    
# 두 파일에서 플리 제외 다른 거 확인