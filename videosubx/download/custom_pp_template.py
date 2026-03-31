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


"""
# https://github.com/yt-dlp/yt-dlp-sample-plugins/blob/master/yt_dlp_plugins/postprocessor/sample.py
# ⚠ Don't use relative imports
from yt_dlp.postprocessor.common import PostProcessor

# ℹ️ See the docstring of yt_dlp.postprocessor.common.PostProcessor

# ⚠ The class name must end in "PP"


class SamplePluginPP(PostProcessor):
    def __init__(self, downloader=None, **kwargs):
        # ⚠ Only kwargs can be passed from the CLI, and all argument values will be string
        # Also, "downloader", "when" and "key" are reserved names
        super().__init__(downloader)
        self._kwargs = kwargs

    # ℹ️ See docstring of yt_dlp.postprocessor.common.PostProcessor.run
    def run(self, info):
        filepath = info.get('filepath')
        if filepath:  # PP was called after download (default)
            self.to_screen(f'Post-processed {filepath!r} with {self._kwargs}')
        else:  # PP was called before actual download
            filepath = info.get('_filename')
            self.to_screen(f'Pre-processed {filepath!r} with {self._kwargs}')
        return [], info  # return list_of_files_to_delete, info_dict
        """
