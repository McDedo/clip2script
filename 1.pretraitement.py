from moviepy.video.io.VideoFileClip import VideoFileClip

# Ask the user for the input video file path

input_path = input("Enter the input video file name: ")

# Video Conversion
output_path = "converted.mp4"

video_clip = VideoFileClip(input_path)
compressed_clip = video_clip

compressed_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")

# Detection des scènes

cap = cv2.VideoCapture(output_path)      # Use the converted video as input
ret, prev_frame = cap.read()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    frame_diff = cv2.absdiff(prev_frame, frame)
    cv2.imshow('Frame Difference', frame_diff)
    prev_frame = frame
    if cv2.waitKey(30) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
