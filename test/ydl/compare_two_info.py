import json
from pathlib import Path
from typing import Any
# from rich.pretty import pprint
from pandas import DataFrame

output = Path(r"C:\Users\leeju\Projects\videosubX\test\output")


def read_dict_from_json(path: Path) -> dict[Any, Any]:
    # """딕셔너리 반환. 존재 안하면 빈 딕셔너리"""
    if not str(path).endswith(".json"):
        path = Path(str(path)+".json")

    if not path.exists():
        # return None
        raise FileNotFoundError(f"해당 위치({str(path)})에 파일이 없습니다.")

    with path.open("r", encoding='utf-8') as json_file:
        info_dict: dict = json.load(json_file)
    return info_dict

# 두 파일에서 플리 제외 다른 거 확인


title = "2시간 실험해서 단 10초만 볼 수 있는 경이로운 현상.. (성공확률 14%)"
id_ = "5LaheFrkDjA"
auto_write_no_flat = read_dict_from_json(
    output/"auto_write_no_flat"/f"{title} [{id_}].info.json")
manual_write_no_flat = read_dict_from_json(
    output/"manually_write_no_flat"/"문과&이과").get('entries', [])[0]

# 실제 해야 할 테스트는 저 둘의 키와 벨류 비교. 이건 그냥 보여주기용
# df_auto = DataFrame(auto_write_no_flat)
# df_manual = DataFrame(manual_write_no_flat)
# df_auto.head()
# df_manual.head()
print(auto_write_no_flat.keys())
print(manual_write_no_flat.keys())