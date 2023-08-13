import spacy
import yt_dlp
import json
import sys

# https://github.com/yt-dlp/yt-dlp#embedding-yt-dlp


def dl_sub(video_id: str):
    ydl_opts = {
        "skip_download": True,
        "writesubtitles": True,
        "subtitleslangs": ["ja"],
        "subtitlesformat": "json3",
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
            "subtitlesformat": "json3",
            "outtmpl": "%(id)s.%(ext)s",
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            video_info = ydl.extract_info(video_id)

    return video_info


def load_sub(video_id: str):
    subtitle_json: dict = {}
    with open(f"{video_id}.ja.json3", encoding="utf-8") as f:
        subtitle_json = json.load(f)

    return [e["segs"] for e in subtitle_json["events"] if "segs" in e]


def preprocess(events: list[dict]) -> str:
    # この処理のところでいろいろやる
    text = []
    ignore_newline = False
    for event in events:
        segs_text = "".join(t["utf8"] for t in event)
        if len(segs_text) > 17 and segs_text != "\n":
            ignore_newline = True
        if segs_text == "\n" and ignore_newline:
            ignore_newline = False
            continue
        text.append(segs_text)

    # text = "".join(utf8["utf8"] for event in events for utf8 in event)
    text = "".join(text)
    processed_text = text

    # 単語以外で必要ないもの
    # unnecessary_str: tuple[str] = ("[音楽]", "\n")
    unnecessary_str: tuple[str] = ("[音楽]\n", "[音楽]")
    for s in unnecessary_str:
        processed_text = processed_text.replace(s, "")

    return processed_text


def remove_interjection(text: str):
    interjection: tuple[str] = ("なんか", "あの", "えー", "えっと")
    for target in interjection:
        text = text.replace(target, "")
    return text


def split_sentence(processed_text: str):
    str_limit = 16500
    split_text = [
        processed_text[x : x + str_limit] for x in range(0, len(processed_text), str_limit)
    ]

    nlp = spacy.load("ja_ginza")

    docs = []
    for text in split_text:
        docs.append(nlp(text))

    sents: list[str] = []
    for doc in docs:
        for sent in doc.sents:
            sents.append(f"{sent.text}\n")
    return sents


def main():
    video_id: str = sys.argv[1]

    video_info = dl_sub(video_id)

    events = load_sub(video_id)
    processed_text = preprocess(events)

    # processed_text = remove_interjection(processed_text)
    # sents = split_sentence(processed_text)

    with open(f"{video_id}_sent.txt", encoding="utf-8", mode="w") as f:
        f.writelines(processed_text)

    print(f"文字数:{sum(len(s) for s in processed_text)}")


if __name__ == "__main__":
    main()
