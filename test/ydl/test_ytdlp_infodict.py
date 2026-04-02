"""
- 엘범 등은 또 다름. 여기 인자가 flat이어도 되는지 체크
- 속도 빠르게 하는 방법
- 플리 다운로드를 영상으로 쪼개는 법
- flat과 일반, 플리 키 비교

- json 정렬하는법
"""
import yt_dlp  # type: ignore
from pathlib import Path
import json

infodict_folder = Path("infodict_folder")

PL_URL = "https://www.youtube.com/playlist?list=PLDUgRz_joPOUCB0kBGAM9nVA8LEISGiDi"
CH_URL = "https://www.youtube.com/@vs-bi8bi"
VID_URL = "https://youtu.be/FMn6hSMNXZQ"

testcase = {
    "플리": PL_URL,
    "채널": CH_URL,
    "비디오": VID_URL,
    "플리_flat": PL_URL,
    "채널_flat": CH_URL
}

for file, url in testcase.items():
    if "flat" in file:
        ydl_opts = {'skip_download': True, 'extract_flat': 'in_playlist'}
    else:
        ydl_opts = {}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        out = infodict_folder / f"{file}.info.json"
        out.parent.mkdir(exist_ok=True, parents=True)

        info_dict = ydl.extract_info(url, download=False)
        info_dict = ydl.sanitize_info(info_dict)
        out.write_text(str(info_dict), encoding="utf-8")

    # yt-dlp의 --write-info-json은 다름. 이것도 체크 필요
with yt_dlp.YoutubeDL() as ydl:
    pass
