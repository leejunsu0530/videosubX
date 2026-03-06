# pylint: disable=wrong-import-position
import warnings  # surpress torchaudio deprecation warning
from importlib.metadata import version, PackageNotFoundError
from rich.console import Console
from time import time
from pathlib import Path
import os
from shutil import which

console = Console()

print("[Note] torchaudio._backend.list_audio_backends deprecation warning is suppressed.")
warnings.filterwarnings("ignore", category=UserWarning,
                        message=".*torchaudio._backend.list_audio_backends has been deprecated.*")

# 임시로 로딩과 시간 부분을 추가. 나중에는 로딩 로깅으로 수정.
# srt = time()
# with console.status("[bold green]Importing videosubX...") as status:
#     from .transcription.transcribe import WhisperXTranscriber  # noqa: E402
# print(f"videosubX imported in {time() - srt:.2f} seconds.")

# ffmpeg 경로 추가 후 whisperx.vad 임포트
ffmpeg_bin_path = Path(which("ffmpeg")).parent
if ffmpeg_bin_path is None:
    raise RuntimeError("ffmpeg is not installed or not found in PATH.")
os.add_dll_directory(str(ffmpeg_bin_path))
from .transcription.transcribe import WhisperXTranscriber  # noqa: E402

# versioning
try:
    __version__ = version("videosubX")  # pyproject.toml의 name과 일치시킬 것
except PackageNotFoundError:  # 빌드 실패시
    __version__ = "0.0.0.dev0"


__all__ = ["WhisperXTranscriber"]


def main():
    pass
