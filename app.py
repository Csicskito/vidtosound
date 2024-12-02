
##############################################################x
from flask import Flask, request, render_template, send_file
import os
import yt_dlp

app = Flask(__name__)
DOWNLOAD_FOLDER = "C:/Users/lacik/Desktop/html/VIDTOSOUNDT/downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def download_youtube_audio(url):
    """
    Download YouTube audio and convert it to MP3.
    Returns the path to the MP3 file.
    """
    ydl_opts = {
        "format": "bestaudio/best",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
        "outtmpl": f"{DOWNLOAD_FOLDER}/%(title)s.%(ext)s",  # Save with the video title
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        mp3_file = os.path.join(DOWNLOAD_FOLDER, f"{info['title']}.mp3")
    return mp3_file

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/download", methods=["POST"])
def download():
    try:
        # Get the URL from the form
        url = request.form["url"]
        mp3_file = download_youtube_audio(url)

        # Send the file to the user for download
        return send_file(mp3_file, as_attachment=True)

    except Exception as e:
        return f"An error occurred: {str(e)}"

if __name__ == "__main__":
    app.run(debug=True)
