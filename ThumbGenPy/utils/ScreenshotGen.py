import os
import requests
import random
import cv2
import random
import m3u8


def get_json(url):
    i = 0
    while i < 5:
        i += 1
        try:
            r = requests.get(url)
            data = r.json()
            return data
        except:
            print("Retrying", i, url)
            continue


def get_better_quality(p):
    qualities = []
    for pos in range(len(p.playlists), 0, -1):
        i = p.playlists[pos - 1]
        quality = i.stream_info.resolution[1]

        if quality == 720:
            return i.absolute_uri

        if quality < 720:
            qualities.append(i.absolute_uri)

    return qualities[0]


def get_random_ts(url, large):
    playlist = m3u8.load(url)
    if large:
        playlist = m3u8.load(get_better_quality(playlist))
    else:
        playlist = m3u8.load(playlist.playlists[0].absolute_uri)

    t = len(playlist.segments)
    x = t // 4
    random_number = random.randint(x, (x * 3) - 1)
    input_file = playlist.segments[random_number].absolute_uri
    return input_file


def convertToScreenshot1(url, large):
    file = get_random_ts(url, large)

    cam = cv2.VideoCapture(file)
    ret, frame = cam.read()
    cam.release()

    while True:
        if ret:
            _, img_encoded = cv2.imencode(".jpg", frame)
            img_bytes = img_encoded.tobytes()
            break
        else:
            continue

    return img_bytes


def convertToScreenshot2(url):
    host = "/".join(url.split("/")[:-1]) + "/"
    r = requests.get(url)
    lines = r.text.split("\n")

    ts = []
    for line in lines:
        line = line.strip(" \n")
        if not line.endswith(","):
            ts.append(host + line)

    total = len(ts)

    x = total // 4
    ts = ts[x : x * 3]

    file = random.choice(ts)
    print(file)

    cam = cv2.VideoCapture(file)
    ret, frame = cam.read()
    cam.release()

    while True:
        if ret:
            _, img_encoded = cv2.imencode(".jpg", frame)
            img_bytes = img_encoded.tobytes()
            break
        else:
            continue

    return img_bytes


def get_screenshot(episodeid, large):
    url = (
        f"https://animedexapi-private-124143.techzbots1.workers.dev/episode/{episodeid}"
    )
    data = get_json(url)
    url = data["results"]["stream"]["sources"][0]["file"]
    try:
        return convertToScreenshot1(url, large)
    except:
        return convertToScreenshot2(url)
