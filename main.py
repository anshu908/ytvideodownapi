from flask import Flask, request, jsonify, send_file
import yt_dlp
import uuid
import os

app = Flask(__name__)
COOKIES_FILE = "cookies.txt"

DEVELOPER = {
    "name": "Anshu",
    "project": "Multi Video Downloader API",
    "github": "https://github.com/cyber-ansh",
    "telegram": "@cyber_ansh"
}

SUPPORTED_PLATFORMS = {
    "youtube": {
        "name": "YouTube",
        "url_pattern": "youtube.com",
        "cookies": True
    },
    "instagram": {
        "name": "Instagram",
        "url_pattern": "instagram.com",
        "cookies": False
    },
    "tiktok": {
        "name": "TikTok",
        "url_pattern": "tiktok.com",
        "cookies": False
    },
    "snapchat": {
        "name": "Snapchat",
        "url_pattern": "snapchat.com",
        "cookies": False
    }
}

@app.route("/")
def home():
    return jsonify({
        "message": "Welcome to Multi Video Downloader API",
        "endpoints": ["/available", "/info", "/download"],
        "developer": DEVELOPER
    })


@app.route("/available", methods=["GET"])
def available():
    return jsonify({
        "supported_platforms": list(SUPPORTED_PLATFORMS.values()),
        "developer": DEVELOPER
    })


@app.route("/info", methods=["GET"])
def get_info():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "Missing URL"}), 400

    if "youtube.com" not in url:
        return jsonify({"error": "Info only available for YouTube"}), 400

    ydl_opts = {
        "cookiefile": COOKIES_FILE,
        "quiet": True,
        "skip_download": True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = [
                {
                    "format_id": f["format_id"],
                    "ext": f.get("ext"),
                    "resolution": f.get("resolution"),
                    "format_note": f.get("format_note"),
                    "filesize": f.get("filesize")
                }
                for f in info.get("formats", [])
                if f.get("filesize")
            ]
            return jsonify({
                "title": info.get("title"),
                "thumbnail": info.get("thumbnail"),
                "uploader": info.get("uploader"),
                "formats": formats
            })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/download", methods=["GET"])
def download():
    url = request.args.get("url")
    quality = request.args.get("quality", "best")
    audio = request.args.get("audio", "false").lower() == "true"

    if not url:
        return jsonify({"error": "Missing URL"}), 400

    # Detect platform
    use_cookies = False
    for platform in SUPPORTED_PLATFORMS.values():
        if platform["url_pattern"] in url:
            use_cookies = platform["cookies"]
            break
    else:
        return jsonify({"error": "Unsupported platform"}), 400

    file_id = str(uuid.uuid4())
    outtmpl = f"{file_id}.%(ext)s"

    ydl_opts = {
        "outtmpl": outtmpl,
        "quiet": True,
        "format": "bestaudio" if audio else quality,
        "noplaylist": True
    }

    if use_cookies:
        ydl_opts["cookiefile"] = COOKIES_FILE

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        return send_file(filename, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        # Clean up
        if 'filename' in locals() and os.path.exists(filename):
            os.remove(filename)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
