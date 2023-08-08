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

    oneline: list[str] = []
    for event in subtitle_json["events"]:
        if "segs" in event:
            for seg in event["segs"]:
                oneline.append(seg.get("utf8", ""))

    return "".join(oneline)


def preprocess(text: str) -> str:
    processed_text = text
    # 単語以外で必要ないもの
    unnecessary_str: tuple[str] = ("[音楽]", "\n")
    for s in unnecessary_str:
        processed_text = processed_text.replace(s, "")

    # 間投詞, 感嘆詞
    interjection: tuple[str] = ("なんか", "あの", "えー", "えっと")
    for target in interjection:
        processed_text = processed_text.replace(target, "")
    return processed_text


def main():
    video_id: str = sys.argv[1]

    # video_info = dl_sub(video_id)

    oneline = load_sub(video_id)
    processed_text = preprocess(oneline)

    str_limit = 16500
    split_text = [processed_text[x : x + str_limit] for x in range(0, len(processed_text), str_limit)]

    nlp = spacy.load("ja_ginza")

    docs = []
    for text in split_text:
        docs.append(nlp(text))

    sents: list[str] = []
    for doc in docs:
        for sent in doc.sents:
            sents.append(f"{sent.text}\n")

    with open(f"{video_id}_sent.txt", encoding="utf-8", mode="w") as f:
        f.writelines(sents)

    print(f"文字数:{sum(list(map(lambda s: len(s), sents)))}")


if __name__ == "__main__":
    main()
