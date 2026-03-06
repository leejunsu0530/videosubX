from yt_dlp import YoutubeDL
# from videosubx.download.parse import parse_cli_args
from rich.pretty import pprint
#
with YoutubeDL() as ydl:
    # api_opts = parse_cli_args(
    # '--format "bv[height<=720]+ba" --output "%(title)s.%(ext)s"')
    # pprint(api_opts)
    info_dict = {
        "title": "Example Video",
        "ext": "mp4",
    }
    outtmpl = "%(title)s.%(ext)s"
    print(ydl.evaluate_outtmpl(outtmpl, info_dict))
    # ydl.parse_outtmpl()
