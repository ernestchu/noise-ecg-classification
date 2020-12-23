for i in {100..234}
do
    echo ${i}
    python3 gen_data.py ../mit-bih-arrhythmia-database-1.0.0/${i}
done
