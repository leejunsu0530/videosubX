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


def parse_cli_args(cli_args: str, cli_defaults=False) -> dict[str, object]:
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


# def highlight_cli(cli_args: str) -> str:
#     """return highlighted html string of CLI arguments"""
#     return ""


def highlight_dict(api_opts: dict[str, object], pretty: bool = True) -> str:
    """return highlighted html string of API options"""
    return ""


def parse_opts():
    """가능한 옵션들과 설명, 자료형 등을 반환"""


# def parse_outtmpl():
#     """%(title)s.%(ext)s와 같은 출력 템플릿을 분석
#     값 채워넣기(미리보기에 쓰거나 Path 업데이트에 사용)는 별도로"""
