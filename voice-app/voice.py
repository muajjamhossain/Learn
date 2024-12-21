import sounddevice as sd
from scipy.io.wavfile import write
from datetime import datetime
import numpy as np

# Function to generate a timestamped filename
def get_timestamped_filename(extension="wav"):
    return datetime.now().strftime(f"recording_%Y%m%d_%H%M%S.{extension}")

# Sampling frequency
freq = 44100

# Recording duration (in seconds)
duration = 30

# Record audio using sounddevice
print("Recording...")
recording = sd.rec(int(duration * freq), samplerate=freq, channels=2)
sd.wait()  # Wait until recording is finished
print("Recording completed.")

# Ensure the recording data is properly formatted
recording = np.int16(recording * 32767)  # Convert to 16-bit PCM format

# Generate timestamped filenames
wav_filename = get_timestamped_filename("wav")
mp3_filename = get_timestamped_filename("mp3")  # MP3 needs external library for encoding

# Save the recording in WAV format
write(wav_filename, freq, recording)
print(f"Recording saved as {wav_filename}")

# If you need MP3 format, you can use an external library like pydub
try:
    from pydub import AudioSegment
    from pydub.utils import mediainfo

    audio = AudioSegment(
        recording.tobytes(), 
        frame_rate=freq, 
        sample_width=recording.dtype.itemsize, 
        channels=2
    )
    audio.export(mp3_filename, format="mp3")
    print(f"Recording also saved as {mp3_filename}")
except ImportError:
    print("pydub is not installed. MP3 conversion skipped.")
