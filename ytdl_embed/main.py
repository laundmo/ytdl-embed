from flask import Flask, redirect, render_template, request, url_for, jsonify
from flask.helpers import send_from_directory
import youtube_dl
import time
import hashlib
from pathlib import Path

def generate_hash(text):
    hasher = hashlib.sha1(text.encode("utf-8"))
    return hasher.hexdigest()[:10]

app = Flask(__name__)

cache_folder = Path(app.root_path) / "cache"

def render_embed(url):
    return render_template(
        "embed.html", mp4=url, current_url=request.url
    )

# testing only
# @app.route('/mp4/<path:path>')
# def send_mp4(path):
#     return send_from_directory("cache", path)

@app.route("/")
def hello_world():
    url = request.query_string.decode("utf-8")
    filename = generate_hash(url) + ".mp4"
    path = cache_folder / filename
    lockfile = path.parent / (path.name + '.lock')
    if not any([path.exists(), lockfile.exists()]):
        lockfile.touch()
        with youtube_dl.YoutubeDL(
            {
                "outtmpl": str(path),
                'prefer_ffmpeg': True,
                "postprocessors": [
                    {"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}
                ],
            }
        ) as ydl:
            ydl.download([url])
        lockfile.unlink()
    time.sleep(1)
    return render_embed(f"/mp4/" + filename)


if __name__ == "__main__":
    app.run()
