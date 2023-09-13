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
    try:
        text = recognizer.recognize_google(segment, language=language)
        return text
    except sr.UnknownValueError:
        return ""
    except sr.RequestError as e:
        print("Erreur lors de la demande : {0}".format(e))
        return ""
def add_punctuation_based_on_pauses(text, pause_threshold=2.0):
    sentences = []
    current_sentence = []
    total_pause_duration = 0.0
    for word in text.split():
        if word.endswith('.'):
            current_sentence.append(word)
            sentences.append(' '.join(current_sentence))
            current_sentence = []
            total_pause_duration = 0.0
        else:
            current_sentence.append(word)
            total_pause_duration += len(word) * 0.04  # Estimation de la durée en secondes par mot (peut nécessiter un ajustement)
            if total_pause_duration >= pause_threshold:
                sentences.append(' '.join(current_sentence))
                current_sentence = []
                total_pause_duration = 0.0
    return ' '.join(sentences)
def capitalize_first_letter(text):
    sentences = text.split(". ")
    capitalized_sentences = [sentence.capitalize() for sentence in sentences]
    return ". ".join(capitalized_sentences)
with sr.AudioFile(audio_file) as source:
    audio_duration = source.DURATION
    segment_duration = 30
    total_segments = int(audio_duration / segment_duration) + 1
    languages = ["fr-FR", "en-US"]
    full_text = ""
    for language in languages:
        for segment_index in range(total_segments):
            start_time = segment_index * segment_duration
            end_time = min((segment_index + 1) * segment_duration, audio_duration)
            segment = recognizer.record(source, offset=start_time, duration=end_time - start_time)
            segment_text = transcribe_segment(segment, language)
            full_text += segment_text + " "
    full_text_with_punctuation = add_punctuation_based_on_pauses(full_text)
    full_text_with_capitalization = capitalize_first_letter(full_text_with_punctuation)
    with open("transcription_complete.txt", "w") as output_file:
        output_file.write(full_text_with_capitalization)
        
        # Partie 4: Génération de PDF

