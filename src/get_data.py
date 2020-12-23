import h5py
import matplotlib.pyplot as plt
# snr_check = []
# for i in range(2300):
#     with h5py.File('../data/118e24/'+str(i)+'.h5', 'r') as f:
#         snr_check.append(0 if str(f['SNR'][()], 'utf-8')=='no' else 1)
# plt.plot(range(len(snr_check)), snr_check)
# plt.show()

ecg = None
with h5py.File('../data/118e_6/1400.h5', 'r') as f:
    print(f['id'][()])
    print(len(f['MLII'][:]))
    print(len(f['V1'][:]))
    print(str(f['label'][()], 'utf-8'))
    print(str(f['SNR'][()], 'utf-8'))
    ecg = f['MLII'][:]
plt.plot(range(len(ecg)), ecg)
plt.show()
