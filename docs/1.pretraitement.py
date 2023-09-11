import tkinter as tk
from tkinter import filedialog
from moviepy.video.io.VideoFileClip import VideoFileClip

# Create a tkinter windows
root = tk.Tk()
root.withdraw()

# Utilisez la boîte de dialogue de sélection de fichier pour obtenir le chemin du fichier vidéo
input_path = filedialog.askopenfilename(title="Sélectionnez un fichier vidéo")

if not input_path:
    print("Aucun fichier sélectionné. Sortie du programme.")
    exit()

# Video Conversion
output_path = "converted.mp4"

video_clip = VideoFileClip(input_path)

# Créez une sous-clip avec la même vidéo
compressed_clip = video_clip.subclip()

compressed_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")


=======
import tkinter as tk
from tkinter import filedialog
from moviepy.video.io.VideoFileClip import VideoFileClip

# Create a tkinter windows
root = tk.Tk()
root.withdraw()

# Utilisez la boîte de dialogue de sélection de fichier pour obtenir le chemin du fichier vidéo
input_path = filedialog.askopenfilename(title="Sélectionnez un fichier vidéo")

if not input_path:
    print("Aucun fichier sélectionné. Sortie du programme.")
    exit()

# Video Conversion
output_path = "input_path\converted.mp4"

video_clip = VideoFileClip(input_path)

# Créez une sous-clip avec la même vidéo
compressed_clip = video_clip.subclip()

compressed_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")


>>>>>>> 271d12ad4d0635a525c9fae3e9d69c994c8476b9:1.pretraitement.py
