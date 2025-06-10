from flask import Flask, request, render_template, send_file, redirect, url_for, flash
import yt_dlp
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"  # 用於加密 session 資料
DOWNLOAD_FOLDER = "./downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)  # 確保目錄存在

def download_audio(url, custom_name=None):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
        'no_warnings': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        original_file_path = os.path.join(DOWNLOAD_FOLDER, f"{info['title']}.mp3")

        if custom_name:  # 如果有自定義名稱，重新命名
            new_file_path = os.path.join(DOWNLOAD_FOLDER, f"{custom_name}.mp3")
            os.rename(original_file_path, new_file_path)
            return new_file_path

        return original_file_path

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")
        custom_name = request.form.get("custom_name")

        if not url:
            flash("請提供有效的 URL！", "error")
            return redirect(url_for("index"))

        return render_template("wait.html", url=url, custom_name=custom_name)

    return render_template("index.html")

@app.route("/download", methods=["POST"])
def download():
    url = request.form.get("url")
    custom_name = request.form.get("custom_name")

    try:
        file_path = download_audio(url, custom_name)
        flash("下載完成！檔案已準備好。", "success")
        return redirect(url_for("index"))  # 返回首頁並顯示提示訊息
    except Exception as e:
        flash(f"下載失敗：{e}", "error")
        return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
