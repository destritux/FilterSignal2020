import os
import uteis
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time 

# Criando variaveis globais
HPF = 0.5
LPF = 32
NOTCH = 60
SampleRate = 250
quality = 10
coluna = 0

# ------- Selecionar arquivo ---------
print('-='*30)
print('-----------  VERIFIQUE SE OS ARQUIVOS name.txt e uteis.py ENCONTRAM-SE NESTA PASTA!!    -----------')
time.sleep(4)

try:
    name_id_file = open('name.txt', 'r')
    
    HPF = float(input("Me diga o HighPass: ", ))
    LPF = float(input("Me diga o LowPass: ", ))
    NOTCH = float(input("Me diga o NOTCH: ", ))
    print(f"\nValores de HPF, LPF e NOTCH:")
    print(f"HighPass = {HPF}")
    print(f"LowPass = {LPF}")
    print(f"NOTCH = {NOTCH}")



    # ------- Dados para filtragem ----------------


    lowcut = np.float16(HPF)
    highcut = np.int8(LPF)
    fs = np.int16(SampleRate) 
    f0 = np.int8(NOTCH)
    Q = np.int8(quality)  # Quality factor for the NOTCH FILTER = 10
    w0 = np.float16(f0 / (fs / 2))  # Normalized Frequency


    for line in name_id_file:
        line = line.rstrip('\n')

        file_name = os.path.splitext(line)[0] # Isso retira a extensão do final do arquivo
        data = pd.read_csv(line, delimiter=",", usecols=[coluna], skiprows=500, dtype=np.float32, engine='c', low_memory=True)
        
        numpy_array = np.array(data, dtype=np.float32)
        data = numpy_array.ravel()

        uteis.create_dir(file_name)

        # ------- Salvando dados --------------------
        print("-="*30)
        print("\nSeparando e filtrando dados para "+file_name+", isso pode demorar um pouco...")
        h = uteis.notch_filter(w0, Q, data) #Retira as frequencias do data
        y = uteis.butter_bandpass_filter(h, lowcut, highcut, fs, order=4)
        datafilt = np.array(y, dtype=np.float32) #transforma o resultado da função em array
        
        uteis.create_grafic(file_name, y, h, datafilt, data, fs)

    name_id_file.close
except TypeError as err:
    print(f'Algo deu errado. O erro foi \n{err}')