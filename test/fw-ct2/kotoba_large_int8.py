"""
https://huggingface.co/RoachLin/kotoba-whisper-v2.2-faster
"""
from faster_whisper import WhisperModel, BatchedInferencePipeline
from time import time
print("라이브러리 로딩 완료")

MODEL_PATH = r"C:\Users\leeju\Projects\.ct2-workspace\outputs\kotoba-whisper-v2.2-ct2-int8" # 변환시에 내가 설정 하나를 빼먹어서 설정값이 빠짐.
MODEL_ID = "kotoba-tech/kotoba-whisper-v2.0-faster" # 일단 코토바가 turbo보다 배는 빠르다!
FILE = r"C:\Users\leeju\Desktop\test_15min.mp4"
# FILE2 = r"C:\Users\leeju\Desktop\[일본 파스텔] 신주쿠 던전에서 당황한 나나 님... 한일 지하철의 추억 + 쿠키 (한일자막).mkv"
# 샤갈 일본어가 아니잖아

_srt = time()
model = WhisperModel(  # MODEL_PATH,
    MODEL_ID,
    device="cpu", compute_type="int8")
_model_loaded = time()
print(f"모델 로딩: {_model_loaded-_srt:.3f}")

batched_model = BatchedInferencePipeline(model=model)
segments, info = batched_model.transcribe(
    FILE,
    # language="ko",
    batch_size=1, vad_filter=True, log_progress=True)
_end = time()

for segment in segments:
    print(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text} ({segment.avg_logprob})")
print(f"모델 로딩: {_model_loaded - _srt:.3f}\n"
      f"전사 작업: {_end - _model_loaded:.3f}")

# 성능이 예상보다 더 별론데? 파인튜닝 + vad 등 필요할 듯
