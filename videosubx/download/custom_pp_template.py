"""This is template of PostProcessor. 
When you write what you want and save, you will be able to import it in downloading page."""

import yt_dlp

# ℹ️ See help(yt_dlp.postprocessor.PostProcessor)


class MyCustomPP(yt_dlp.postprocessor.PostProcessor):
    def __init__(self, downloader=None):
        super().__init__(downloader=downloader)
        # ℹ️ You can add your own initialization code here

    def run(self, info):
        # self.to_screen('Doing stuff')
        return [], info


"""이 이하는 나중에 지우기"""
# with yt_dlp.YoutubeDL() as ydl:
# ℹ️ "when" can take any value in yt_dlp.utils.POSTPROCESS_WHEN
# ydl.add_post_processor(MyCustomPP(), when='pre_process')
# ydl.download(URLS)
