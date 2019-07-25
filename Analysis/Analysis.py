from analysis_config import *
import current_analysis
import bias_analysis
import dac_analysis
import drift_analysis
def main():
    analyze()
def analyze():
    if data == 'bias':
        return bias_analysis.bias(path,show_plot,save_plot)

    elif data == 'dac':
        return dac_analysis.dac(path,show_plot,save_plot)

    elif data == 'current':
        return current_analysis.current(path,ave_time,num_points,show_plot,save_plot)
    else:
        print("Not supported.")
