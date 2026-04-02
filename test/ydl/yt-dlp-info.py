from yt_dlp import YoutubeDL
from pathlib import Path
import json

# 플레이리스트의 다운로드의 동작 확인을 위해,
# 한쪽은 yt-dlp의 --write-info-json 옵션을 사용하여 자동으로 info.json 파일을 생성하도록 하고,
# 다른 한쪽은 수동으로 정보를 추출해 info.json 파일을 생성하도록 한다.
output = Path('output')
auto_write_dir = output / 'auto_write'
manually_write_dir = output / 'manually_write'
auto_write_no_flat = output / 'auto_write_no_flat'
manually_write_no_flat = output / 'manually_write_no_flat'
for dir_ in [auto_write_dir, manually_write_dir, auto_write_no_flat, manually_write_no_flat]:
    dir_.mkdir(parents=True, exist_ok=True)
URL = "https://www.youtube.com/playlist?list=PLDUgRz_joPOUCB0kBGAM9nVA8LEISGiDi"


def test_case_1():
    ydl_opts = {
        'skip_download': True,
        'writeinfojson': True,
        'extract_flat': 'in_playlist',
        'paths': {'home': str(auto_write_dir)}
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([URL])


def test_case_2():
    ydl_opts = {
        'skip_download': True,
        'extract_flat': 'in_playlist',
        'paths': {'home': str(manually_write_dir)}
    }

    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(URL, download=False)
        info_dict = ydl.sanitize_info(info_dict)

        with (manually_write_dir/f"{info_dict.get("title")}.json").open("w", encoding='utf-8') as f:
            json.dump(info_dict, f, ensure_ascii=False, indent=4)
            print(f"{manually_write_dir/f'{info_dict.get("title")}.json'} is created.")
        ydl.download([URL])


def test_case_3():
    ydl_opts = {
        'skip_download': True,
        'writeinfojson': True,
        # 'extract_flat': 'in_playlist',
        'paths': {'home': str(auto_write_no_flat)}
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([URL])


def test_case_4():
    ydl_opts = {
        'skip_download': True,
        # 'extract_flat': 'in_playlist',
        'paths': {'home': str(manually_write_no_flat)}
    }

    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(URL, download=False)
        info_dict = ydl.sanitize_info(info_dict)
        with (manually_write_no_flat/f"{info_dict.get("title")}.json").open("w", encoding='utf-8') as f:
            json.dump(info_dict, f, ensure_ascii=False, indent=4)
            print(f"{manually_write_no_flat/f'{info_dict.get("title")}.json'} is created.")
        ydl.download([URL])


if __name__ == '__main__':
    test_case_1()
    test_case_2()
    test_case_3()
    test_case_4()
