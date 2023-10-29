import os
import sys
from collections.abc import Generator, Iterable
import xml.etree.ElementTree as ET
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


def load_sub(video_id: str) -> Generator[str]:
    """ttmlファイルを読み込む

    Args:
        video_id (str): VideoID

    Returns:
        list[str]: 字幕1行が要素のgenerator
    """
    ns = {"ttml": "http://www.w3.org/ns/ttml"}
    tree = ET.parse(f"{video_id}.ja.ttml")
    root = tree.getroot()
    return (subtitle.text for subtitle in root.findall("./ttml:body/ttml:div/ttml:p", ns))


def process_text(texts: Iterable[str]) -> list[str]:
    """字幕の文字列(リスト)を適当に整形する

    Args:
        texts (Iterable[str]): 文字列を要素に持つイテラブルオブジェクト

    Returns:
        list[str]: 整形した文字列のリスト
    """
    processed_text: list[str] = []
    oneline: list[str] = []
    for text in texts:
        if text == "[音楽]":
            continue
        oneline.append(text)
        if len(text) > 17:
            continue
        processed_text.append("".join(oneline))
        oneline = []

    return processed_text


def remove_interjection(text: str):
    interjection: tuple[str] = ("なんか", "あの", "えー", "えっと")
    for target in interjection:
        text = text.replace(target, "")
    return text


def main():
    video_id: str = sys.argv[1]

    if not os.path.isfile(f"{video_id}.ja.ttml"):
        dl_sub(video_id)

    texts = load_sub(video_id)
    processed_text = process_text(texts)

    with open(f"{video_id}_sent.txt", encoding="utf-8", mode="w") as f:
        f.write("\n".join(processed_text))

    print(f"文字数:{sum(len(s) for s in processed_text)}")


if __name__ == "__main__":
    main()
