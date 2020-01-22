# FilterSignal2020
> Filter for electrophysiological signals of plants and plot of graphs (Autocorrelation, Density, RAW signal, Filtered signal, FFT, PSD, Lag Scatter)


<p> The program uses the name.txt file to analyze several electrophysiological data files, using the following steps: </p>
  <p> 1 - Remove the frequencies above, below and noise </p>
   <p> 2 - Filter the data using the scipy.signal.filtfilt library (https://docs.scipy.org/doc/scipy-0.18.1/reference/generated/scipy.signal.filtfilt.html)</p >
   <p> 3 - Plot the graphs using the filtered data (Autocorrelation, Density, RAW signal, Filtered signal, FFT, PSD, Lag Scatter) </p>![](../header.png)

## Use
For use, fill in the name.txt file with the names of the files where the raw data is located.
If the data contains more than one column (Ex: OpenBCI) check the variable 'column' to ensure that the data will be read correctly.

## Meta

Thiago Carvalho – [@destritux](https://twitter.com/destritux) – destritux@gmail.com

Distributed under the MIT license. See `LICENSE` for more information.


> Filtro para sinais eletrofisiologicos de plantas e Plot de graficos (Autocorrelação, Densidade, sinal RAW, sinal Filtrado, FFT,  PSD, Lag Scatter)

<p>O programa utiliza do arquivo name.txt para analizar varios arquivos de dados eletrofisiologico, através dos seguintes passos:</p>
 <p>1 - Retira as frequências acima, abaixo e ruido</p>
  <p>2 - Filtra os dados utilizando a biblioteca scipy.signal.filtfilt (https://docs.scipy.org/doc/scipy-0.18.1/reference/generated/scipy.signal.filtfilt.html)</p>
  <p>3 - Plota os graficos utilizando os dados filtrados (Autocorrelation, Density, RAW signal, Filtered signal, FFT, PSD, Lag Scatter)</p>![](../header.png)

## Exemplo de uso
Para uso, preencha o arquivo name.txt com os nome dos arquivos onde encontra-se os dados brutos. 
Caso os dados contenham mais de uma coluna (Ex: OpenBCI) verifique a variavel 'coluna' para garantia de que os dados seram lidos corretamente. 

## Meta

Thiago Carvalho – [@destritux](https://twitter.com/destritux) – destritux@gmail.com

Distribuído sob a licença MIT. Veja `LICENSE` para mais informações.
