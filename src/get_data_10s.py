import h5py
import matplotlib.pyplot as plt
snr_check = []
for i in range(0, 648000, 3600):
    with h5py.File('../data/119e24/'+str(i)+'.h5', 'r') as f:
        snr_check.append(0 if str(f['SNR'][()], 'utf-8')=='clean' else 1)
plt.plot(range(len(snr_check)), snr_check)
plt.show()

# ecg = None
# with h5py.File('../data/119e24/1400.h5', 'r') as f:
#     print(f['id'][()])
#     print(len(f['MLII'][:]))
#     print(str(f['SNR'][()], 'utf-8'))
#     ecg = f['MLII'][:]
# plt.plot(range(len(ecg)), ecg)
# plt.show()
