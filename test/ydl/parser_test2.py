"""나머지 옵션들의 해석, 자동완성 및 변환 구현 방법 고민"""

from yt_dlp import parse_options
# from yt_dlp.options import create_parser # 이건 내가 쓰는 용 아님
from shlex import split as shlex_split  # shlex로 처리해도 딱히 결과에 문제는 없었음
from rich.pretty import pprint

argv = shlex_split('yt-dlp -F "bv+ba" -N 16 "url"')
parser, opts, urls, ydl_opts = parse_options(argv)
# 옵션 설명같은 걸 찾으려면 결국 parser를 써야 함.
# opts는 현 옵션을 반영함. 기본값을 주는건가? 근데 그냥 딕셔너리가 아니었음. 보니까 네임드튜플같은 걸지도? 아래의 ydlopts가 이걸 그대로 딕셔너리로 번역함.
# urls는 ['yt-dlp', 'bv+ba', 'url']가 나왔는데 뭐지?
# ydlopts도 옵션을 줌. 이걸 번역용으로 써도 되나? 기본값이 너무 많이 들어갔긴 한데
#  >> 잘 보니까 기본값 수준이 아니라 모든 옵션의 나열인듯?

# pprint(opts)
pprint(ydl_opts)
