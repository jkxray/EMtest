from analysis_config import *
import current_analysis
import bias_analysis
import dac_analysis
import drift_analysis
def main():
    analyze()
def analyze():
    if data == 'bias':
        return bias_analysis.bias()

    elif data == 'dac':
        dac_analysis.dac()

    elif data == 'current':
        current_analysis.current()
    else:
        print("Not supported.")
