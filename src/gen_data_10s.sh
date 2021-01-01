dataset="118e_6 118e00 118e06 118e12 118e18 118e24 119e_6 119e00 119e06 119e12 119e18 119e24"
for d in ${dataset}
do
python3 gen_data_10s.py ../mit-bih-noise-stress-test-database-1.0.0/${d}
done

dataset_clean="118 119"
for d in ${dataset_clean}
do
python3 gen_data_10s.py ../mit-bih-arrhythmia/${d}
done

