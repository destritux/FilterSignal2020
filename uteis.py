import os
import io
from scipy import signal
import shutil
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image
from obspy.signal.tf_misfit import plot_tfr
from statsmodels.graphics.tsaplots import plot_pacf

# Criando variaveis configuracao grafico
plt.rcParams['agg.path.chunksize'] = 10000
plt.rcParams['figure.dpi'] = 100
plt.rcParams['savefig.dpi'] = 500
Plt_color = 'black'
Plt_width = '0.8'
plt.rcParams['savefig.dpi'] = 500

def notch_filter(w0, Q, data):
    """
    ->Rejeita uma banda de frequência estreita e deixa o resto do espectro pouco alterado.
    :param w0: float
              Frequência para remover de um sinal. Se fs for especificado, ele estará 
              nas mesmas unidades que fs. Por padrão, é um escalar normalizado que deve
              satisfazer 0 < w0 < 1, com w0 correspondente a metade da frequência de 
              amostragem.
    :param Q: float
              Fator de qualidade. Parâmetro sem dimensão que caracteriza o filtro 
              de entalhe -3 dB de largura de banda bw em relação à sua frequência 
              central, Q = w0 / bw.
    :param data: array_like
              O sinal a ser filtrado. 
               
    :return: A saída filtrada com a mesma forma que data.
    
    Thiago Carvalho @destritux
    """
    b, a = signal.iirnotch(w0, Q)
    h = signal.filtfilt(b, a, data)
    return h


def butter_bandpass(lowcut, highcut, fs, order):
    """
    -> Design de filtro analógico e digital Butterworth. Projete um filtro 
    Butterworth digital ou analógico de nona ordem e retorne os coeficientes do 
    filtro. A resposta em frequência de um filtro Butterworth é muito plana
    (não possui ripple, ou ondulações) na banda passante, e se aproxima do 
    zero na banda rejeitada.

    :param lowcut:  float
                   Valor do LowPass
    :param highcut: float
                   Valor do HighPass
    :param fs:      int
                   Valor do SampleRate     
    :param order:   int
                   A ordem do filtro. 
    :return:       Polinômios do numerador (b) e do denominador (a) do filtro 
                   IIR. Somente retornado se output = 'ba'.
    
    Thiago Carvalho @destritux    
    """
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = signal.butter(order, [low, high], btype='bandpass')
    return b, a

def butter_bandpass_filter(h, lowcut, highcut, fs, order):
    """
    -> Esta função aplica um filtro digital linear duas vezes, uma para frente e 
    outra para trás. O filtro combinado tem fase zero e um filtro solicita o dobro
    do original. A função fornece opções para lidar com as bordas do sinal.
    :param h:       array_like
                   dados a serem tratados
    :param lowcut:  float
                   Valor do LowPass
    :param highcut: float
                   Valor do HighPass
    :param fs:      int
                   Valor do SampleRate  
    :param order:   int
                   A ordem do filtro.
    :return: Dados filtrados
    
    Thiago Carvalho @destritux
    """
    b, a = butter_bandpass(lowcut, highcut, fs, order)
    y = signal.filtfilt(b, a, h)
    return y

def save_file(save_data, save_name_file, ext='.txt'): 
    """
    ->Função que salva o arquivo de dados para futuro tratamento em outro Software
    :param save_data: array_like
             dados a serem salvos em um arquivo
    :param save_name_file: str
             nome do arquivo a ser salvo
    :param ext: str
            extenção do arquivo a ser salvo, .txt por padrão
    :return: Sem retorno  
    
    Thiago Carvalho @destritux      
    """
    save_name_file +=ext
    np.savetxt(save_name_file, save_data, fmt='%1.7f')  # 7 casas depois da vírgula
    return

def save_img_tiff(tiff_name_path_file, tiff_file_name, tiff_grafic_name):
    """
    -> Salva graficos em tiff
    :param tiff_name_path_file:
            Caminho para salvar a imagem
    :param tiff_file_name:
            Nome do arquivo recebido
    :param tiff_grafic_name:
            Nome da imagem a ser salva
    :return: Sem retorno
    
    Thiago Carvalho @destritux
    """
    # Save the image in memory in PNG format
    png1 = io.BytesIO()
    plt.savefig(png1, format="png")
    # Load this image into PIL
    png2 = Image.open(png1)
    # Save as TIFF
    png2.save(tiff_name_path_file +'/' + tiff_file_name + '_' + tiff_grafic_name +".tiff")
    png1.close()
    return

def create_grafic(create_grafic_file_name, y, h, create_grafic_datafilt, data, fs):
    """
    -> Cria os graficos 
    :param create_grafic_file_name: str
            Nome do arquivo que foi tratado
    :param y: array_like
            Dados filtrados
    :param h: array_like
            Dados filtrados retirado o noth
    :param create_grafic_datafilt: np.array
            Dados filtrados salvos tipo numpy
    :param data: array_like
            dados originais sem tratamento
    :param fs: int
            Valor do SampleRate  
    :return: Sem retorno
    
    Thiago Carvalho @destritux    
    """
    name_path_file = './'+create_grafic_file_name       
    os.makedirs(name_path_file)
    name = name_path_file +'/'+create_grafic_file_name+'_filtrado'
    save_file(y, name)

    print(f"\nCriando plot RAW SIGNAL...")
    plt.figure(1)
    plt.clf()
    plt.title("RAW signal ")
    plt.plot(data, color=Plt_color, linewidth=Plt_width)
    plt.ylabel("ΔV(mV)")
    plt.xlabel("time(s)")
    plt.tight_layout()

    grafic_name = str('RAW_SIGNAL')
    name_file = name_path_file +'/' +  create_grafic_file_name + '_' + grafic_name

    save_img_tiff(name_path_file, create_grafic_file_name, grafic_name)
    save_file(data, name_file)
    print("RAW SIGNAL concluído!")
    print("-="*30)

    print("\nCriando plot FILTERED SIGNAL...")
    plt.figure(2)
    plt.clf()
    plt.title("Filtered signal")
    plt.plot(create_grafic_datafilt, color=Plt_color, linewidth= Plt_width)
    plt.ylabel("ΔV(mV)")
    plt.xlabel("time(s)")
    plt.tight_layout()

    grafic_name = str('FILTERED_SIGNAL')
    name_file = name_path_file +'/' +  create_grafic_file_name + '_' + grafic_name

    save_img_tiff(name_path_file, create_grafic_file_name, grafic_name)
    save_file(y, name_file)
    print("FILTERED SIGNAL concluído!")
    print("-="*30)

    print("\nCriando plot FFT FILT...")
    plt.figure(3)
    plt.clf()
    plt.title("Fast Fourier Transform FILT")
    plt.magnitude_spectrum(create_grafic_datafilt, Fs=fs, color=Plt_color, linewidth= Plt_width)
    plt.ylabel("F")
    plt.xlabel('frequency (Hz)')
    plt.tight_layout()

    grafic_name = str('FFT_FILT')
    name_file = name_path_file +'/' +  create_grafic_file_name + '_' + grafic_name

    save_img_tiff(name_path_file, create_grafic_file_name, grafic_name)
    save_file(y, name_file)

    print("FFT FILT concluído!")
    print("-="*30)

    print("\nCriando plot FFT RAW...")
    plt.figure(4)
    plt.clf()
    plt.title("Fast Fourier Transform RAW...")
    plt.magnitude_spectrum(data, Fs=fs, color=Plt_color, linewidth= Plt_width)
    plt.ylabel("F")
    plt.xlabel('frequency (Hz)')
    plt.tight_layout()

    grafic_name = str('FFT_RAW')
    name_file = name_path_file +'/' +  create_grafic_file_name + '_' + grafic_name

    save_img_tiff(name_path_file, create_grafic_file_name, grafic_name)
    save_file(y, name_file) 
    print("FAST FOURIER TRANSFORM concluído!")
    print("-="*30)

    print("\nCriando plot PSD...")
    f_values, psd_values = signal.welch(create_grafic_datafilt, fs)

    plt.figure(5)
    plt.clf()
    plt.title("Power Spectral Density")  
    plt.plot(f_values, psd_values, linestyle='-', color=Plt_color, linewidth=Plt_width)
    plt.xlabel('frequency (Hz)')
    plt.ylabel('PSD')
    plt.tight_layout()
    
    grafic_name = str('PSD')
    name_file = name_path_file +'/' +  create_grafic_file_name + '_' + grafic_name

    save_img_tiff(name_path_file, create_grafic_file_name, grafic_name)
    save_file(y, name_file) 
    print("PSD concluído!")
    print("-="*30)

    print("\nCriando plot Histogram...")
    plt.figure(6)
    plt.clf()
    plt.title("Histogram")

    series = pd.Series(create_grafic_datafilt)
    series.hist(bins=44, grid=0)
    plt.tight_layout()    
    grafic_name = str('Histogram')
    name_file = name_path_file +'/' +  create_grafic_file_name + '_' + grafic_name

    save_img_tiff(name_path_file, create_grafic_file_name, grafic_name)
    #save_file(y, name_file) 
    print("Histogram concluído!")
    print("-="*30)
    plt.plot()

    print("\nCriando plot Density...")
    plt.figure(7)
    plt.clf()
    plt.title("Density")
    series.plot(kind='kde')
    plt.tight_layout()    
    grafic_name = str('Density')
    name_file = name_path_file +'/' +  create_grafic_file_name + '_' + grafic_name

    save_img_tiff(name_path_file, create_grafic_file_name, grafic_name)
    print("Density concluído!")
    print("-="*30)
    plt.plot()

    print("\nCriando plot Lag Scatter...")
    plt.figure(8)
    plt.clf()
    plt.title("Lag Scatter")

    pd.plotting.lag_plot(series)

    plt.tight_layout()    
    grafic_name = str('Lag Scatter')
    name_file = name_path_file +'/' +  create_grafic_file_name + '_' + grafic_name

    save_img_tiff(name_path_file, create_grafic_file_name, grafic_name)
    print("Lag Scatter concluído!")
    print("-="*30)
    plt.plot()  

    print("\nCriando plot Autocorrelation...")
    plt.figure(9)
    plt.clf()
    plt.title("Autocorrelation")

    pd.plotting.autocorrelation_plot(series)

    plt.tight_layout()    
    grafic_name = str('Autocorrelation')
    name_file = name_path_file +'/' +  create_grafic_file_name + '_' + grafic_name

    save_img_tiff(name_path_file, create_grafic_file_name, grafic_name)
    print("Autocorrelation concluído!")
    print("-="*30)
    plt.plot() 
    return

def create_dir(create_dir_file_name):
    """
    -> Cria o diretorio para salvar os graficos e arquivos de dados, caso já 
    exista ele exclui o diretorio existente.
    :param create_dir_file_name: str
            Nome do diretorio a ser criado.
    :return: Sem retorno

    Thiago Carvalho @destritux
    """
    path_name = './'+create_dir_file_name
    if os.path.exists(path_name):
        shutil.rmtree(path_name, ignore_errors=False)
    return
