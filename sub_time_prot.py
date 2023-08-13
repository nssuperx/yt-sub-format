import json
from typing import NamedTuple
import matplotlib.pyplot as plt
import numpy as np


class Subtitle(NamedTuple):
    tStartMs: int
    dDurationMs: int
    segs: list[dict]


VIDEOID = "videoid"


def main():
    video_id: str = VIDEOID
    subtitle_json: dict = {}
    with open(f"{video_id}.ja.json3", encoding="utf-8") as f:
        subtitle_json = json.load(f)

    events: list[Subtitle] = []
    newline_events: list[Subtitle] = []
    for event in subtitle_json["events"]:
        if "segs" in event and len(event["segs"]) == 1 and event["segs"][0]["utf8"] == "\n":
            newline_events.append(
                Subtitle(
                    event.get("tStartMs", 0), event.get("dDurationMs", 0), event.get("segs", [])
                )
            )
        else:
            events.append(
                Subtitle(
                    event.get("tStartMs", 0), event.get("dDurationMs", 0), event.get("segs", [])
                )
            )

    startMs = np.array(tuple(e.tStartMs for e in events), dtype=np.int32)
    durationMs = np.array(tuple(e.dDurationMs for e in events), dtype=np.int32)
    segs_len = np.array(tuple(len(e.segs) for e in events), dtype=np.int32)
    str_size = np.array(tuple(len("".join(s["utf8"] for s in e.segs)) for e in events), dtype=np.int32)
    nl_durationMs = np.array(tuple(e.dDurationMs for e in newline_events), dtype=np.int32)
    # print(f"text lines: {startMs.size}, newlines: {nl_durationMs.size}")
    startMs_diff = startMs[1:] - startMs[:-1]
    next_sub_time = (startMs[1:-1] + durationMs[1:-1]) - startMs[2:]
    fig = plt.figure()
    ax1 = fig.subplots()
    ax2 = ax1.twinx()
    # ax1.plot(durationMs[20:-20])
    # ax2.plot(segs_len[20:-20], color=(1.0, 0, 0, 0.5))
    ax1.plot(str_size[20:-20])
    ax2.plot(segs_len[20:-20], color=(1.0, 0, 0, 0.5))
    # ax1.bar(range(0, startMs_diff.size*2, 2), startMs_diff)
    # ax2.bar(range(1, (durationMs.size-1)*2, 2), durationMs[1:], color="orange")
    plt.show()


if __name__ == "__main__":
    main()
