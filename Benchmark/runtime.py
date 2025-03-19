import os
import subprocess
import re
import matplotlib.pyplot as plt
import numpy as np


#"time" command in terminal and takes the average of the 10 values obtained for each type of file.
#takes the value called "real"

def get_execution_time(command):
    times = []
    for _ in range(10):
        result = subprocess.run(f"time {command}", shell=True, text=True, capture_output=True, executable='/bin/bash')
        match = re.search(r"real\s+(\d+m)?(\d+\.\d+)s", result.stderr)
        if match:
            minutes = match.group(1)
            seconds = match.group(2)
            if minutes:
                minutes = int(minutes[:-1])  #removes "m" 
                times.append(minutes * 60 + float(seconds))
            else:
                times.append(float(seconds))
                
    #average with 4 decimals
    avg_time = sum(times) / len(times) if times else None
    return round(avg_time, 4) if avg_time is not None else None

def benchmark_files(directory):
    results = {}
    
    native_dir = os.path.join(directory, "native")
    wasm_dir = os.path.join(directory, "wasm")
    wasm_obf_dir = os.path.join(directory, "wasm_obfuscated")
    native_obf_dir = os.path.join(directory, "native_obfuscated")
    
    
    #native times
    native_files = [f for f in os.listdir(native_dir) if f.endswith("_native")]
    for native in native_files:
        name = native.replace("_native", "")  #remove _native
        avg_native_time = get_execution_time(f"./{os.path.join(native_dir, native)}")  #executes
        results[name] = [avg_native_time, None, None, None]
    
    #wasm times
    wasm_files = [f for f in os.listdir(wasm_dir) if f.endswith(".wasm") and not f.endswith("_obfuscated.wasm")]
    for wasm in wasm_files:
        name = wasm.replace(".wasm", "")  
        avg_wasm_time = get_execution_time(f"wasmtime {os.path.join(wasm_dir, wasm)}")  #time wasmtime name.wasm
        if name in results:
            results[name][1] = avg_wasm_time
        else:
            results[name] = [None, avg_wasm_time, None, None]
    
    #wasm_obfuscated times
    obfuscated_files = [f for f in os.listdir(wasm_obf_dir) if f.endswith("_obfuscated.wasm")]
    for obf in obfuscated_files:
        name = obf.replace("_obfuscated.wasm", "")  
        avg_obf_time = get_execution_time(f"wasmtime {os.path.join(wasm_obf_dir, obf)}")  
        if name in results:
            results[name][2] = avg_obf_time
        else:
            results[name] = [None, None, avg_obf_time, None]
    
    #native_obfuscated times
    obfuscated_native_files = [f for f in os.listdir(native_obf_dir) if f.endswith("_native_obfuscated")]
    for obf_native in obfuscated_native_files:
        name = obf_native.replace("_native_obfuscated", "")  
        avg_obf_native_time = get_execution_time(f"./{os.path.join(native_obf_dir, obf_native)}")  
        if name in results:
            results[name][3] = avg_obf_native_time
        else:
            results[name] = [None, None, None, avg_obf_native_time]
    
    return results

#overhead
def calculate_overhead(results):
    overheads_wasm = []
    overheads_wasm_obf = []
    overheads_native_obf = []
    
    for values in results.values():
        native_time, wasm_time, wasm_obf_time, native_obf_time = values
        
        if native_time and wasm_time:
            overheads_wasm.append(((wasm_time - native_time) / native_time) * 100)
        
        if native_time and wasm_obf_time:
            overheads_wasm_obf.append(((wasm_obf_time - native_time) / native_time) * 100)
        
        if native_time and native_obf_time:
            overheads_native_obf.append(((native_obf_time - native_time) / native_time) * 100)
    
    avg_overhead_wasm = round(sum(overheads_wasm) / len(overheads_wasm), 2) if overheads_wasm else 0
    avg_overhead_wasm_obf = round(sum(overheads_wasm_obf) / len(overheads_wasm_obf), 2) if overheads_wasm_obf else 0
    avg_overhead_native_obf = round(sum(overheads_native_obf) / len(overheads_native_obf), 2) if overheads_native_obf else 0
    
    return avg_overhead_wasm, avg_overhead_wasm_obf, avg_overhead_native_obf

#histogram saved in a file
def plot_bar_chart(results, avg_overhead_wasm, avg_overhead_wasm_obf, avg_overhead_native_obf, bar_chart_file):
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
    ax.set_title(f'Runtime (Overhead WASM: {avg_overhead_wasm}% - Overhead WASM Obfuscated: {avg_overhead_wasm_obf}% - Overhead Native Obfuscated: {avg_overhead_native_obf}%)')
    ax.set_xticks(x + width)
    ax.set_xticklabels(names, rotation=45, ha="right")
    ax.legend()

    plt.tight_layout()
    plt.savefig(bar_chart_file)  
    plt.close()

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
    
    
    data = [native_times, wasm_times, wasm_obf_times, native_obf_times]
    labels = ['Binary', 'WASM', 'WASM Obfuscated', 'Native Obfuscated']

    fig, ax = plt.subplots(figsize=(12, 6))

   
    ax.boxplot(data, vert=False, patch_artist=True, labels=labels, 
               boxprops=dict(facecolor='lightgray', color='gray'),
               flierprops=dict(marker='o', color='red', markersize=5),
               medianprops=dict(color='black'))

    
    ax.set_xlabel('Seconds')
    ax.set_title('Runtime Distribution')

    plt.tight_layout()
    plt.savefig(boxplot_file) 
    plt.close()


directory_path = "/home/ubuntu/Desktop/Benchmark"
benchmark_results = benchmark_files(directory_path)

avg_overhead_wasm, avg_overhead_wasm_obf, avg_overhead_native_obf = calculate_overhead(benchmark_results)

print(f"Overhead medio WASM: {avg_overhead_wasm}%")
print(f"Overhead medio WASM Obfuscated: {avg_overhead_wasm_obf}%")
print(f"Overhead medio Native Obfuscated: {avg_overhead_native_obf}%")


bar_chart_file = "bar_chart.png"
boxplot_file = "boxplot_chart.png"


plot_bar_chart(benchmark_results, avg_overhead_wasm, avg_overhead_wasm_obf, avg_overhead_native_obf, bar_chart_file)
plot_boxplot_chart(benchmark_results, boxplot_file)



