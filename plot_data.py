import pyaudio
import wave
import numpy as np
import matplotlib.pyplot as plt
import mysql.connector
from sql_script_templates import get_single_insert_labeled, make_audio_table_labeled


# This script is used to plot the audio data to find a metronome click. If you find one metronome click and know the
# tempo of the metronome you can label most of the signal accurately with minimal manual work. Use this script to find
# the start and end of a metronome tocl and use the manually_label_data.py script to label a few hundred metronome ticks
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
INPUT_DEVICE_INDEX = 1

# audio parameters
BPS = 252/60 # metronome beats per second
TIME_PER_BEAT = 1/BPS # this is separation between beats, not duration
SAMPLES_PER_BEAT = RATE*TIME_PER_BEAT# audio_data_win is duration

WAVE_INPUT_FILENAME = "data/metronome_data_6.wav"
audio = pyaudio.PyAudio()

# open the file for reading
wf = wave.open(WAVE_INPUT_FILENAME, 'rb')
p = pyaudio.PyAudio()

# read data from file
data = wf.readframes(CHUNK)
frames = [data]
while len(data) > 0:
    data = wf.readframes(CHUNK)
    frames.append(data)
data = b''.join(frames)
audio_data = np.fromstring(data, dtype=np.int16)

# adjust the plot window to find a narrow start and end window to use in manually_label_data.py
plot_min = 0
plot_max = int(RATE)  # plots a second of data
plot_min = 4000
plot_max = 4600#10250+1000

audio_data_win = audio_data[plot_min:plot_max]
plt.plot([i for i in range(audio_data_win.shape[0])], audio_data_win)
plt.show()
# For the sample metronome_data_6.wav I estimated a start and end tuple of 4000, 4600
# I use those values in the manually_label_data.py script
