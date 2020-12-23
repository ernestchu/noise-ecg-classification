import wfdb
from biosppy.signals import ecg
import h5py
import numpy as np
import sys
import os

for filename in ('118','119'):
    signal, fields = wfdb.rdsamp('./mit-bih-arrhythmia/'+filename)
    annotation = wfdb.rdann('./mit-bih-arrhythmia/'+filename, 'atr')
    fs = fields['fs'] # sample rate

    MLII_raw = signal[:, 0]
    V1_raw = signal[:, 1]

    MLII = ecg.ecg(MLII_raw, fs, show=False)
    V1 = ecg.ecg(V1_raw, fs, show=False)

    filename_prefix = './data_no/'+filename+'/'
    os.mkdir(filename_prefix)
    for i, sample in enumerate(annotation.sample):
        with h5py.File(filename_prefix+str(i)+'.h5', 'w') as f:
            f.create_dataset('MLII', data=MLII['filtered'][int(sample-0.25*fs):int(sample+0.45*fs)])
            f.create_dataset('V1', data=V1['filtered'][int(sample-0.25*fs):int(sample+0.45*fs)])
            f.create_dataset('label', data=annotation.symbol[i])
            f.create_dataset('SNR', data='no')
