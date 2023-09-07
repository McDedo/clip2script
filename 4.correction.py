import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from transformers import CamembertForMaskedLM, CamembertTokenizer, BertForMaskedLM, BertTokenizer
import os

nltk.download('punkt')
nltk.download('stopwords')

def clean_text(text):
    # Tokenisation
    tokens = word_tokenize(text)
    # Suppression de la ponctuation et des caractères non alphabétiques
    tokens = [word for word in tokens if word.isalpha()]
    # Conversion en minuscules
    tokens = [word.lower() for word in tokens]
    # Suppression des mots vides
    stop_words = set(stopwords.words('english'))  # Utilisation des mots vides en anglais
    tokens = [word for word in tokens if word not in stop_words]
    cleaned_text = ' '.join(tokens)
    return cleaned_text

def correct_text(text, lang):
    if lang == 'fr':
        tokenizer = CamembertTokenizer.from_pretrained("camembert-base")
        model = CamembertForMaskedLM.from_pretrained("camembert-base")
    elif lang == 'en':
        tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
        model = BertForMaskedLM.from_pretrained("bert-base-uncased")
    else:
        raise ValueError("Langue non prise en charge")
    
    # Tokenisation du texte
    tokens = tokenizer.tokenize(text)
    
    # Remplacement de chaque token par la suggestion la plus probable du modèle
    corrected_tokens = []
    for token in tokens:
        if token == tokenizer.mask_token:
            # Le modèle utilise un masque pour la prédiction de mots manquants
            # Remplacez le masque par la suggestion la plus probable
            input_text = ' '.join(corrected_tokens)  # Texte jusqu'à présent
            masked_text = f"{input_text} {tokenizer.mask_token} {token}"  # Texte masqué
            input_ids = tokenizer.encode(masked_text, return_tensors='pt')
            with torch.no_grad():
                logits = model(input_ids)[0]
            predicted_token_id = logits[0, -1].argmax().item()
            predicted_token = tokenizer.decode(predicted_token_id)
            corrected_tokens.append(predicted_token)
        else:
            corrected_tokens.append(token)
    
    corrected_text = ' '.join(corrected_tokens)
    return corrected_text

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
        cleaned_text = clean_text(text)
        
        # Détection de la langue (ici, simplement en vérifiant si "fr" ou "en" apparaît dans le texte)
        if "fr" in cleaned_text:
            lang = 'fr'
        else:
            lang = 'en'
        
        corrected_text = correct_text(cleaned_text, lang)
        return corrected_text

# Chemin du fichier texte
file_path = input("Entrez le nom du fichier texte : ")

if not os.path.isfile(file_path):
    print("Chemin de fichier invalide.")
else:
    corrected_text = process_file(file_path)
    print(f"Texte corrigé ({'français' if 'fr' in corrected_text else 'anglais'}):")
    print(corrected_text)
