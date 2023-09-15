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
def add_punctuation_based_on_pauses(text, pause_threshold=1.0):
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
            total_pause_duration += len(word) * 0.04 
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
    segment_duration = 60
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
nltk.download('punkt')

# Fonction pour segmenter un texte en paragraphes et/ou phrases
def segment_text(text, separator='\n\n', segment_into=('paragraphs', 'sentences')):
    if not set(segment_into).issubset({'paragraphs', 'sentences'}):
        raise ValueError("Les éléments de 'segment_into' doivent être 'paragraphs' et/ou 'sentences'.")

    segments = []
    if 'paragraphs' in segment_into:
        paragraphs = text.split(separator)
        segments.extend(paragraphs)
    
    if 'sentences' in segment_into:
        sentences = sent_tokenize(text)
        segments.extend(sentences)
    
    return segments

input_filename = "transcription_complete.txt"

if not os.path.isfile(input_filename):
    print(f"Le fichier '{input_filename}' n'existe pas.")
    exit(1)

# Function to detect file encoding
def detect_encoding(input_filename):
    with open(input_filename, 'rb') as file:
        detector = chardet.universaldetector.UniversalDetector()
        for line in file:
            detector.feed(line)
            if detector.done:
                break
        detector.close()
    return detector.result['encoding']

# Determine the file's encoding
input_encoding = detect_encoding(input_filename)

# Open the file with the detected encoding
with open(input_filename, 'r', encoding=input_encoding) as file:
    text = file.read()

# Segmenter le texte en paragraphes et en phrases
paragraphs = segment_text(text, separator='\n\n', segment_into=['paragraphs'])
sentences = segment_text(text, segment_into=['sentences'])

formatted_segments = paragraphs + sentences
output_filename = input("Entrez le nom du fichier de sortie PDF : ")
if os.path.isfile(output_filename):
    response = input(f"Le fichier '{output_filename}' existe déjà. Voulez-vous le remplacer ? (O/N) : ").strip().lower()
    if response != 'o':
        exit(1)
font_name = input("Entrez le nom de la police (ou appuyez sur Entrée pour utiliser la police par défaut) : ").strip()
font_size = input("Entrez la taille de la police (ou appuyez sur Entrée pour utiliser la taille par défaut) : ").strip()
if not font_name:
    font_name = 'Helvetica' 
if not font_size:
    font_size = 12 
try:
    font_size = float(font_size)
except ValueError:
    print("La taille de la police doit être un nombre valide.")
    exit(1)

doc = SimpleDocTemplate(output_filename, pagesize=letter)
styles = getSampleStyleSheet()
custom_style = ParagraphStyle(
    name='CustomStyle',
    parent=styles['Normal'],
    fontName=font_name,
    fontSize=font_size,
    textColor=colors.black
)
segments = []
for segment_text in formatted_segments:
    segment = Paragraph(segment_text, style=custom_style)
    segments.append(segment)
doc.build(segments)
print(f"Le PDF a été créé avec succès sous le nom '{output_filename}'.")
