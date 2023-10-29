import yt_dlp

# https://github.com/yt-dlp/yt-dlp#embedding-yt-dlp


def dl_sub(video_id: str):
    ydl_opts = {
        "skip_download": True,
        "writesubtitles": True,
        "subtitleslangs": ["ja"],
        "subtitlesformat": "ttml",
        "outtmpl": "%(id)s.%(ext)s",
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        video_info = ydl.extract_info(video_id)

    if len(video_info["requested_subtitles"]) == 0:
        print("auto sub")
        ydl_opts = {
            "skip_download": True,
            "writeautomaticsub": True,
            "subtitleslangs": ["ja"],
            "subtitlesformat": "ttml",
            "outtmpl": "%(id)s.%(ext)s",
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            video_info = ydl.extract_info(video_id)

    return video_info
