from pylsl import StreamInlet, resolve_stream
import Settings
import time
import os
import numpy as np

flag = False

def connectEEG():
# finding eeg and starting stream
# TODO: Add Try/Catch
	print("looking for an EEG stream...")
	streams = resolve_stream('type', 'EEG')

	inlet = StreamInlet(streams[0])
	print("connected")

	return (inlet)

def collectData(inlet, user, pathDir):
	channel_data = []
	while(Settings.whileTrue):
		channel = []
		for i in range(8):
			sample, timestamp = inlet.pull_sample()
			channel.append(sample[:60])
		channel_data.append(channel)
	saveData(channel_data, user, pathDir)

def saveData(data, user, pathDir):
	currTime = time.time()
	np.save(os.path.join(f"{pathDir}", f"{user}{currTime}.npy"),
					np.array(data).reshape(-1,8,60))
