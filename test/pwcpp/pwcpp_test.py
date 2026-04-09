"""
https://absadiki.github.io/pywhispercpp/#pywhispercpp.constants.PARAMS_SCHEMA
이거 정독 ㄱㄱ.
펼치기 열어보면 유용한 정보 더 나오고
상수 구조들 중요함."""
from pywhispercpp.model import Model
from pywhispercpp.utils import output_srt
from rich.pretty import pprint
from openvino import Core
from time import time


def check_available_devices_ov() -> list[str]:
    core = Core()
    devices = core.available_devices
    return devices

# d = check_available_devices_ov()
# print(d)


srt = time()
model = Model(  # 여기 params는 PARAMS_SCHEMA임. 아래 transcribe도 그렇다고 함
    # "base-q5_1",
    # 'large-v3-turbo-q5_0',
    r"C:\Users\leeju\Projects\videosubX\test\pwcpp\ggml-kotoba-whisper-v2.0-q5_0.bin",
    # 지금 n_thread 같은거 4로 해놔서 그런진 모르겠는데 터보나 코토바는 버겁게 돌아감. vs 끄고 다시 시도해봐야 함.

    use_openvino=True,
    openvino_device='GPU',  # 어처피 npu든 gpu든 점유율 안올라간다. hf로 하기

    # 출력 관련 옵션들
    # 기본은 tqdm과 t0=0, t1=140, text=Bella, hello., probability=nan 꼴로 출력
    # >> realtime false, progress true, timestamps true가 기본값인 듯
    # 그리고 상수에 realtime은 사용하지 말라고 권고되어 있었음. (avoid it, use callback instead)
    # print_realtime=True,  # [00:00:00.000 --> 00:00:01.400]   Bella, hello. 출력
    # print_progress=False,  # true가 기본값, tqdm 출력하는 듯
    # print_timestamps=True, # 기본값은 t라는데 왜 바꿔도 뭐가 안달라지냐

    # vad=True,
    # redirect_whispercpp_logs_to=r"C:\Users\leeju\Projects\videosubX\test\pwcpp\log.txt",
    n_threads=4
)

segments = model.transcribe(
    # r'C:\Users\leeju\Projects\videosubX\test\sample1.mp4',
    r"C:\Users\leeju\Desktop\test_15min.mp4",
    n_processors=4,
    new_segment_callback=lambda s: print(f"[{s.t0} --> {s.t1}] {s.text}"),
    language="ja"
)

# for segment in segments:
# print(segment.text)

output_srt(
    segments, r"C:\Users\leeju\Projects\videosubX\test\pwcpp\pwcpp_output.txt")

print(time()-srt)
# model.get_params() # Returns a dict representation of the actual params
# model.get_params_schema() # A simple link to ::: constants.PARAMS_SCHEMA
# model.lang_max_id()
# model.print_timings()
# print("-------------------------system info----------------")
# model2 = Model(redirect_whispercpp_logs_to=None)
# model2.system_info()  # 이거 아무 출력이 안나오는데 최신 커밋 버그인가? << 아님. 터미널에선 잘 출력됨
# model.available_languages()
# model.auto_detect_language("media", offset_ms=0, n_threads=4)

# pwutils.to_timestamp(376, ".")
# pwutils.output_srt()
