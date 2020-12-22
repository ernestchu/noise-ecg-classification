import wfdb
import wfdb.processing
import numpy as np
import matplotlib.pyplot as plt
filename = 'mit-bih-noise-stress-test-database-1.0.0/119e24'
record_preview = wfdb.rdrecord(filename, sampto=3000)
annotation_preview = wfdb.rdann(filename, 'atr', sampto=3000)
signal, fields = wfdb.rdsamp(filename)
annotation = wfdb.rdann(filename, 'atr')

MLII = signal[:, 0]
V1 = signal[:, 1]
print(fields['fs'])

MLII_qrs = wfdb.processing.xqrs_detect(MLII, fields['fs'])
MLII_hr = wfdb.processing.compute_hr(fields['sig_len'], MLII_qrs, fields['fs'])
# radius(segment length) = samples/1 heart beat
MLII_peaks = wfdb.processing.find_local_peaks(MLII, int((1/np.nanmean(MLII_hr))*60*fields['fs']))

V1_qrs = wfdb.processing.xqrs_detect(V1, fields['fs'])
V1_hr = wfdb.processing.compute_hr(fields['sig_len'], V1_qrs, fields['fs'])
V1_peaks = wfdb.processing.find_local_peaks(V1, int((1/np.nanmean(V1_hr))*60*fields['fs']))

print('-'*20 + 'MLII' + '-'*20)
print('Raw:', MLII)
print('Heart rate:', np.nanmean(MLII_hr))
print('Number of heart beat', len(MLII_peaks))
print('-'*20 + 'V1' + '-'*20)
print('Raw:', V1)
print('Heart rate:', np.nanmean(V1_hr))
print('Number of heart beat', len(V1_peaks))

print('-'*20 + 'Annotation' + '-'*20)
print('Number of annotations:', len(annotation.sample))
print('Locations:', annotation.sample)
print('Labels:', annotation.symbol[:10])

fig, ax = plt.subplots(2)
ax[0].plot(range(len(MLII_hr)), MLII_hr)
ax[0].set_title('MLII')
ax[1].plot(range(len(V1_hr)), V1_hr)
ax[1].set_title('V1')
plt.show()

# help(wfdb.Annotation)
# wfdb.plot_wfdb(record=record_preview, annotation=annotation_preview, plot_sym=True,
#                time_units='seconds', title='MIT-BIH Record 100',
#                figsize=(10,4), ecg_grids='all')
