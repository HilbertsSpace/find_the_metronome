import pyaudio
import wave
import numpy as np
import matplotlib.pyplot as plt
import mysql.connector
from sql_helpers import insert_audio_row, drop_audio_table, make_audio_table


# This script saves the audio data and a y label to the audio_table.

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
INPUT_DEVICE_INDEX = 1
WAVE_INPUT_FILENAME = "data/metronome_data_6.wav"
audio = pyaudio.PyAudio()
plot_beats = True

# audio parameters
BPS = 252/60 # metronome beats per second
TIME_BETWEEN_BEAT = 1/BPS
SAMPLES_PER_BEAT = RATE*TIME_BETWEEN_BEAT # this is separation between beats
# my guess for the first start and end beat
START_BEAT = 4000
END_BEAT = 4600

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



beat = set() # indices of samples where metronome click not present
no_beat = set() # indices of samples where metronome click is not present

i = 0
start = START_BEAT
end = END_BEAT
while i < 100: # labeling around 100 beats
    audio_data_win2 = audio_data[int(start):int(end)]
    if plot_beats:
        plt.plot([i for i in range(audio_data_win2.shape[0])], audio_data_win2)
        plt.show()
        plt.clf()
    beat.update([i for i in range(int(start),int(end))])
    start+=SAMPLES_PER_BEAT
    no_beat.update([i for i in range(int(start), int(end))]) # metronome doesn't hit here
    end+=SAMPLES_PER_BEAT
    i+=1
end-=SAMPLES_PER_BEAT

X = []
y = []
i = 0
step = 512
while i < end:
    X.append(audio_data[i:i+step])
    curr = set([i for i in range(i, i+step)])
    b = len(curr.intersection(beat))
    nb = len(curr.intersection(no_beat))
    if b > nb:
        y.append(1)
    else:
        y.append(0)
    i+=step
labeled = len(y)
while i < len(audio_data):
    X.append(audio_data[i:i + step])
    y.append(None)
    i += step

X_win = X[0:100]
y_win = y[0:100]
X_concat = np.concatenate(X_win)[0:100000]

plt.plot([i for i in range(X_concat.shape[0])], X_concat, 'b', alpha=.5)
y_x = [i*512 for i in range(len(y_win))]
y_maxed = [each*max(X_concat) for each in y_win]
plt.plot(y_x, y_maxed, 'r', alpha=.5)
plt.show()


DB_NAME = 'testDB'
cnx = mysql.connector.connect(user='free')
cursor = cnx.cursor()

cursor.execute("USE {};".format(DB_NAME))
cursor.execute(drop_audio_table)
cursor.execute(make_audio_table)

i = 0
while i < len(X):
    data_insert_row_1 = insert_audio_row(X[i], y[i])
    cursor.execute(data_insert_row_1)
    if not i%100:
        print('%s of %s rows written to db'%(str(i), str(len(X))))
    i+=1
cnx.commit()
print('done')
print('pushed %s rows of labeled and %s of unlabeled data to db'%(str(labeled), str(len(X)-labeled)))
