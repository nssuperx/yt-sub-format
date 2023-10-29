import sys
import os
import glob
from split_sentence import load_sub, process_text


def main():
    dirname: str = sys.argv[1]

    ttmlfiles = glob.glob(f"{dirname}/**/*.ja.ttml", recursive=True)

    for file in ttmlfiles:
        texts = load_sub(file)
        processed_text = process_text(texts)

        name, _ = os.path.splitext(file)
        outputname = f"{name}.txt"
        with open(outputname, encoding="utf-8", mode="w") as f:
            f.write("\n".join(processed_text))

        print(f"文字数:{sum(len(s) for s in processed_text)} {outputname}")


if __name__ == "__main__":
    main()
