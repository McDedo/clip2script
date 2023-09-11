

# Charger la vidéo
output_path = "converted.mp4"
video = VideoFileClip(output_path)  # Use the converted video as input


# Extraire l'audio de la vidéo
audio = video.audio

output_path = 'extracted_audio.wav'
audio.write_audiofile(output_path)

video.close()
audio.close()
