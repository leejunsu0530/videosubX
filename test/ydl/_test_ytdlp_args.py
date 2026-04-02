# ytdlp 인자 파싱 및 이걸 변환하는 부분 테스트
"""
이미 있는 cli에서 파싱해오기.
whisperx는 아마 필요없고(내가 직접 구현할거니까), ytdlp는 업뎃이 자주있어서 gui모드에 자동 파싱이 필요.
방법 자체는 안어려울듯
"""
from yt_dlp import parse_options
import optparse
from pprint import pprint


"""
1. option_list
    이건 파서에 직접 속한 Option 객체들의 평면 리스트야.
    포함되는 것
    - parser.add_option(...)으로 추가한 옵션
    - 기본 옵션 (-h / --help)
    - ❌ OptionGroup에 들어간 옵션은 포함 안 됨
    구조: 
    Option
    ├─ _short_opts   (-m)
    ├─ _long_opts    (--model)
    ├─ action        ('store')
    ├─ dest          ('model')
    ├─ default       ('small')
    ├─ type          ('string')
    ├─ help          (설명 문자열)
    ├─ choices       (선택지)
    └─ metavar       (표시 이름)

2. option_groups
    -h 출력의 각 섹션을 그대로 표현한 구조
    각 그룹 구조:
    OptionGroup
    ├─ title        (섹션 제목)
    ├─ description  (선택)
    └─ option_list  (Option 리스트)

3. 자주 쓰는 필드명
| 정보     | 접근 방법                               |
| ------ | ----------------------------------- |
| 옵션 이름  | `opt._short_opts`, `opt._long_opts` |
| 저장 변수명 | `opt.dest`                          |
| 기본값    | `opt.default`                       |
| 타입     | `opt.type`                          |
| 선택지    | `opt.choices`                       |
| 설명     | `opt.help`                          |
| 표시 이름  | `opt.metavar`                       |

"""

parser, opts, urls, ydl_opts = parse_options([])
group_cnt = 0
total_cnt = 0

with open("ytdlp-opts.md", "w",encoding='utf=8') as f:
    for group in parser.option_groups:
        group_cnt += 1
        print(f"# {group_cnt}. {group.title}: {len(group.option_list)}개 옵션", file=f)
        # pprint(group.__dict__)
        # break
        for in_group_idx, option in enumerate(group.option_list):
            total_cnt += 1
            print(
                f"## {total_cnt} ({group_cnt}-{in_group_idx+1}): {option}", 
                f"- short: {option._short_opts}",
                f"- long: {option._long_opts}",
                f"- dest(저장변수명): {option.dest}", 
                f"- default: {option.default}", 
                f"- type: {option.type}",
                f"- choices: {option.choices}",
                f"- help: {option.help}",
                f"- metavar(표시 이름): {option.metavar}",
                sep="\n", end="---\n\n", file=f
                )

print("옵션 정보가 ytdlp-opts.md에 저장되었습니다.")
