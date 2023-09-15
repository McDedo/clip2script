import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib import colors
from nltk.tokenize import sent_tokenize, word_tokenize  # J'ai ajouté word_tokenize pour une utilisation potentielle
import nltk
import chardet
import tkinter as tk
from tkinter import filedialog


# Télécharger les données nécessaires pour la segmentation en phrases
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

# Vérifier si le fichier d'entrée existe
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

# Combiner les résultats
formatted_segments = paragraphs + sentences

# Nom du fichier de sortie PDF
output_filename = input("Entrez le nom du fichier de sortie PDF : ")

# Vérifier si le fichier de sortie existe déjà
if os.path.isfile(output_filename):
    response = input(f"Le fichier '{output_filename}' existe déjà. Voulez-vous le remplacer ? (O/N) : ").strip().lower()
    if response != 'o':
        exit(1)

# Demander à l'utilisateur de personnaliser la police et la taille (avec des valeurs par défaut)
font_name = input("Entrez le nom de la police (ou appuyez sur Entrée pour utiliser la police par défaut) : ").strip()
font_size = input("Entrez la taille de la police (ou appuyez sur Entrée pour utiliser la taille par défaut) : ").strip()

if not font_name:
    font_name = 'Helvetica'  # Police par défaut
if not font_size:
    font_size = 12  # Taille par défaut

try:
    font_size = float(font_size)
except ValueError:
    print("La taille de la police doit être un nombre valide.")
    exit(1)

doc = SimpleDocTemplate(output_filename, pagesize=letter)
styles = getSampleStyleSheet()

# Définir un nouveau style de paragraphe personnalisé
custom_style = ParagraphStyle(
    name='CustomStyle',
    parent=styles['Normal'],
    fontName=font_name,
    fontSize=font_size,
    textColor=colors.black
)

segments = []

# Créer des objets Paragraph avec le texte formaté
for segment_text in formatted_segments:
    segment = Paragraph(segment_text, style=custom_style)
    segments.append(segment)

# Construire le document PDF
doc.build(segments)

print(f"Le PDF a été créé avec succès sous le nom '{output_filename}'.")
