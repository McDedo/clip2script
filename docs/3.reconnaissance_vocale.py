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
        return ""
    except sr.RequestError as e:
        print("Erreur lors de la demande : {0}".format(e))
        return ""

# Fonction pour ajouter de la ponctuation à un texte
def add_punctuation(text):
    # Supprimez la ponctuation de la sortie de la reconnaissance vocale (car elle ne contient pas de ponctuation)
    text = text.translate(str.maketrans('', '', string.punctuation))
    # Ajoutez la ponctuation à l'endroit approprié
    text_with_punctuation = text.replace('.', '. ').replace('!', '! ').replace('?', '? ')
    return text_with_punctuation

# Ouvrez le fichier audio
with sr.AudioFile(audio_file) as source:
    # Déterminez la durée totale de l'audio
    audio_duration = source.DURATION
    # Définissez la durée maximale d'un segment (en secondes)
    segment_duration = 30
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
    # Ajoutez de la ponctuation à la transcription complète
    full_text_with_punctuation = add_punctuation(full_text)
    # Créez un fichier externe pour contenir la transcription complète avec ponctuation
    with open("transcription_complete_with_punctuation.txt", "w") as output_file:
        output_file.write(full_text_with_punctuation)

