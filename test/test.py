# from yt_dlp import YoutubeDL
# from videosubx.download.parse import parse_cli_args
# from rich.pretty import pprint

# with YoutubeDL() as ydl:
#     api_opts = parse_cli_args(
#         '--format "bv[height<=720]+ba" --output "%(title)s.%(ext)s"')
#     pprint(api_opts)
#     # ydl.prepare_outtmpl()
#     # ydl.parse_outtmpl()
from rich.console import Console
print("코드 실행됨")

console = Console()
with console.status("[bold green]Importing videosubX...") as status:
    print("whisperx")
    import whisperx
    print("vad")
    from whisperx.vads import Vad
    # print("schema")
    # from whisperx.schema import AlignedTranscriptionResult, TranscriptionResult
    # print("utils")
    # from whisperx.utils import LANGUAGES, optional_int, str2bool
    # print("diarize")
    # from whisperx.diarize import DiarizationPipeline
