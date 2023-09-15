import speech_recognition as sr
import string

# Créez un objet Recognizer
recognizer = sr.Recognizer()

# Chemin vers le fichier audio
audio_file = 'extracted_audio.wav'  # Utilisez l'audio extrait comme entrée

# Fonction pour transcrire un segment audio
def transcribe_segment(segment, language):
    try:
        # Utilisez le moteur de reconnaissance vocale
        text = recognizer.recognize_google(segment, language=language)
        return text
    except sr.UnknownValueError:
        return None
    except sr.RequestError as e:
        print("Erreur lors de la demande : {0}".format(e))
        return None

# Fonction pour ajouter de la ponctuation en fonction des pauses
def add_punctuation_based_on_pauses(text, pause_threshold=1.0):
    # Divisez le texte en phrases en fonction des pauses détectées
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

# Fonction pour mettre en majuscules la première lettre de chaque phrase
def capitalize_first_letter(text):
    sentences = text.split(". ")
    capitalized_sentences = [sentence.capitalize() for sentence in sentences]
    return ". ".join(capitalized_sentences)

# Ouvrez le fichier audio
with sr.AudioFile(audio_file) as source:
    # Déterminez la durée totale de l'audio
    audio_duration = source.DURATION
    # Définissez la durée maximale d'un segment (en secondes)
    segment_duration = 60
    # Calculez le nombre total de segments nécessaires
    total_segments = int(audio_duration / segment_duration) + 1
    # Transcrire chaque segment
    languages = ["fr-FR", "en-US"]
    full_text = ""
    for language in languages:
        for segment_index in range(total_segments):
            start_time = segment_index * segment_duration
            end_time = min((segment_index + 1) * segment_duration, audio_duration)
            # Obtenez un segment audio
            segment = recognizer.record(source, offset=start_time, duration=end_time - start_time)
            # Transcrire le segment et ajouter le texte au résultat complet
            segment_text = transcribe_segment(segment, language)
            full_text += segment_text + " "
    # Ajoutez de la ponctuation en fonction des pauses à la transcription complète
    full_text_with_punctuation = add_punctuation_based_on_pauses(full_text)
    # Mettez en majuscules la première lettre de chaque phrase
    full_text_with_capitalization = capitalize_first_letter(full_text_with_punctuation)
    # Créez un fichier externe pour contenir la transcription complète avec ponctuation et majuscules
    with open("transcription_complete.txt", "w") as output_file:
        output_file.write(full_text_with_capitalization)

