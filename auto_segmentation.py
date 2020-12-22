import wfdb
from biosppy.signals import ecg
import numpy as np
import matplotlib.pyplot as plt
filename = 'mit-bih-noise-stress-test-database-1.0.0/119e24'
record_preview = wfdb.rdrecord(filename, sampto=3000)
annotation_preview = wfdb.rdann(filename, 'atr', sampto=3000)
signal, fields = wfdb.rdsamp(filename)
annotation = wfdb.rdann(filename, 'atr')

MLII_raw = signal[:, 0]
V1_raw = signal[:, 1]

MLII = ecg.ecg(MLII_raw, fields['fs'], show=False)
V1 = ecg.ecg(V1_raw, fields['fs'], show=False)

# plt.plot(MLII['templates_ts'], MLII['templates'].mean(axis=0))
# plt.title('Heartbeat template')
# plt.show()

# log
print('\n'+'-'*20 + 'MLII' + '-'*20)
print('Raw:', MLII_raw)
print('Segmentation score:', ecg.compare_segmentation(annotation.sample, MLII['rpeaks'])['performance'])
print('\n'+'-'*20 + 'V1' + '-'*20)
print('Raw:', V1_raw)
print('Segmentation score:', ecg.compare_segmentation(annotation.sample, V1['rpeaks'])['performance'])

print('\n'+'-'*20 + 'Annotation' + '-'*20)
print('Number of annotations:', len(annotation.sample))
print('Locations:', annotation.sample)
print('Labels:', annotation.symbol[:10])

# help(wfdb.Annotation)
# wfdb.plot_wfdb(record=record_preview, annotation=annotation_preview, plot_sym=True,
#                time_units='seconds', title='MIT-BIH Record 100',
#                figsize=(10,4), ecg_grids='all')
