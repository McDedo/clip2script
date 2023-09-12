import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib import colors
from nltk.tokenize import sent_tokenize, word_tokenize  # J'ai ajouté word_tokenize pour une utilisation potentielle
import nltk

# Télécharger les données nécessaires pour la segmentation en phrases
nltk.download('punkt')

# Fonction pour segmenter un texte en paragraphes ou phrases
def segment_text(text, separator='\n\n', segment_into='paragraphs'):
    if segment_into == 'paragraphs':
        return text.split(separator)
    elif segment_into == 'sentences':
        return sent_tokenize(text)
    else:
        raise ValueError("L'argument 'segment_into' doit être 'paragraphs' ou 'sentences'.")

input_filename = "texte_corrigé.txt"

# Vérifier si le fichier d'entrée existe
if not os.path.isfile(input_filename):
    print(f"Le fichier '{input_filename}' n'existe pas.")
    exit(1)

# Lire le contenu du fichier texte
with open(input_filename, 'r') as file:
    text = file.read()

# Sélectionner le mode de segmentation (paragraphes ou phrases)
segment_into = input("Segmenter en 'paragraphes' ou 'phrases' ? : ").strip().lower()

# Segmenter le texte en paragraphes ou phrases en utilisant un séparateur personnalisé
separator = '\n\n'  # Séparateur par défaut pour les paragraphes
if segment_into == 'phrases':
    formatted_segments = segment_text(text, segment_into='sentences')
else:
    formatted_segments = segment_text(text, separator, segment_into='paragraphs')

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
