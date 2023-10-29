from collections.abc import Generator, Iterable
import xml.etree.ElementTree as ET


def load_sub(filename: str) -> Generator[str]:
    """ttmlファイルを読み込む

    Args:
        filename (str): ファイル名

    Returns:
        list[str]: 字幕1行が要素のgenerator
    """
    ns = {"ttml": "http://www.w3.org/ns/ttml"}
    tree = ET.parse(filename)
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
        # [音楽]か何もない空白の時はスキップ(空白はstringではなくNoneTypeになっている)
        if text == "[音楽]" or type(text) is not str:
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
