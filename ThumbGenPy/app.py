from flask import Flask, Response, request, redirect
from utils.ImageResizer import resize_image
from utils.ScreenshotGen import get_screenshot
from utils.PostImageHandler import Upload_To_Postman, get_postman_urls
import os

app = Flask(__name__)


@app.route("/gen/<episodeId>", methods=["GET", "POST", "HEAD"])
def gen(episodeId):
    if request.method == "HEAD":
        return Response(
            status=200, headers={"Content-type": "image/jpg", "Content-Length": "0"}
        )

    else:
        size = episodeId.split("_")[-1]
        episodeId = episodeId.replace(size, "").strip("_ ")
        if size == "large":
            image = get_screenshot(episodeId, True)
        else:
            image = get_screenshot(episodeId, False)
            image = resize_image(image, 300, 300)

        return Response(
            image,
            mimetype="image/jpg",
            status=200,
            content_type="image/jpg",
        )


@app.route("/")
def home():
    return "Hello, World!"


@app.route("/upload/<episodeId>")
def upload(episodeId):
    url = f"https://dwuofx75gdsahgfshafh21y5srrvtx6sxg6693pdru.vercel.app/gen/{episodeId}_large"
    link = Upload_To_Postman(url)
    x = link.split("/")
    link = "/".join(x[:-1])
    data = get_postman_urls(link)

    return {"medium": data[0], "large": data[1]}


@app.route("/thumb/<episodeId>")
def thumbnail(episodeId):
    url = f"https://dwuofx75gdsahgfshafh21y5srrvtx6sxg6693pdru.vercel.app/gen/{episodeId}_thumb"
    link = Upload_To_Postman(url)
    x = link.split("/")
    link = "/".join(x[:-1])
    data = get_postman_urls(link)
    return {"thumb": data[1]}
