import wfdb
from biosppy.signals import ecg
import h5py
import numpy as np
import sys
import os

# os.mkdir('./data_10s/')
for filename in ('118', '119', '118e_6', '118e00', '118e06', '118e12', '118e18', '118e24', '119e_6', '119e00', '119e06', '119e12', '119e18', '119e24'):
    if (len(filename) == 3):
        dir = './mit-bih-arrhythmia/'
    else:
        dir = './mit-bih-noise-stress-test-database-1.0.0/'
    signal, fields = wfdb.rdsamp(dir+filename)
    annotation = wfdb.rdann(dir+filename, 'atr')
    fs = fields['fs'] # sample rate

    MLII_raw = signal[:, 0]
    V1_raw = signal[:, 1]

    filename_prefix = './data_10s/'+filename+'/'
    # os.mkdir(filename_prefix)
    print(len(MLII_raw))
    # for i in range(0, len(MLII_raw), fs * 10):
    #     with h5py.File(filename_prefix+str(i)+'.h5', 'w') as f:
    #         f.create_dataset('MLII', data=MLII_raw[i:i+fs*10])
    #         f.create_dataset('V1', data=V1_raw[i:i+fs*10])
