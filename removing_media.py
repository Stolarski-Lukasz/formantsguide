import os
import glob
import time


# 18000 seconds = 5h
def delete_old_images(seconds=18000):
    # removing spectrograms older than 18000 seconds
    list_of_spectrograms = glob.glob('media/spectrograms/*.*')
    for file in list_of_spectrograms:
        if time.time() - os.stat(file).st_mtime > seconds:
            print("removed spectrogram", file)
            os.remove(file)
        else: 
            print("not removed spectrogram", file)
    # removing spectrums older than 18000 seconds
    list_of_spectrums = glob.glob('media/spectrums/*.*')
    for file in list_of_spectrums:
        if time.time() - os.stat(file).st_mtime > seconds:
            print("removed spectrum", file)
            os.remove(file)
        else: 
            print("not removed spectrum", file)


delete_old_images()
