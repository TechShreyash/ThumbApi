import json, requests, secrets, string, re
from bs4 import BeautifulSoup
from datetime import datetime
import urllib.parse


def session(length):
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for i in range(length))


def Upload_To_Postman(file_url):
    # GET NECESSARY KEYS
    _session_upload = int(datetime.now().timestamp() * 1000)
    _session = requests.get("https://postimages.org/web")
    _session_time = datetime.now()
    _session_time = _session_time.strftime("%d/%m/%Y,%H:%M:%S")
    _ui = [24, 1600, 900, "true", "", "", _session_time]

    _upload_session = session(32)
    _soup = BeautifulSoup(_session.text, "html.parser")

    # EXTRACT KEY
    data = _soup.find_all("script")[-1].get_text()
    pattern = r"\b\w{40}\b"
    match = re.search(pattern, data)
    _token = match.group()

    # UPLOAD HEADERS
    headers = {
        "Origin": "https://postimages.org/web",
        "Referer": "https://postimages.org/web",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
    }

    _data = {
        "token": _token,
        "upload_session": _upload_session,
        "url": file_url,
        "numfiles": 1,
        "gallery": "",
        "ui": _ui,
        "optsize": 0,
        "expire": 0,
        "session_upload": _session_upload,
    }
    # PARSE DICT TO PARAM FORM
    _data = urllib.parse.urlencode(_data)
    _data = urllib.parse.unquote(_data)

    # UPLOAD THE IMAGE
    _upload = requests.post(
        "https://postimages.org/json/rr", headers=headers, data=_data
    )
    data = _upload.json()
    print(data)
    return data['url']


# Upload_To_Postman('https://thumb-gen-py.vercel.app/gen/kuroko-no-basket-2nd-season-dub-episode-3_thumb')


def get_postman_urls(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    img1 = soup.find("img", {"id": "main-image"}).get("src")
    img2 = soup.find("a", {"id": "download"}).get("href").split("?")[0]

    return img1, img2


# print(get_postman_urls("https://postimg.cc/hJbJd2hP"))
