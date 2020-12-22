import wfdb
from biosppy.signals import ecg
import h5py
import numpy as np
import sys
import os
filename = sys.argv[1]
signal, fields = wfdb.rdsamp(filename)
annotation = wfdb.rdann(filename, 'atr')
fs = fields['fs'] # sample rate

MLII_raw = signal[:, 0]
V1_raw = signal[:, 1]

MLII = ecg.ecg(MLII_raw, fs, show=False)
V1 = ecg.ecg(V1_raw, fs, show=False)

is_noise = False
every_two_minute = 0
filename_prefix = '../data/'+filename[-6:]+'/'
os.mkdir(filename_prefix)
for i, sample in enumerate(annotation.sample):
    with h5py.File(filename_prefix+str(i)+'.h5', 'w') as f:
        f.create_dataset('id', data=i)
        f.create_dataset('MLII', data=MLII['filtered'][int(sample-0.25*fs):int(sample+0.45*fs)])
        f.create_dataset('V1', data=V1['filtered'][int(sample-0.25*fs):int(sample+0.45*fs)])
        f.create_dataset('label', data=annotation.symbol[i])
        f.create_dataset('SNR', data=(filename[-2:] if is_noise else 'no'))
        if (sample-5*60*fs) > (2*60*fs)*every_two_minute:
            is_noise = not is_noise
            every_two_minute += 1
