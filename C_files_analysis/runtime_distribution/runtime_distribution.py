import os
import subprocess
import re
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


#histogram saved in a file
def plot_bar_chart(results, bar_chart_file):
    names = list(results.keys())
    native_times = []
    wasm_times = []
    wasm_obf_times = []
    native_obf_times = []
    
    for values in results.values():
        native_times.append(values[0] if values[0] is not None else np.nan)
        wasm_times.append(values[1] if values[1] is not None else np.nan)
        wasm_obf_times.append(values[2] if values[2] is not None else np.nan)
        native_obf_times.append(values[3] if values[3] is not None else np.nan)
    
    
    x = np.arange(len(names))
    width = 0.2  

    fig, ax = plt.subplots(figsize=(12, 6))

    
    ax.bar(x - width, native_times, width, label='Binary', color='red')
    ax.bar(x, wasm_times, width, label='WASM', color='blue')
    ax.bar(x + width, wasm_obf_times, width, label='WASM Obfuscated', color='green')
    ax.bar(x + 2*width, native_obf_times, width, label='Native Obfuscated', color='brown')

    
    ax.set_xlabel('File')
    ax.set_ylabel('Seconds')
    ax.set_title(f'Runtime')
    ax.set_xticks(x + width)
    ax.set_xticklabels(names, rotation=45, ha="right")
    ax.legend()

    plt.tight_layout()
    plt.savefig(bar_chart_file)  
    plt.close()
    
    
def overhead(native_times, other_times):
    return [(time / native - 1) * 100 if native is not None and native > 0 else np.nan
            for native, time in zip(native_times, other_times)]

#boxplot saved in a file
def plot_boxplot_chart(results, boxplot_file):
    names = list(results.keys())
    
    
    native_times = []
    wasm_times = []
    wasm_obf_times = []
    native_obf_times = []
    
    for values in results.values():
        native_times.append(values[0] if values[0] is not None else np.nan)
        wasm_times.append(values[1] if values[1] is not None else np.nan)
        wasm_obf_times.append(values[2] if values[2] is not None else np.nan)
        native_obf_times.append(values[3] if values[3] is not None else np.nan)
    
    
    #overheads
    overhead_wasm = overhead(native_times, wasm_times)
    overhead_wasm_obf = overhead(native_times, wasm_obf_times)
    overhead_native_obf = overhead(native_times, native_obf_times)

    avg_overhead_wasm = np.nanmean(overhead_wasm)
    avg_overhead_wasm_obf = np.nanmean(overhead_wasm_obf)
    avg_overhead_native_obf = np.nanmean(overhead_native_obf)
    
    
    data = [native_times, wasm_times, wasm_obf_times, native_obf_times]
    labels = ['Binary', 'WASM', 'WASM Obfuscated', 'Native Obfuscated']

    fig, ax = plt.subplots(figsize=(12, 6))

   
    ax.boxplot(data, vert=False, patch_artist=True, labels=labels, 
               boxprops=dict(facecolor='lightgray', color='gray'),
               flierprops=dict(marker='o', color='red', markersize=5),
               medianprops=dict(color='black'))

    
    ax.set_xlabel('Seconds')
    ax.set_title(f'Runtime Distribution\n'
                 f'Overhead WASM: {avg_overhead_wasm:.2f}% | '
                 f'Overhead WASM Obfuscated: {avg_overhead_wasm_obf:.2f}% | '
                 f'Overhead Native Obfuscated: {avg_overhead_native_obf:.2f}%')

    plt.tight_layout()
    plt.savefig(boxplot_file) 
    plt.close()


def load_csv(csv_file):
    df = pd.read_csv(csv_file)
    results = {}
    for index, row in df.iterrows():
        results[row['name']] = [row['native'], row['wasm'], row['wasm_obfuscated'], row['native_obfuscated']]
    return results


runtime_results = load_csv('runtime_results.csv')
bar_chart_file = 'bar_chart_runtime_distribution.pdf'  
boxplot_file = 'boxplot_runtime_distribution.pdf' 

plot_bar_chart(runtime_results, bar_chart_file)
plot_boxplot_chart(runtime_results, boxplot_file)



