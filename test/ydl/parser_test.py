from yt_dlp.options import create_parser
from yt_dlp import parse_options
import sys
import optparse
from rich.pretty import pprint

if __name__ == "__main__":
    # parser = create_parser()
    parser = parse_options().parser
    # do = parser.get_option_group("Download Options")
    # print(do.title)
    # for group in parser.option_groups:
        # print(group.title)

    opt = parser.get_option("-N")
    # formatter = parser.formatter
    optparse.HelpFormatter.expand_default()
    print(opt.help)
    print(opt.metavar)

    # 깃허브 설명에 가능한 것들 목록이 나타나는 것?
    # 메타var가 있는것들 분석(여러개가 있다던지)
    # -t 옵션 내가 불러올 수 있음? 왜 help에 뜨고 여긴 안뜸
