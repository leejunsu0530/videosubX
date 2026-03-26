from enum import Enum
from typing import TypeAlias, Any, Literal

InfoDict: TypeAlias = dict[str, Any]  # 키는 알바 아니고 그냥 이름만 다른 딕셔너리

# 결국 별로 의미는 없는데 복잡해질 뿐이라 이건 안하기로 함.
# CliOpt: TypeAlias = str  # 이게 필요할까?
# YdlOpts: TypeAlias = dict[str, Any] # 이게 필요할까2

class PPWhen(str, Enum):
    PRE_PROCESS = ("pre_process", "after video extraction")
    AFTER_FILTER = ("after_filter", "after video passes filter")
    VIDEO = ("video", "after --format; before --print/--output")
    BEFORE_DL = ("before_dl", "before each video download")
    POST_PROCESS = ("post_process", "after each video download; default")
    AFTER_MOVE = ("after_move", "after moving the video file to its final location")
    AFTER_VIDEO = ("after_video", "after downloading and processing all formats of a video")
    PLAYLIST = ("playlist", "at end of playlist")

    def __new__(cls, value: str, description: str):
        obj = str.__new__(cls, value)
        obj._value_ = value
        obj.description = description
        return obj

    @classmethod
    def is_valid(cls, value: str) -> bool:
        try:
            cls(value)
            return True
        except ValueError:
            return False

    @classmethod
    def values(cls) -> list[str]:
        return [e.value for e in cls]

    @classmethod
    def items(cls) -> list[tuple[str, str]]:
        return [(e.value, e.description) for e in cls]



if __name__ == '__main__':
    def test(when: PPWhen):
        ...
    test(PPWhen.PRE_PROCESS)
    test("pre_process")
    str(PPWhen.PRE_PROCESS) == PPWhen.POST_PROCESS.value
    print(PPWhen.PRE_PROCESS.description)
    PPWhen("pre_process")
