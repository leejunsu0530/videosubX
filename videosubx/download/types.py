from typing import TypeAlias, Any, Literal

InfoDict: TypeAlias = dict[str, Any]  # 키는 알바 아니고 그냥 이름만 다른 딕셔너리
# CliOpt: TypeAlias = str  # 이게 필요할까?
# YdlOpts: TypeAlias = dict[str, Any] # 이게 필요할까2

PPWhen = {  # 구조 변경 필요. gpt 참고
    "pre_process": "after video extraction",
    "after_filter": "after video passes filter",
    "video": "after --format; before --print/--output",
    "before_dl": "before each video download",
    "post_process": "after each video download; default",
    "after_move": "after moving the video file to its final location",
    "after_video": "after downloading and processing all formats of a video",
    "playlist": "at end of playlist"
}
