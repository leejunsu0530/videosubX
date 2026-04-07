"""
https://absadiki.github.io/pywhispercpp/#pywhispercpp.constants.PARAMS_SCHEMA
이거 정독 ㄱㄱ.
펼치기 열어보면 유용한 정보 더 나오고
상수 구조들 중요함."""
from pywhispercpp.model import Model
from rich.pretty import pprint
from openvino import Core
import pywhispercpp.utils as pwutils


def check_available_devices_ov() -> list[str]:
    core = Core()
    devices = core.available_devices
    return devices

# d = check_available_devices_ov()
# print(d)


# model = Model(  # 여기 params는 PARAMS_SCHEMA임. 아래 transcribe도 그렇다고 함
#     'base',  # 'large-v3-turbo-q8_0',
#     # use_openvino=True,
#     # openvino_device='CPU',
#     print_realtime=True,
#     print_progress=True,
#     print_timestamps=True,
#     # vad=True,
#     # redirect_whispercpp_logs_to=r"C:\Users\leeju\Projects\videosubX\test\pwcpp\log.txt",
#     n_threads=4
# )

# segments = model.transcribe(
#     r'C:\Users\leeju\Projects\videosubX\test\sample1.mp4',
#     n_processors=4,
#     new_segment_callback=print
# )

# for segment in segments:
# print(segment.text)

# model.get_params() # Returns a dict representation of the actual params
# model.get_params_schema() # A simple link to ::: constants.PARAMS_SCHEMA
# model.lang_max_id()
# model.print_timings()
print("-------------------------system info----------------")
model2 = Model(redirect_whispercpp_logs_to=None)
model2.system_info()  # 이거 아무 출력이 안나오는데 최신 커밋 버그인가? << 아님. 터미널에선 잘 출력됨
# model.available_languages()
# model.auto_detect_language("media", offset_ms=0, n_threads=4)

# pwutils.to_timestamp(376, ".")
# pwutils.output_srt()
