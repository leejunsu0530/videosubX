"""
# 그냥 yt-dlp의 일반적인 옵션 > 다운로드 방식 선택하기 or 파일 다운로드 및 내가 관리하기

TODO:
ytdlp의 인자들은 -h로 보여줄 수 있는데, 이건 argpase로 구현되고 init의 main 함수에 있음.
마찬가지로 init에서 parse_options라는 함수가 있음. 아래의 해석 함수에서 참고.

"""
import yt_dlp
from typing import Literal


def download_youtube(urls: list[str],
                     ydl_opts: dict | str,
                     postprocessors: dict[yt_dlp.postprocessor.PostProcessor,
                                          Literal["pre_process",
                                                  "after_filter",
                                                  "video",
                                                  "before_dl",
                                                  "post_process",
                                                  "after_move",
                                                  "after_video",
                                                  "playlist"]] = None) -> Literal[0, 1]:
    if isinstance(ydl_opts, str):
        ydl_opts = return_cli_to_api(ydl_opts)

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        if postprocessors is not None:
            for pp, when in postprocessors.items():
                ydl.add_post_processor(pp, when)
        error_code: Literal[0, 1] = ydl.download(urls)
    return error_code


class DownloadManager:
    def __init__(self):
        pass

class DownloadFromFile(DownloadManager):
    pass

    # 파일 위치 지정시 파일로 저장하는 함수
    # 파일의 포메팅 여부 선택(PP로는 파일 접근이 안돼서 구현이 어려울거니까 파이썬으로)
    # 파일을 통해 다운로드 시도 및 실패시 별도 처리