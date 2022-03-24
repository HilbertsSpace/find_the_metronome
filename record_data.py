import pyaudio
import wave
import numpy as np
import matplotlib.pyplot as plt


# This script is used to record training audio.  I'm recording a metronome.
# Use PyAudio to print recording devices available
print_input_devices = 1
if print_input_devices:
    p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    for i in range(0, numdevices):
        if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))


INPUT_DEVICE_INDEX = 1 # selects a recording device
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 100
WAVE_OUTPUT_FILENAME = "data/metronome_data_7.wav"

audio = pyaudio.PyAudio()
# start Recording
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK, input_device_index=INPUT_DEVICE_INDEX)
print("recording...")
frames = []
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)
print("finished recording")

# stops recording stream, closes
stream.stop_stream()
stream.close()
audio.terminate()

audio_data = np.fromstring(b''.join(frames), dtype=np.int16)
print(len(audio_data))
audio_data = audio_data.tobytes()
print(len(audio_data))

# writes a wav file
waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
waveFile.setnchannels(CHANNELS)
waveFile.setsampwidth(audio.get_sample_size(FORMAT))
waveFile.setframerate(RATE)
waveFile.writeframes(b''.join(frames))
waveFile.close()
print('saved audio to %s'%WAVE_OUTPUT_FILENAME)
