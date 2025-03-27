import os
import subprocess
import re
import matplotlib.pyplot as plt
import numpy as np
import csv

#check if "time" and "wasmtime" are available commands
def check_command(command):
    try:
        subprocess.run(["which", command], capture_output=True, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

#time command
if not check_command("time"):
    print("'time' is not available. Install it.")
    exit(1)

#wasmtime command
if not check_command("wasmtime"):
    print("'wasmtime' is not available. Install wasm-tools.")
    exit(1)


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
    
    #verify existence of directories
    if not os.path.exists(native_dir) or not os.path.exists(wasm_dir) or not os.path.exists(wasm_obf_dir) or not os.path.exists(native_obf_dir):
        raise FileNotFoundError("Some subdirectories not found")
    
    
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



#path of this directory 
this_directory = os.path.dirname(os.path.abspath(__file__))

benchmark_results = benchmark_files(this_directory)

avg_overhead_wasm, avg_overhead_wasm_obf, avg_overhead_native_obf = calculate_overhead(benchmark_results)


def save_to_csv(results, output_file):
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["name", "native", "wasm", "wasm_obfuscated", "native_obfuscated"])
        
        for name, values in results.items():
            writer.writerow([name] + values)





output_dir = os.path.join(this_directory, "runtime_distribution")
#verify "runtime_distribution" exists. If not, it creates it
os.makedirs(output_dir, exist_ok=True)
#save there the csv file
output_csv = os.path.join(output_dir, "runtime_bynarien.csv")
save_to_csv(benchmark_results, output_csv)

#overhead
print(f"Overhead WASM: {avg_overhead_wasm}%")
print(f"Overhead WASM Obfuscated: {avg_overhead_wasm_obf}%")
print(f"Overhead Native Obfuscated: {avg_overhead_native_obf}%")




