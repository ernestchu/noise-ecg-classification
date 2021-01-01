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

is_noise = False
every_two_minute = 0
all_clean = False
if len(filename.split('/')[-1]) == 3: # 118, 119
    all_clean = True
filename_prefix = '../data_10s/'+filename.split('/')[-1]+'/'
os.mkdir(filename_prefix)
for i in range(0, len(MLII_raw), fs*10):
    with h5py.File(filename_prefix+str(i)+'.h5', 'w') as f:
        if (i-5*60*fs) >= (2*60*fs)*every_two_minute and not all_clean:
            is_noise = not is_noise
            every_two_minute += 1
        f.create_dataset('index', data=i)
        f.create_dataset('MLII', data=MLII_raw[i:i+fs*10])
        f.create_dataset('SNR', data=(filename[-2:] if is_noise else 'clean'))
