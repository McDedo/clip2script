import tkinter as tk
from tkinter import filedialog
from moviepy.video.io.VideoFileClip import VideoFileClip
import cv2

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
compressed_clip = video_clip

compressed_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")

# Detection des scènes

cap = cv2.VideoCapture(output_path)      # Use the converted video as input
ret, prev_frame = cap.read()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    frame_diff = cv2.absdiff(prev_frame, frame)
    cv2.imshow('Frame Difference', frame_diff)
    prev_frame = frame
    if cv2.waitKey(30) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
