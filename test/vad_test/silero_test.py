from silero_vad import load_silero_vad, read_audio, get_speech_timestamps
from rich.pretty import pprint
from time import time

srt = time()
model = load_silero_vad()
wav = read_audio('sample1.mp4')
speech_timestamps = get_speech_timestamps(
    wav,
    model,
    # Return speech timestamps in seconds (default is samples)
    return_seconds=True,
)
pprint(speech_timestamps)
print(time() - srt)