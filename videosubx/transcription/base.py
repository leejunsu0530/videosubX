"""
아래 코드 수정해서 공통 부분만 남김(가비지 컬렉터나 오디오 쪼개서 가져오기, vad 전사 강제정렬 화자분리의 틀 등)
상속이나 base 관련 내용이므로, 삽질하지 않으려면 **class 공부한 후** 만들기"""
from __future__ import annotations
from abc import abstractmethod, ABC
import gc
import torch
from typing import Type, Literal, Optional, Any, Generator, Iterable
from dataclasses import dataclass
from pathlib import Path
import numpy as np
import logging
from ..utils.types import ParameterSpec


@dataclass(slots=True)
class AudioSegment:
    audio: np.ndarray
    start: float
    end: float
    sample_rate: int


@dataclass(slots=True)  # 값 추가는 안할거지만, 나중에 나오는 값 보면서 구조 바꿔야할지도 모름
class TranscriptedSegment:
    text: str
    start: float
    end: float
    confidence: float | None = None
    speaker: str | None = None


class ModelComponentBase(ABC):
    """VAD, Align, Diarize 공통 베이스"""
    CONFIG_SCHEMA = {}

    def __init__(self, config: dict | None = None):
        self.config = config or {}
        self._model = None

    @abstractmethod
    def load(self):
        pass

    @abstractmethod
    def __call__(self, *args, **kwargs):
        pass

    @property
    def is_loaded(self) -> bool:
        return self._model is not None


class VadBase(ModelComponentBase):

    @abstractmethod
    def __call__(self, audio_stream: Iterable[np.ndarray]) -> Iterable[np.ndarray]:
        pass


class AsrBase:
    pass


class AlignModelBase(ModelComponentBase):
    @abstractmethod
    def __call__(self, transcription: Any) -> Any:
        pass


class DiarizeModelBase(ModelComponentBase):
    @abstractmethod
    def __call__(self, transcription: Any) -> Any:
        pass


class TranscribePipeline:
    pass


"""
파생 transcriber들의 엔진:
- whisperx
- faster-whisper(whisperx에서 다른 모델을 불러올 수 있으면 wx에서 같이 처리)
- pywhispercpp(whisper.cpp의 파이썬 바인딩)
- huggingface의 whisper 모델(파인튜닝된 모델, 양자화 모델 포함)
    - 양자화 기능은 HFTranscriberBase에서 처리
    - OVTranscriber(HFTranscriberBase)는 자동으로 모델 OV로 변환 및 저장, 양자화를 지원 

기능 담당: 공통적인 부분
- 모델 다운로드 및 로드
- 오디오 청킹 및 불러오기(파일 또는 온라인 상에서 청킹한 부분만큼씩 가져오는 제너레이터로 메모리 및 연산 절약)
- vad, 전사, 화자 구분, 강제정렬의 일련의 과정 수행
- 가비지 컬렉터
- 로깅
"""
