from pylsl import StreamInlet, resolve_stream
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
from collections import deque

# used to callibrate the length of capture
#last_print = time.time()
#fps_counter = deque(maxlen=150)



def connectEEG():
# finding eeg and starting stream
	print("looking for an EEG stream...")
	streams = resolve_stream('type', 'EEG')

	inlet = StreamInlet(streams[0])
	print("connected")

	return (inlet)
# used to measure about n-seconds of reading
#seconds = 1
#fps = 100 * seconds


def collectData(inlet):
	channel_data = []
	for i in range(1): # n frames/second will be collected
		channel = []
		for i in range(8): # n electroid channels
        		sample, timestamp = inlet.pull_sample()
        		channel.append(sample[:60])

		channel_data.append(channel)

	np.save('testfile123', channel_data)

	print (channel_data)
"""
plt.plot(channel_data[0][2])
plt.show()
"""

"""
# outputs the FPS
	fps_counter.append(time.time() - last_print)
	last_print = time.time()
	cur_raw_hz = 1/(sum(fps_counter)/len(fps_counter))
	print(cur_raw_hz)

# used to plot the n-th frame
for i in range(2):
	for chan in channel_data:
		plt.plot(channel_data[chan][:60])
plt.show()
"""
