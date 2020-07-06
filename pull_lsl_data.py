from pylsl import StreamInlet, resolve_stream
import time
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
from collections import deque

def connectEEG():
# finding eeg and starting stream
	print("looking for an EEG stream...")
	streams = resolve_stream('type', 'EEG')

	inlet = StreamInlet(streams[0])
	print("connected")

	return (inlet)

def collectData(inlet):
	channel_data = []
	for i in range(10): # n frames/second will be collected
		channel = []
		for i in range(8): # n electroid channels
				sample, timestamp = inlet.pull_sample()
				channel.append(sample[:60])
				print(sample)
		channel_data.append(channel)
	return(channel_data)

def saveData(user, pathDir, channel_data):
	currTime = time.time()
	np.save(os.path.join(f"{pathDir}", f"{user}{currTime}.npy"),
					np.array(channel_data).reshape(-1,8,60))
