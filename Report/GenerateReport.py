import Analysis
import datetime
import csv
def read_offsets():
    out=''
    count=0
    with open(path+'/offsets.csv','r') as csvfile:
        plots = csv.reader(csvfile, delimiter=',')
        for row in plots:
            if count > 0:
                out+=', '+row[0]
            else:
                out+=row[0]
            count+=1
    return out
def main():
    serial_number=''
    data_path=''
    offsets=''
    date = datetime.datetime.now().split(' ')[0]
    for arg in sys.argv:
        if arg.split('=')[0]=='serial_number':
            serial_number=arg.split('=')[1]
    path=data_path+'/'+serial_number
    offsets=read_offsets()

    Analysis.data='bias'
    Analysis.path = data_path+'/'+serial_number
    Analysis.trial_id = '1'
    Analysis.ave_time='1'
    Analysis.num_points=15
    Analysis.show_plot='y'
    Analysis.save_plot='n'
    bias_out=Analysis.analyze()

    Analysis.data='dac'
    Analysis.path = data_path+'/'+serial_number
    Analysis.trial_id = '1'
    Analysis.ave_time='1'
    Analysis.num_points=15
    Analysis.show_plot='y'
    Analysis.save_plot='n'
    dac_out=Analysis.analyze()

    Analysis.data='current'
    Analysis.path = data_path+'/'+serial_number
    Analysis.trial_id = '1'
    Analysis.ave_time='1'
    Analysis.num_points=15
    Analysis.show_plot='y'
    Analysis.save_plot='n'
    1ms_current_out=Analysis.analyze()

    Analysis.data='current'
    Analysis.path = data_path+'/'+serial_number
    Analysis.trial_id = '1'
    Analysis.ave_time='100'
    Analysis.num_points=15
    Analysis.show_plot='y'
    Analysis.save_plot='n'
    100ms_current_out=Analysis.analyze()

    document=r'''
    %\documentclass{revtex4-1}
    \documentclass{article}%
    %\usepackage{amsmath}%
    %\usepackage{amsfonts}%
    \usepackage{amssymb}%
    \usepackage{graphicx,float}
    \usepackage{amsmath}
    \usepackage{geometry}
    \usepackage{booktabs}
    \usepackage{float}
    \usepackage{makecell}
    \geometry{letterpaper}


    \begin{document}

    \title{NSLS2\_EM Serial \#'''+serial_number+''' Test Report}
    \author{Kon Aoki}
    %\\Colorado College}
    \date{'''+date+'''}
    \maketitle

    \section{Summary}
    The NSLS2\_EM electrometer serial \#'''+serial_number+''' was tested for its accuracy of readouts.

    %PROCEDURE
    \section{Procedure}
    \begin{enumerate}
    	\item Record ADC offsets
    	\item Grounding
    		\begin{enumerate}
    			\item Confirm chassis ground to mains ground
    			\item Confirm outer conductor of coax connector grounded to chassis
    		\end{enumerate}
    	\item Bias (Test date: '''+date+''')
    		\begin{enumerate}
    			\item Set bias via EPICS \label{itm:1s}
    			\item Measure and record bias output
    			\item Repeat measurement 3 times \label{itm:1l}
    			\item Repeat procedure \ref{itm:1s}-\ref{itm:1l} for biases -10 to 10V in 1V increments
    		\end{enumerate}
    	\item DAC Output (Test date: '''+date+''')
    		\begin{enumerate}
    			\item Set DAC via EPICS \label{itm:2s}
    			\item Measure and record DAC output \label{itm:2s2}
    			\item Repeat measurement 3 times \label{itm:2l}
    			\item Repeat procedure \ref{itm:2s}-\ref{itm:2l} for outputs -10 to 10V in 1V increments \label{itm:l2}
    			\item Repeat all steps for each channel
    		\end{enumerate}
    	\item Current measurement at 1ms averaging time (Test date: '''+date+''')
    		\begin{enumerate}
    			\item Set values per read to 50
    			\item Set averaging time to 1ms
    			\item Set number of points to collect to 100
    			\item Set ADC offset
    			\item Set range \label{itm:3s}
    			\item Set input current \label{itm:3s2}
    			\item Wait 5.1 seconds until data is ready (averaging time $\times$ number of points $+$ $5$s buffer)
    			\item Record current measurement \label{itm:3l}
    			\item Repeat procedure \ref{itm:3s2}-\ref{itm:3l} for 15 inputs between 0 and 20\% above the range setting
    			\item Repeat procedure \ref{itm:3s}-\ref{itm:3l} for ranges 1$\mu$A to 50mA
    			\item Repeat all steps for each channel
    		\end{enumerate}
    	\item Current measurement at 100ms averaging time (Test date: '''+date+''')
    		\begin{enumerate}
    			\item Set values per read to 50
    			\item Set averaging time to 100ms
    			\item Set number of points to collect to 100
    			\item Set ADC offset
    			\item Set range \label{itm:4s}
    			\item Set input current \label{itm:4s2}
    			\item Wait 15 seconds until data is ready (averaging time $\times$ number of points $+$ $5$s buffer)
    			\item Record current measurement \label{itm:4l}
    			\item Repeat procedure \ref{itm:4s2}-\ref{itm:4l} for 15 inputs between 0 and 20\% above the range setting
    			\item Repeat procedure \ref{itm:4s}-\ref{itm:4l} for ranges 1$\mu$A to 50mA
    			\item Repeat all steps for each channel
    		\end{enumerate}
    \end{enumerate}

    %RESULTS
    \section{Results}
    ADC Offsets were set at '''+offsets+'''. \\
    Confirmed chassis ground to mains ground\\
    Confirmed outer conductor of coax connector grounded to chassis.
    %Bias
    \subsection{Bias Voltage}
    \begin{figure}[H]
    	\centering
    	\includegraphics[width=1\textwidth]{plot/bias.png}
    	\caption{Bias Voltage}
    	\label{fig_bias}
    \end{figure}

    \begin{table}[H]
    \centering
    \begin{tabular}{|l|l|l|}
    \hline
    Slope & Offset (V) & Median STD (V)\\ \hline
    '''+bias_out+'''
    \end{tabular}
    \end{table}

    %DAC
    \subsection{DAC Output}
    \begin{figure}[H]
    	\centering
    	\includegraphics[width=1\textwidth]{plot/dac.png}
    	\caption{DAC Output}
    	\label{fig_dac}
    \end{figure}
    \begin{table}[H]
    \centering
    \begin{tabular}{|l|l|l|l|}
    \hline
    Channel & Slope & Offset (V) & Median STD (V)\\ \hline
    '''+dac_out+'''
    \end{tabular}
    \end{table}

    %CURRENT MEASUREMENT 1ms
    \subsection{Current Measurement 1ms Averaging Time}
    *Note that measurements taken from input values above the range setting was ignored for the model for ranges 1$\mu$A to 1mA. For the 50mA range, input values above 40mA (80\%) was ignored for the model.
    \begin{figure}[H]
    	\centering
    	\includegraphics[width=0.55\textwidth]{plot/1ms_range1.png}
    	\caption{Range 1$\mu$A}
    	\label{fig_adc}
    \end{figure}
    \begin{figure}[H]
    	\centering
    	\includegraphics[width=0.55\textwidth]{plot/1ms_range10.png}
    	\caption{Range 10$\mu$A}
    	\label{fig_adc2}
    \end{figure}
    \begin{figure}[H]
    	\centering
    	\includegraphics[width=0.55\textwidth]{plot/1ms_range100.png}
    	\caption{Range 100$\mu$A}
    	\label{fig_adc3}
    \end{figure}
    \begin{figure}[H]
    	\centering
    	\includegraphics[width=0.55\textwidth]{plot/1ms_range1000.png}
    	\caption{Range 1mA}
    	\label{fig_adc4}
    \end{figure}
    \begin{figure}[H]
    	\centering
    	\includegraphics[width=0.55\textwidth]{plot/1ms_range50000.png}
    	\caption{Range 50mA}
    	\label{fig_adc5}
    \end{figure}
    \begin{table}[H]
    \centering
    \begin{tabular}{|l|l|l|l|l|}
    \hline
    Channel & Range ($\mu$A) & Slope & Offset ($\mu$A) & Median STD ($\mu$A)\\ \Xhline{3\arrayrulewidth}
    '''+1ms_current_out+'''
    \end{tabular}
    \end{table}

    %CURRENT MEASUREMENT 100ms
    \subsection{Current Measurement 100ms Averaging Time}
    *Note that measurements taken from input values above the range setting was ignored for the model for ranges 1$\mu$A to 1mA. For the 50mA range, input values above 40mA (80\%) was ignored for the model.

    \begin{figure}[H]
    	\centering
    	\includegraphics[width=0.55\textwidth]{plot/100ms_range1.png}
    	\caption{Range 1$\mu$A}
    	\label{fig_adc}
    \end{figure}
    \begin{figure}[H]
    	\centering
    	\includegraphics[width=0.55\textwidth]{plot/100ms_range10.png}
    	\caption{Range 10$\mu$A}
    	\label{fig_adc2}
    \end{figure}
    \begin{figure}[H]
    	\centering
    	\includegraphics[width=0.55\textwidth]{plot/100ms_range100.png}
    	\caption{Range 100$\mu$A}
    	\label{fig_adc3}
    \end{figure}
    \begin{figure}[H]
    	\centering
    	\includegraphics[width=0.55\textwidth]{plot/100ms_range1000.png}
    	\caption{Range 1mA}
    	\label{fig_adc4}
    \end{figure}
    \begin{figure}[H]
    	\centering
    	\includegraphics[width=0.55\textwidth]{plot/100ms_range50000.png}
    	\caption{Range 50mA}
    	\label{fig_adc5}
    \end{figure}

    \begin{table}[H]
    \centering
    \begin{tabular}{|l|l|l|l|l|}
    \hline
    Channel & Range ($\mu$A) & Slope & Offset ($\mu$A) & Median STD ($\mu$A)\\ \Xhline{3\arrayrulewidth}
    '''+100ms_current_out+'''
    \end{tabular}
    \end{table}


    \end{document}
    '''

    f = open(data_path+"../Unit"+serial_number+"_report.tex","w")
    f.write(document)
    f.close()
