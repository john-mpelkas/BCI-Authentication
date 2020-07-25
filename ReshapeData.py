import numpy as np
import os

def reshape():

    # Retrives files in the specified directory
    # NOTE: Change os.walk directory where data files live
    files = []
    for dirname, dirnames, filenames in os.walk(r'C:\Users\mpelkasj\Desktop\EEG_Data'):
        for filename in filenames:
            files.append(os.path.join(dirname, filename))

    # Resize arrays and Unrollto append it to file
    f = open('masterFile.txt', 'ab')
    for file in files:
        x = np.load(file)
        x = x[:275, :8, :60]
        x = x.reshape(1, -1)
        np.savetxt(f, x, delimiter=' ')

reshape()
