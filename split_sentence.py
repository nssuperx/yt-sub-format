import spacy
import sys

def main():
    video_id: str = sys.argv[1]

    raw_text = ""
    with open(f"{video_id}.txt", encoding="utf-8") as f:
        raw_text = f.read()

    raw_text = raw_text.replace("[音楽]", "。")

    str_limit = 16500
    split_raw_text =  [raw_text[x:x+str_limit] for x in range(0, len(raw_text), str_limit)]

    nlp = spacy.load("ja_ginza")

    docs = []
    for text in split_raw_text:
        docs.append(nlp(text))

    sents: list[str] = []
    for doc in docs:
        for sent in doc.sents:
            sents.append(f"{sent.text}\n")
            
    with open(f"{video_id}_sent.txt", encoding="utf-8", mode="w") as f:
        f.writelines(sents)
    

if __name__=="__main__":
    main()
