from moviepy.editor import VideoFileClip

# Chemin vers la vidéo d'entrée
chemin_video = input("Entrez le nom du fichier texte : ")

# Charger la vidéo
video = VideoFileClip(chemin_video)

# Extraire l'audio de la vidéo
audio = video.audio

# Définir le chemin de sortie pour le fichier audio extrait (format WAV par défaut)
chemin_audio_extrait = 'humour.wav'

# Enregistrer le fichier audio extrait
audio.write_audiofile(chemin_audio_extrait)

video.close()
audio.close()