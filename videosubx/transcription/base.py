"""
아래 코드 수정해서 공통 부분만 남김(가비지 컬렉터나 오디오 쪼개서 가져오기, vad 전사 강제정렬 화자분리의 틀 등)
상속이나 base 관련 내용이므로, 삽질하지 않으려면 **class 공부한 후** 만들기"""
from __future__ import annotations
from abc import abstractmethod, ABC
import gc
import torch
from typing import Literal, Optional, Any, Generator, Iterable
from dataclasses import dataclass
from pathlib import Path
import numpy as np
import logging

# 아래 3개의 Base들은 모델 로딩과 처리를 구현.
# 세부적인 부분(vad에서 silero, pyannote, huggingface를 쓰는 각각의 모델들의 기능 구현 등)는 이 Base를 상속해서 구현


class ModelComponentBase(ABC):
    """VAD, Align, Diarize 공통 베이스"""

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


class AlignModelBase(ModelComponentBase):
    @abstractmethod
    def __call__(self, transcription: Any) -> Any:
        pass


class DiarizeModelBase(ModelComponentBase):
    @abstractmethod
    def __call__(self, transcription: Any) -> Any:
        pass


class TranscriberBase(ABC):
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
    # 상속한 엔진 capability 표시용
    MODEL_NAME: Optional[str] = None
    SUPPORTS_ALIGN: bool = False
    SUPPORTS_DIARIZATION: bool = False

    def __init__(self,
                 vad: VadBase | None = None,
                 align_model: AlignModelBase | None = None,
                 diarize_model: DiarizeModelBase | None = None,
                 device: str = "cpu",  # 여기는 상속한 모델들에서 별도로 타입 추가 지정
                 dtype: str = "float32",
                 logger:Optional[logging.Logger]=None,
                 ) -> None:
        self.vad = vad
        self.align_model = align_model
        self.diarize_model = diarize_model

        self.device = device
        self.dtype = dtype

        self._model = None
        self._audio_cache = None

        self.logger = logger or self._default_logger()

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
            1. VAD(true for default, and if you don't use it, sentence can be cut in the middle)
            2. chunking
        """
        # 불러오는 방식을 쪼갤지?
        # 가져온 제너레이터를 self. 변수로 만들기?
        return (i for i in range(10))

    def transcribe(
        self,
        audio_input: str | Path,
        chunk_length_minutes: Optional[float] = None,
    ) -> Generator[Any, None, None]:

        self.logger.info("Start transcription pipeline")

        self._ensure_model_loaded()
        self._ensure_components_loaded()

        audio_gen = self.load_audio(audio_input, chunk_length_minutes)

        for chunk in audio_gen:
            result = self._transcribe_chunk(chunk)

            if self.align_model:
                result = self.align_model(result)

            if self.diarize_model:
                result = self.diarize_model(result)

            yield result

        self._cleanup()

    # =========================
    # Abstract Methods
    # =========================

    @abstractmethod
    def _load_model(self):
        pass

    @abstractmethod
    def _transcribe_chunk(self, audio: np.ndarray) -> Any:
        pass

    # =========================
    # Lazy Loading
    # =========================

    def _ensure_model_loaded(self):
        if self._model is None:
            self.logger.info("Loading model...")
            self._model = self._load_model()

    def _ensure_components_loaded(self):
        for comp in (self.vad, self.align_model, self.diarize_model):
            if comp and not comp.is_loaded:
                self.logger.info(f"Loading component: {comp.__class__.__name__}")
                comp.load()

    # =========================
    # Audio Pipeline
    # =========================

    def load_audio(
        self,
        source: str | Path,
        chunk_length_minutes: Optional[float] = None,
    ) -> Generator[np.ndarray, None, None]:

        stream = self._open_audio(source)

        if self.vad:
            segments = self.vad(stream)
        else:
            segments = self._naive_segment(stream)

        for seg in segments:
            yield from self._chunk_segment(seg, chunk_length_minutes)

    # ---- 세부 단계 ----

    def _open_audio(self, source: str | Path) -> Iterable[np.ndarray]:
        """
        file / url 처리
        (구현 필요)
        """
        raise NotImplementedError

    def _naive_segment(self, stream: Iterable[np.ndarray]) -> Iterable[np.ndarray]:
        """
        VAD 없을 때 fallback
        """
        return stream

    def _chunk_segment(
        self,
        segment: np.ndarray,
        chunk_length_minutes: Optional[float],
    ) -> Generator[np.ndarray, None, None]:

        if chunk_length_minutes is None:
            yield segment
            return

        sr = 16000  # 가정
        chunk_size = int(sr * 60 * chunk_length_minutes)

        for i in range(0, len(segment), chunk_size):
            yield segment[i:i + chunk_size]

    # =========================
    # Utility
    # =========================

    @staticmethod
    def _delete_object(*objects: Any) -> None:
        for obj in objects:
            del obj
        gc.collect()

        try:
            import torch
            torch.cuda.empty_cache()
        except ImportError:
            pass

    def _cleanup(self):
        self.logger.info("Cleaning up memory")
        self._delete_object(self._audio_cache)

    def _default_logger(self) -> logging.Logger:
        logger = logging.getLogger(self.__class__.__name__)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s"
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        logger.setLevel(logging.INFO)
        return logger

    # =========================
    # Properties
    # =========================

    @property
    def is_model_loaded(self) -> bool:
        return self._model is not None



class HFTranscriberBase(TranscriberBase):
    pass


class OVTranscriberBase(HFTranscriberBase):
    pass
