from ytmp3 import youtube_repo
import re


class WrongUrlException(RuntimeError):
    pass


class YtMp3Service:
    YOUTUBE_ID_REGEX = "(?<=v\=)([a-zA-Z0-9_-]{11})"

    def __init__(self) -> None:
        super().__init__()
        self.yr = youtube_repo.YoutubeRepo()

    def download_video(self, url):
        video_url = [self.process_url(u) for u in (url if isinstance(url, list) else [url])]
        return self.yr.download_yt_video(video_url)

    @staticmethod
    def process_url(url):
        m = re.search(YtMp3Service.YOUTUBE_ID_REGEX, url)
        if not m:
            raise WrongUrlException("Proceeded url is not valid")
        found = m.group(1)
        return "https://www.youtube.com/watch?v=" + found

    def set_download_dir(self, download_dir):
        self.yr = youtube_repo.YoutubeRepo(download_dir)


if __name__ == '__main__':
    s = YtMp3Service()
    s.set_download_dir("/home/przemek/PycharmProjects/ytmp3/ytmp3")
    s.download_video("https://www.youtube.com/watch?v=gQAGMaoCxyw&list=PLBuBGiqkjCzUstBUg2hH_ViTQCMoxAKyQ")
