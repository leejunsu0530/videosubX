from pathlib import Path
import json


def to_path(path: Path | str) -> Path:
    if isinstance(path, str):
        return Path(path)
    else:
        return path


def write_json(path: str | Path, dict_: dict, encoding: str = 'utf-8') -> Path:
    """작성한 파일 경로를 반환"""
    if isinstance(path, str):
        path = Path(path)
    if 'json' not in path.suffix:  # 확장자가 .json으로 끝나지 않으면 json 붙인 새 이름으로 반환
        path = path.with_name(path.name + '.json')
    path.parent.mkdir(parents=True, exist_ok=True)  # path의 폴더를 만들기
    # console.log(f'{path.parent} 생성')
    with path.open('w', encoding=encoding) as file:
        json.dump(dict_, file, ensure_ascii=False, indent=4)
    return path


def read_json(path: str | Path, encoding: str = 'utf-8') -> dict:
    """
    파일이 없을 시 FileNotFoundError 발생
    """
    if isinstance(path, str):
        path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"주어진 경로 {path}에 파일이 없습니다.")
    else:
        with path.open('r', encoding=encoding) as file:
            dict_: dict = json.load(file)
        return dict_
