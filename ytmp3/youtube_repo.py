from __future__ import unicode_literals
import youtube_dl
import os
from pathlib import Path
import traceback


class MyLogger(object):
    def debug(self, msg):
        print(msg)

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)

    def info(self, msg):
        print(msg)


class VideoNotAvailableException(Exception):
    pass


class YoutubeRepo:
    DEFAULT_DOWNLOAD_DIRECTORY = os.path.join(Path.home(), "Downloads", "yt_mp3")
    DEFAULT_TMP_DIRECTORY = os.path.join(Path.home(), "Downloads")

    def hook(self, d):
        if d['status'] == 'downloading':
            filename = d['filename']
            downloaded_bytes = d['downloaded_bytes']
            total_bytes = d['total_bytes']
            percent = 100 * downloaded_bytes / total_bytes
            self.log.debug(
                str(filename) + " " +
                str(downloaded_bytes) + "/" + str(total_bytes) +
                " (" + "{0:.2f}".format(percent) + "%)"
            )
        if d['status'] == 'finished':
            self.log.debug('Downloading finished. Begin processing....')

    def __init__(self, download_dir=DEFAULT_DOWNLOAD_DIRECTORY, hooks=None) -> None:
        super().__init__()
        if hooks is None:
            hooks = [self.hook]
        self.log = MyLogger()
        self.hooks = hooks
        self.ydl = youtube_dl.YoutubeDL(self._get_youtube_dl_opts(download_dir))

    def _get_youtube_dl_opts(self, download_dir) -> dict:
        return {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'logger': self.log,
            'progress_hooks': self.hooks,
            'outtmpl': os.path.join(download_dir, '%(title)s.%(ext)s')
        }

    def download_yt_video(self, url):
        try:
            res = self.ydl.download(url)
            self.log.info(str(url) + ": Processing to mp3 finished...")
            return res
        except youtube_dl.utils.DownloadError:
            self.log.info("Couldn't download message")
            traceback.print_exc()
            raise VideoNotAvailableException
        except Exception:
            self.log.info("Got unknown exception")
            traceback.print_exc()
            raise


if __name__ == '__main__':
    yr = YoutubeRepo("/home/przemek/PycharmProjects/ytmp3/ytmp3")
    yr.download_yt_video(['https://www.youtube.com/watch?v=62p0ImadtIg'])
