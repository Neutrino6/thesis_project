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

#take 2 csv files: first one with emscripten + bynarien, second one with emscripten + wasm-mutate and clang + wasm-mutate
def plot2_boxplot_chart(results1, results2, boxplot_file):
    
    
    #results1 emscripten + bynarien
    native_times = []
    wasm_emscripten_times = []
    wasm_obf_emscripten_bynarien_times = []
    native_obf_times = []
    
    for values in results1.values():
        native_times.append(values[0] if values[0] is not None else np.nan)
        wasm_emscripten_times.append(values[1] if values[1] is not None else np.nan)
        wasm_obf_emscripten_bynarien_times.append(values[2] if values[2] is not None else np.nan)
        native_obf_times.append(values[3] if values[3] is not None else np.nan)
    
    #results2 emscripten + wasm-mutate and clang + wasm-mutate
    wasm_clang_times = []
    wasm_obf_clang_times = []
    wasm_obf_emscripten_times = []
    
    for values in results2.values():
        wasm_clang_times.append(values[0] if values[0] is not None else np.nan)
        wasm_obf_clang_times.append(values[1] if values[1] is not None else np.nan)
        wasm_obf_emscripten_times.append(values[2] if values[2] is not None else np.nan)
    
    #overheads
    overhead_wasm_emscripten = overhead(native_times, wasm_emscripten_times)
    overhead_wasm_obf_emscripten_bynarien = overhead(native_times, wasm_obf_emscripten_bynarien_times)
    overhead_native_obf = overhead(native_times, native_obf_times)
    overhead_wasm_clang = overhead(native_times, wasm_clang_times)
    overhead_wasm_obf_clang = overhead(native_times, wasm_obf_clang_times)
    overhead_wasm_obf_emscripten = overhead(native_times, wasm_obf_emscripten_times)

    avg_overhead_wasm_emscripten = np.nanmean(overhead_wasm_emscripten)
    avg_overhead_wasm_obf_emscripten_bynarien = np.nanmean(overhead_wasm_obf_emscripten_bynarien)
    avg_overhead_native_obf = np.nanmean(overhead_native_obf)
    avg_overhead_wasm_clang = np.nanmean(overhead_wasm_clang)
    avg_overhead_wasm_obf_clang = np.nanmean(overhead_wasm_obf_clang)
    avg_overhead_wasm_obf_emscripten = np.nanmean(overhead_wasm_obf_emscripten)
    
    
    data = [
        native_times, wasm_emscripten_times, wasm_obf_emscripten_bynarien_times, native_obf_times,
        wasm_clang_times, wasm_obf_clang_times, wasm_obf_emscripten_times
    ]
    labels = [
        'Binary', 'WASM Emscripten', 'WASM Obfuscated Emscripten + Bynarien', 'Native Obfuscated',
        'WASM Clang', 'WASM Obfuscated Clang + wasm-mutate', 'WASM Obfuscated Emscripten + wasm-mutate'
    ]
    
    fig, ax = plt.subplots(figsize=(14, 7))
    
    ax.boxplot(data, vert=False, patch_artist=True, labels=labels,
               boxprops=dict(facecolor='lightgray', color='gray'),
               flierprops=dict(marker='o', color='red', markersize=5),
               medianprops=dict(color='black'))
    
    ax.set_xlabel('Seconds')
    

    #ax.set_title(f'Runtime Distribution')
    ax.set_title('Runtime Distribution', fontsize=12)
    ax.text(0.5, -0.2,  # Metti il testo sotto il grafico
        f'Overhead WASM Emscripten: {avg_overhead_wasm_emscripten:.2f}% \n '
        f'Overhead WASM Obfuscated Emscripten + Bynarien: {avg_overhead_wasm_obf_emscripten_bynarien:.2f}% \n '
        f'Overhead Native Obfuscated: {avg_overhead_native_obf:.2f}% \n '
        f'Overhead WASM Clang: {avg_overhead_wasm_clang:.2f}% \n '
        f'Overhead WASM Obfuscated Clang + wasm-mutate: {avg_overhead_wasm_obf_clang:.2f}% \n '
        f'Overhead WASM Obfuscated Emscripten + wasm-mutate: {avg_overhead_wasm_obf_emscripten:.2f}%',
        fontsize=8, ha='center', va='top', transform=ax.transAxes)


    plt.tight_layout()
    plt.savefig(boxplot_file)
    plt.close()

def load_csv1(csv_file):
    df = pd.read_csv(csv_file)
    results = {}
    for index, row in df.iterrows():
        results[row['name']] = [row['native'], row['wasm'], row['wasm_obfuscated'], row['native_obfuscated']]
    return results

def load_csv2(csv_file):
    df = pd.read_csv(csv_file)
    results = {}
    for index, row in df.iterrows():
        results[row['name']] = [row['wasm_clang'], row['wasm_obf_clang'], row['wasm_obf_emscripten']]
    return results


runtime_bynarien = load_csv1('runtime_bynarien.csv')
runtime_wasmmutate = load_csv2('runtime_wasm-mutate.csv')
bar_chart_file = 'bar_chart_runtime_distribution.pdf'  
boxplot_file = 'boxplot_runtime_distribution.pdf' 
boxplot2_file = 'boxplot2_runtime_distribution.pdf'

plot_bar_chart(runtime_bynarien, bar_chart_file)
plot_boxplot_chart(runtime_bynarien, boxplot_file)

plot2_boxplot_chart(runtime_bynarien, runtime_wasmmutate, boxplot2_file)


