import os
import nltk
import torch
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from transformers import BertTokenizer, CamembertTokenizer, BertForMaskedLM, CamembertForMaskedLM

nltk.download('punkt')
nltk.download('stopwords')

def clean_text(text):
    # Tokenization
    tokens = word_tokenize(text)
    # Remove punctuation and non-alphabetic characters
    tokens = [word for word in tokens if word.isalpha()]
    # Convert to lowercase
    tokens = [word.lower() for word in tokens]
    # Remove stop words
    stop_words = set(stopwords.words('english'))  # Using English stop words
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
    
    # Tokenization of the text
    tokens = tokenizer.tokenize(text)
    
    # Replace each token with the model's most likely suggestion
    corrected_tokens = []
    for token in tokens:
        if token == tokenizer.mask_token:
            # The model uses a mask for predicting missing words
            # Replace the mask with the most likely suggestion
            input_text = ' '.join(corrected_tokens)  # Text so far
            masked_text = f"{input_text} {tokenizer.mask_token} {token}"  # Masked text
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

def process_file(input_filename, output_filename):
    with open(input_filename, 'r', encoding='utf-8') as file:
        text = file.read()
        cleaned_text = clean_text(text)
        
        # Language detection (here, simply checking if "fr" or "en" appears in the text)
        if "fr" in cleaned_text:
            lang = 'fr'
        else:
            lang = 'en'
        
        corrected_text = correct_text(cleaned_text, lang)

        # Save the corrected text to an output file
        with open(output_filename, 'w', encoding='utf-8') as outfile:
            outfile.write(corrected_text)

# File paths
input_filename = "transcription_complete.txt"   # Use the converted video as input

if not os.path.isfile(input_filename):
    print(f"Le fichier '{input_filename}' est introuvable.")
else:
    # Specify the path for the output file
    output_filename = "texte_corrigé.txt"
   
    process_file(input_filename, output_filename)  # Call the function with both input and output filenames
<<<<<<< HEAD

=======
>>>>>>> ad7c2f1a10f383c248436ef59d567ee3162508dd
