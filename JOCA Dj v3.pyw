import os
import shutil
import threading
import tkinter as tk
from tkinter import messagebox
from yt_dlp import YoutubeDL
import ttkbootstrap as tb
from ttkbootstrap.constants import *

from flask import Flask, request
import queue
from flask_cors import CORS   # <-- adicionado

# --- Constants ---
OUTPUT_PATH = r'C:\Users\Admin\Desktop\Musicas baixadas'
PENDRIVE_PATH = r'D:\\'

# --- Flask queue ---
download_queue = queue.Queue()
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # habilita CORS para todas as rotas


def log_history(message):
    history_text.insert(tk.END, message + "\n")
    history_text.yview(tk.END)

def progress_hook(d):
    if d['status'] == 'downloading':
        total = d.get('total_bytes') or d.get('total_bytes_estimate')
        downloaded = d.get('downloaded_bytes', 0)
        if total:
            current = downloaded / total * 100
            progress_label.config(text=f"{current:.2f}% - Tenha Paciência Joca kkkk")
            progress_bar['value'] = current
            window.update_idletasks()

    elif d['status'] == 'finished':
        progress_label.config(text="Salvando MP3 no Pendrive Joca...")
        progress_bar['value'] = 90
        window.update_idletasks()

def download_and_process(url):
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': os.path.join(OUTPUT_PATH, '%(title)s.%(ext)s'),
            'noplaylist': True,
            'progress_hooks': [progress_hook],
            'ignoreerrors': True,
        }

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

            if filename.endswith((".webm", ".m4a", ".mp4")):
                filename = filename.rsplit(".", 1)[0] + ".mp3"

        dest = os.path.join(PENDRIVE_PATH, os.path.basename(filename))
        backup = os.path.join(OUTPUT_PATH, "musicas-ja-copiadas-pro-pendrive", os.path.basename(filename))

        os.makedirs(os.path.dirname(backup), exist_ok=True)

        shutil.copy(filename, dest)
        shutil.move(filename, backup)

        progress_bar['value'] = 100
        progress_label.config(text="Música baixada e copiada com sucesso Joca!")
        log_history(f"Sucesso: {os.path.basename(filename)} copiado.")

    except Exception as e:
        log_history(f"Erro: {e}")
        messagebox.showerror("Erro", str(e))
        progress_bar['value'] = 0
        progress_label.config(text="")

# --------- WORKER QUE PROCESSA A FILA ---------
def queue_worker():
    while True:
        url = download_queue.get()
        url_entry.delete(0, tk.END)
        url_entry.insert(0, url)

        if not os.path.exists(PENDRIVE_PATH):
            messagebox.showerror(
                "Ai não Joca... Cadê o Pendrive??",
                "Só funciona com o pendrive, esqueceu kkkkkkkk"
            )
            log_history("Falha: Pendrive não encontrado!")
            continue

        progress_bar['value'] = 0
        progress_label.config(text="Baixando sua música Joca...")
        window.update_idletasks()

        download_and_process(url)
        download_queue.task_done()

threading.Thread(target=queue_worker, daemon=True).start()

# --------- ENDPOINT QUE RECEBE LINK DO CHROME ---------
@app.route("/add")
def add():
    try:
        url = request.args.get("url", "").strip()

        # Se não for link do YouTube → ignora silenciosamente
        if not url or "youtube.com/watch" not in url:
            return "", 204  # No content, sem erro

        download_queue.put(url)
        log_history(f"[Fila] Recebido do Chrome: {url}")
        return "OK", 200

    except:
        return "", 204  # ignora qualquer erro inesperado

def run_flask():
    app.run(host="0.0.0.0", port=5005, debug=False, use_reloader=False)

threading.Thread(target=run_flask, daemon=True).start()

# --- GUI Setup ---
window = tb.Window(themename="cosmo")
window.title("Joca DJ")
window.geometry("800x580")

url_label = tb.Label(window, text="Link do YouTube", bootstyle="info", font=("Segoe UI", 14))
url_label.pack(pady=(20, 5))

url_entry = tb.Entry(window, font=("Segoe UI", 10), width=60)
url_entry.pack(pady=5, padx=20, fill=X)

# botão manual continua funcionando
def execute_all_actions():
    url = window.clipboard_get().strip()
    download_queue.put(url)

style = tb.Style()
style.configure("Custom.TButton", font=("Segoe UI", 16))  # fonte maior

execute_button = tb.Button(
    window,
    text="🎵 Colar, Baixar e Salvar no Pendrive Joca",
    command=execute_all_actions,
    bootstyle="primary",
    width=50,
    style="Custom.TButton"   # aplica estilo customizado
)
execute_button.pack(pady=15)

progress_label = tb.Label(window, text="", font=("Segoe UI", 14))
progress_label.pack(pady=5)

progress_bar = tb.Progressbar(window, orient="horizontal", mode="determinate", bootstyle="info-striped")
progress_bar.pack(pady=10, padx=20, fill=X)

history_label = tb.Label(window, text="Histórico de Downloads", bootstyle="secondary", font=("Segoe UI", 12))
history_label.pack(pady=(20, 5))

history_text = tk.Text(window, height=10, font=("Segoe UI", 10), wrap=tk.WORD, bg="#f9f9f9")
history_text.pack(padx=20, pady=10, fill=BOTH, expand=True)

window.mainloop()
