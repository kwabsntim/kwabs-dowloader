import tkinter as tk
from tkinter import ttk
import threading
from yt_dlp import YoutubeDL

# GUI setup
window = tk.Tk()
window.geometry("600x400")
window.config(bg="black")
window.title("Kwabs Youtube Downloader")

tk.Label(window, text="Kwabs Youtube Downloader", bg="black", fg="white", font=("Arial", 20)).place(x=100, y=20)

link_var = tk.StringVar()
link = tk.Entry(window, width=50, bg='white', textvariable=link_var)
link.place(x=100, y=100)

# Progress and status widgets
progress = tk.DoubleVar()
progress_bar = ttk.Progressbar(window, variable=progress, maximum=100, length=400)
progress_bar.place(x=100, y=220)

status_label = tk.Label(window, text="", bg="black", fg="white")
status_label.place(x=100, y=260)

# Progress hook function
def progress_hook(d):
    if d['status'] == 'donloading':
        percent = float(d.get('progress', 0).replace('%', '')) if 'progress' in d else 0
        progress.set(percent)
        status_label.config(text=f"Downloading... {percent:.2f}%")  
        window.update_idletasks()
    elif d['status'] == 'finished':
        progress.set(100)
        status_label.config(text="Download completed!")

# Function to start download
def download_video():
    url = link_var.get().strip()
    if not url:
        status_label.config(text="Please enter a valid URL.")
        return

    def run_download():
        try:
            ydl_opts = {
                'outtmpl': '%(title)s.%(ext)s',
                'progress_hooks': [progress_hook],
                
                'writesubtitles':True,
                'writeautomaticsub': True,
                'subtitleslangs': ['en'],
                'format': 'best[height<=720]',
                
            }

            with YoutubeDL(ydl_opts) as ydl:
                info=ydl.extract_info(url, download=True)
                title = info.get('title', 'Downloaded Video')

                status_label.config(text=f"Downloaded: {title}").pack()
                progress.set(100).place(x=100, y=220)
                window.update_idletasks()
        except Exception as e:
                ydl.download([url])
        except Exception as e:
            status_label.config(text=f"Error: {e}")

    # Run download in a separate thread to avoid freezing GUI
    threading.Thread(target=run_download).start()

tk.Button(window, text='DOWNLOAD VIDEO', font='arial 10 bold', fg="white", bg='black', padx=1, command=download_video).place(x=230, y=170)

window.mainloop()
