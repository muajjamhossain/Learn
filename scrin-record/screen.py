import pyautogui
import cv2
import numpy as np
import pyaudio
import wave
import threading

# Specify resolution
resolution = (1920, 1080)

# Specify video codec
codec = cv2.VideoWriter_fourcc(*"XVID")

# Specify name of Output file
filename = "Recording.avi"

# Specify frames rate
fps = 60.0

# Create VideoWriter object
out = cv2.VideoWriter(filename, codec, fps, resolution)

# Create an Empty window
cv2.namedWindow("Live", cv2.WINDOW_NORMAL)

# Resize this window
cv2.resizeWindow("Live", 480, 270)

# Audio parameters
audio_filename = "audio.wav"
audio_format = pyaudio.paInt16
audio_channels = 1
audio_rate = 44100
audio_chunk = 1024

# Initialize PyAudio for audio recording
p = pyaudio.PyAudio()
stream = p.open(format=audio_format,
                channels=audio_channels,
                rate=audio_rate,
                input=True,
                frames_per_buffer=audio_chunk)

frames = []

# Function to record audio in a separate thread
def record_audio():
    while True:
        data = stream.read(audio_chunk)
        frames.append(data)

# Start audio recording in a separate thread
audio_thread = threading.Thread(target=record_audio)
audio_thread.daemon = True
audio_thread.start()

while True:
    # Take screenshot using PyAutoGUI
    img = pyautogui.screenshot()

    # Convert the screenshot to a numpy array
    frame = np.array(img)

    # Convert it from BGR(Blue, Green, Red) to RGB(Red, Green, Blue)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Write it to the output file
    out.write(frame)

    # Optional: Display the recording screen
    cv2.imshow('Live', frame)

    # Stop recording when we press 'q'
    if cv2.waitKey(1) == ord('q'):
        break

# Release the Video writer
out.release()

# Stop the audio stream and save the audio file
stream.stop_stream()
stream.close()
p.terminate()

# Save audio to file
with wave.open(audio_filename, 'wb') as wf:
    wf.setnchannels(audio_channels)
    wf.setsampwidth(p.get_sample_size(audio_format))
    wf.setframerate(audio_rate)
    wf.writeframes(b''.join(frames))

# Destroy all windows
cv2.destroyAllWindows()
