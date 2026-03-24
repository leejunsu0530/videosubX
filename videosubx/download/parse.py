"""
사용자의 cli 옵션 해석, 도움말 출력, 구문 강조를 처리

Note that part of the code is from https://github.com/yt-dlp/yt-dlp/blob/master/devscripts/cli_to_api.py
Last commit was at Aug 7, 2025

TODO:
몽키패치 수정 - 어쩌면 전체를 클래스나 함수로 묶어서 지역변수로 만들어버리면?
"""
# Allow direct execution
import yt_dlp
import yt_dlp.options
from shlex import split as shlex_split  # shlex로 처리해도 딱히 결과에 문제는 없었음
from pprint import pformat
from rich.pretty import pprint, Pretty
from .types import InfoDict

_create_parser = yt_dlp.options.create_parser


def _parse_patched_options(opts):
    patched_parser = _create_parser()
    patched_parser.defaults.update({
        'ignoreerrors': False,
        'retries': 0,
        'fragment_retries': 0,
        'extract_flat': False,
        'concat_playlist': 'never',
        'update_self': False,
    })
    yt_dlp.options.create_parser = lambda: patched_parser
    try:
        return yt_dlp.parse_options(opts)
    finally:
        yt_dlp.options.create_parser = _create_parser


_default_opts = _parse_patched_options([]).ydl_opts


def _cli_to_api(opts, cli_defaults=False):
    opts = (yt_dlp.parse_options if cli_defaults else _parse_patched_options)(
        opts).ydl_opts

    diff = {k: v for k, v in opts.items() if _default_opts[k] != v}
    if 'postprocessors' in diff:
        diff['postprocessors'] = [pp for pp in diff['postprocessors']
                                  if pp not in _default_opts['postprocessors']]
    return diff


# def highlight_cli(cli_args: str) -> str:
#     """return highlighted html string of CLI arguments"""
#     return ""


def cli_to_api(cli_args: str, cli_defaults=False) -> dict[str, object]:
    """
    Args:
        args: A string of CLI arguments, e.g. "yt-dlp --format "bv[height<=720]+ba" --output '%(title)s.%(ext)s' URL". 'yt-dlp' can be omitted.
    Returns:
        A dictionary of API options that correspond to the given CLI arguments, e.g. {'format': 'bv[height<=720]+ba', 'output': '%(title)s.%(ext)s'}.
    """
    if not cli_args.startswith('yt-dlp '):
        cli_args = 'yt-dlp ' + cli_args
    api = _cli_to_api(shlex_split(cli_args), cli_defaults=cli_defaults)
    return api


def highlight_dict(ydl_opts: dict[str, object], pretty: bool = True) -> str:
    """return highlighted html string of API options"""
    return ""


class YdlOptHelper:
    """넣은 값에 따라 옵션을 찾아줌. 그리고 그 옵션의 여러 값들을 알려줌
    """

    def __init__(self):
        """일련의 그룹명, 옵션들과 설명(즉, 띄울 최소 정보)을 딕셔너리 쌍으로 해서 가져옴. 
        대조한 후 필요할 때마다(유저가 옵션 검색뿐만 아니라 옵션을 실제로 목록에 넣었을 때) 나머지 metavars 등까지 파서에서 불러옴."""
        self.parser = None

    def find_option_from_name(self, user_input: str, consider_capital: bool = False):
        """
        입력한 내용으로 시작하는 것을 먼저 출력하고, 그게 중간에 들어가는 것 등을 그 아래에 출력
        Args:
            user_input: 유저가 입력한 옵션의 일부
            consider_capital: 대소문자 구분을 신경쓸지 여부
        """

    def find_option_from_keyword(self, user_input: str):
        """입력한 내용이 포함된 help를 가진 옵션들을 출력"""

    def show_output_template(self, outtmpl: str, info_dict: InfoDict):
        """값을 넣어서 완성된 출력 템플릿 예시를 보여줌"""

    def get_option_parser(self, option_name: str):
        """말 그대로 옵션의 파서를 불러옴."""
    
    def get_option_info(self, option_name:str):
        """"""
        parser = self.get_option_parser(option_name)
        return {
            "help": parser.help
        }