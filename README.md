# yt-sub-format
YouTubeの字幕をダウンロードしていろいろする。

## 目標のコマンド

```powershell
.\yt-dlp.exe --write-auto-sub --sub-lang ja --sub-format ttml --skip-download <VideoId>
.\yt-dlp.exe --write-sub --sub-lang ja --sub-format ttml --skip-download <VideoId>
```

## やってること

* 適当に文字列つなげて改行

### 改行のやり方
話者が話していない時に改行したい。

元の字幕を見ると、改行されているタイミングは

* 文字数が多くなってきたとき
* 話者が話していないとき
  * 改行か、`[音楽]`という文字列が入れられている

上記の、「文字数が多くなってきたとき」だけ改行せずに次の字幕とつなげれば、大体、いい感じの文章になる。
