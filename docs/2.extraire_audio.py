<<<<<<< HEAD:docs/2.extraire_audio.py
# Charger la vidéo
video = VideoFileClip(output_path)  # Use the converted video as input


# Extraire l'audio de la vidéo
audio = video.audio

output_path = 'extracted_audio.wav'
audio.write_audiofile(output_path)

video.close()
audio.close()
=======
import speech_recognition as sr

# Charger la vidéo
output_path = "converted.mp4"
video = VideoFileClip(output_path)  # Use the converted video as input


# Extraire l'audio de la vidéo
audio = video.audio

output_path = 'extracted_audio.wav'
audio.write_audiofile(output_path)

video.close()
audio.close()
>>>>>>> 271d12ad4d0635a525c9fae3e9d69c994c8476b9:2.extraire_audio.py
