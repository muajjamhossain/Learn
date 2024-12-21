import pyautogui
import cv2
import numpy as np
import pyaudio
import wave
import threading

# Audio recording setup
audio_filename = "audio.wav"
audio_format = pyaudio.paInt16  # Audio format
audio_channels = 1  # Mono audio
audio_rate = 44100  # Sample rate (samples per second)
audio_chunk = 1024  # Buffer size
audio_device_index = None  # Default device

# Screen recording setup
resolution = (1920, 1080)  # Screen resolution
fps = 60.0  # Frames per second for screen recording
output_filename = "Recording_with_audio.avi"  # Output video file
codec = cv2.VideoWriter_fourcc(*"XVID")  # Video codec

# Function to record audio
def record_audio():
    print("Audio recording started...")
    
    # Initialize audio stream
    p = pyaudio.PyAudio()
    stream = p.open(format=audio_format, channels=audio_channels, rate=audio_rate, 
                    input=True, frames_per_buffer=audio_chunk, input_device_index=audio_device_index)

    frames = []
    
    while True:
        try:
            data = stream.read(audio_chunk)
            frames.append(data)
        except KeyboardInterrupt:
            break

    print("Audio recording stopped.")
    
    # Save the audio to a WAV file
    with wave.open(audio_filename, 'wb') as wf:
        wf.setnchannels(audio_channels)
        wf.setsampwidth(p.get_sample_size(audio_format))
        wf.setframerate(audio_rate)
        wf.writeframes(b''.join(frames))
    
    # Close the audio stream
    stream.stop_stream()
    stream.close()
    p.terminate()

# Function to record screen
def record_screen():
    print(f"Resolution set to {resolution}, FPS set to {fps}")
    
    # Create VideoWriter object for screen recording
    out = cv2.VideoWriter(output_filename, codec, fps, resolution)
    
    # Create a window for display (optional)
    cv2.namedWindow("Live", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Live", 480, 270)

    while True:
        try:
            # Capture the screen
            img = pyautogui.screenshot()
            img = img.convert('RGB')  # Convert to RGB
            frame = np.array(img)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)  # Convert to BGR for OpenCV
            
            # Write the frame to the video file
            out.write(frame)
            
            # Display the screen recording (optional)
            cv2.imshow("Live", frame)
            
            # Stop recording on pressing 'q'
            if cv2.waitKey(1) == ord('q'):
                break
        except KeyboardInterrupt:
            break
    
    # Release the VideoWriter object
    out.release()
    cv2.destroyAllWindows()
    print("Screen recording stopped.")

# Main function to start both audio and video recording
def start_recording():
    # Start audio recording in a separate thread
    audio_thread = threading.Thread(target=record_audio)
    audio_thread.daemon = True
    audio_thread.start()
    
    # Start screen recording
    record_screen()

# Start the recording
if __name__ == "__main__":
    start_recording()
