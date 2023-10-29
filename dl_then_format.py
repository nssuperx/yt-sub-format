import os
import sys
from dl_sub import dl_sub
from split_sentence import load_sub, process_text


def main():
    video_id: str = sys.argv[1]

    if not os.path.isfile(f"{video_id}.ja.ttml"):
        dl_sub(video_id)

    texts = load_sub(f"{video_id}.ja.ttml")
    processed_text = process_text(texts)

    with open(f"{video_id}_sent.txt", encoding="utf-8", mode="w") as f:
        f.write("\n".join(processed_text))

    print(f"文字数:{sum(len(s) for s in processed_text)}")


if __name__ == "__main__":
    main()
