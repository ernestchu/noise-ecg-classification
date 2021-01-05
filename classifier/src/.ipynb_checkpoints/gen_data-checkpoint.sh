for i in {118..119}
do
    echo ${i}
    python3 gen_data.py ../../mit-bih-arrhythmia/${i}
done