package main

import (
	"encoding/xml"
	"fmt"
	"os"
	"os/exec"
	"strings"
)

type Subtitles struct {
	Body struct {
		Div struct {
			Text []string `xml:"p"`
		} `xml:"div"`
	} `xml:"body"`
}

func main() {
	videoId := os.Args[1]

	_, serr := os.Stat(videoId + ".ja.ttml")
	if serr != nil {
		dlSub(videoId)
	}
	f, err := os.ReadFile(videoId + ".ja.ttml")
	if err != nil {
		panic(err)
	}

	result := Subtitles{}

	err = xml.Unmarshal([]byte(string(f)), &result)
	if err != nil {
		panic(err)
	}

	outText := strings.Join(result.Body.Div.Text, "")

	err = os.WriteFile(videoId+".txt", []byte(outText), 0644)
	if err != nil {
		panic(err)
	}
}

func dlSub(videoId string) {
	out, err := exec.Command("powershell", ".\\yt-dlp.exe", "--write-sub", "--sub-lang", "ja", "--sub-format", "ttml", "--skip-download", "--id", videoId).Output()
	if err != nil || strings.Contains(string(out), "There are no subtitles for the requested languages") {
		fmt.Println("自動生成字幕を取得します。")
		_, err = exec.Command("powershell", ".\\yt-dlp.exe", "--write-auto-sub", "--sub-lang", "ja", "--sub-format", "ttml", "--skip-download", "--id", videoId).Output()
	}
	if err != nil {
		fmt.Println(err)
		return
	}
}
