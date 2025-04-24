from flask import Flask, request, jsonify, redirect
import yt_dlp

app = Flask(__name__)
PORT = 8000

SUPPORTED_PLATFORMS = {
    "youtube.com": {"name": "YouTube", "cookies": True},
    "youtu.be": {"name": "YouTube", "cookies": True},
    "instagram.com": {"name": "Instagram", "cookies": False},
    "tiktok.com": {"name": "TikTok", "cookies": False},
    "snapchat.com": {"name": "Snapchat", "cookies": False}
}

DEVELOPER = {
    "name": "Ansh",
    "project": "Multi Video Downloader API",
    "github": "https://github.com/unknown",
    "telegram": "@cyber_ansh"
}

@app.route("/")
def home():
    return jsonify({
        "message": "Welcome to Multi Video Downloader API",
        "credit": "t.me/AnshAPi"
    })

@app.route("/available")
def available():
    return jsonify({
        "supported_platforms": [
            {
                "name": v["name"],
                "url_pattern": k,
                "cookies": v["cookies"]
            } for k, v in SUPPORTED_PLATFORMS.items()
        ],
        "developer": DEVELOPER
    })

@app.route("/info")
def info():
    url = request.args.get("url")
    if not url or not any(p in url for p in SUPPORTED_PLATFORMS):
        return jsonify({"error": "Unsupported platform or invalid URL"}), 400

    ydl_opts = {
        "quiet": True,
        "dump_single_json": True,
        "cookiefile": "cookies.txt" if "youtube.com" in url or "youtu.be" in url else None
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            return jsonify(info_dict)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/download")
def download():
    url = request.args.get("url")
    quality = request.args.get("quality", "best")
    audio_only = request.args.get("audio", "false").lower() == "true"

    if not url or not any(p in url for p in SUPPORTED_PLATFORMS):
        return jsonify({"error": "Unsupported platform"}), 400

    ydl_opts = {
        "format": "bestaudio/best" if audio_only else quality,
        "quiet": True,
        "noplaylist": True,
        "cookiefile": "cookies.txt" if "youtube.com" in url or "youtu.be" in url else None,
        "outtmpl": "%(title)s.%(ext)s"
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            direct_url = info_dict.get("url", "")
            return redirect(direct_url)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
