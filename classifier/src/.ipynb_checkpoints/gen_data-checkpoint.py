import wfdb
from biosppy.signals import ecg
import h5py
import numpy as np
import sys
import os
symbols = 'NAVR'
filename = sys.argv[1]
signal, fields = wfdb.rdsamp(filename)
annotation = wfdb.rdann(filename, 'atr')
fs = fields['fs'] # sample rate

MLII_raw = signal[:, 0]
MLII = ecg.ecg(MLII_raw, fs, show=False)

filename_prefix = '../segmentation/'+filename[-3:]+'/'
os.mkdir(filename_prefix)
for i, sample in enumerate(annotation.sample):
    if annotation.symbol[i] in symbols:
        with h5py.File(filename_prefix+str(i)+'.h5', 'w') as f:
            f.create_dataset('index', data=i)
            f.create_dataset('MLII', data=MLII['filtered'][int(sample-0.25*fs):int(sample+0.45*fs)])
            f.create_dataset('label', data=annotation.symbol[i])
