"""
아래 코드 수정해서 공통 부분만 남김(가비지 컬렉터나 오디오 쪼개서 가져오기, vad 전사 강제정렬 화자분리의 틀 등)
상속이나 base 관련 내용이므로, 삽질하지 않으려면 **class 공부한 후** 만들기"""

import gc
import torch
import platform
import subprocess
from typing import Literal, Optional, Any, Generator
from dataclasses import dataclass
from pathlib import Path
import numpy as np


# class VadConfig:
    # pass
    # device = torch.device("NPU")
    # 인텔 gpu는 되는데 npu는 안해줌

class TranscriberBase:
    """
    공통적인 부분:
    - 모델 다운로드, 양자화 처리
    - 오디오 청킹 및 불러오기(파일로 하든 제너레이터+온라인에서 끊어서 가져오기로 하든)
    - vad, 전사, 화자구분, 강제정렬의 일련의 과정 틀 잡아놓기(사용자가 원하는 거 넣을 수 있도록?)
    - 가비지 컬렉터 부분
    - 로깅 부분?
    - ov base도 만들고, 변환 후 저장해서 다음에는 그거로 불러오게 하기


    어디부터 어디까지를 클래스 변수로 하고 어디를 인스턴스 변수로 할지?
    """

    def __init__(self,
                #  vad_config: VadConfig
                 ) -> None:
        pass

    @staticmethod
    def _delete_object(*objects: Any) -> None:
        for obj in objects:
            del obj
        gc.collect()
        torch.cuda.empty_cache()

    def load_audio(self,
                   audio_path_or_url: str | Path,
                   use_vad: bool = True,
                   chunk_length_minutes: Optional[float] = None
                   ) -> Generator[np.ndarray, None, None]:
        """
        You can use path(string or pathlib.Path) or url(string)
        it will process 
            1. VAD(default, but if you don't use it, sentence can be cut in the middle), 
            chunking, 
            and return a generator of audio chunks as numpy arrays.
        """
        # 불러오는 방식을 쪼갤지?
        # 가져온 제너레이터를 self. 변수로 만들기?

    def get_audio_duration(self):
        pass

    # def download_model(self):
        # pass

    def transcribe(self):
        pass

    def asr(self):
        pass

    def align(self):
        pass

    def diarize(self):
        pass


class TranscriberBaseOV(TranscriberBase):
    pass


class VadBase:
    pass


class AlignModelBase:
    pass


class DiraizeModelBase:
    pass
