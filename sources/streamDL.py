
import ffmpeg_streaming
from ffmpeg_streaming import Formats, Bitrate, Representation, Size
import requests
import shutil

def download_stream(link: str, out_path: str="./dl/") -> bool:


    video = ffmpeg_streaming.input(link)
    hls = video.hls(Formats.h264())
    _360p  = Representation(Size(640, 360), Bitrate(276 * 1024, 128 * 1024))
    _480p  = Representation(Size(854, 480), Bitrate(750 * 1024, 192 * 1024))
    _720p  = Representation(Size(1280, 720), Bitrate(2048 * 1024, 320 * 1024))

    hls = video.hls(Formats.h264(), hls_time=3600)
    hls.flags('delete_segments')
    hls.representations(_720p)
    hls.output("/mnt/c/Users/anael/OneDrive/projets/streamFinder/dl/test.mp4")
    return True


def download_file(link: str, file: str="test",ext: str="mp4", out_path: str="./dl/") -> bool:
    with requests.get(link, allow_redirects=True, stream=True) as r:
        with open(f"{out_path}{file}.{ext}", 'wb') as f:
            shutil.copyfileobj(r.raw, f)
