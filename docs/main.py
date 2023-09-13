import tkinter as tk
from tkinter import filedialog
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.editor import VideoFileClip
import speech_recognition as sr
import string
import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib import colors
from nltk.tokenize import sent_tokenize, word_tokenize
import nltk
import chardet

# Partie 1: Traitement vidéo
root = tk.Tk()
root.withdraw()
input_path = filedialog.askopenfilename(title="Sélectionnez un fichier vidéo")

if not input_path:
    print("Aucun fichier sélectionné. Sortie du programme.")
    exit()

output_path = "converted.mp4"
video_clip = VideoFileClip(input_path)
compressed_clip = video_clip.subclip()
compressed_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")

# Partie 2: Extraction audio
output_path = "converted.mp4"
video = VideoFileClip(output_path)
audio = video.audio
output_path = 'extracted_audio.wav'
audio.write_audiofile(output_path)

# Partie 3: Reconnaissance vocale et transcription
recognizer = sr.Recognizer()
audio_file = 'extracted_audio.wav'
def transcribe_segment(segment, language):
