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
    
    wasm_clang_dir = os.path.join(directory, "wasm_clang")
    wasm_obf_clang_dir = os.path.join(directory, "wasm_obfuscated_wasm-mutate_clang")
    wasm_obf_emscripten_dir = os.path.join(directory, "wasm_obfuscated_wasm-mutate_emscripten")
    
    
    #verify existence of directories
    if not os.path.exists(wasm_clang_dir) or not os.path.exists(wasm_obf_clang_dir) or not os.path.exists(wasm_obf_emscripten_dir):
        raise FileNotFoundError("Some subdirectories not found")
    
    
    #wasm_clang times
    wasm_clang_files = [f for f in os.listdir(wasm_clang_dir) if f.endswith(".wasm")]
    for wasm_clang in wasm_clang_files:
        name = wasm_clang.replace(".wasm", "")  #remove .wasm
        avg_wasm_clang_time = get_execution_time(f"./{os.path.join(wasm_clang_dir, wasm_clang)}")  #executes
        results[name] = [avg_wasm_clang_time, None, None]
    
    #wasm_obf_clang times
    wasm_obf_clang_files = [f for f in os.listdir(wasm_obf_clang_dir) if f.endswith("_obfuscated.wasm")]
    for wasm_obf_clang in wasm_obf_clang_files:
        name = wasm_obf_clang.replace("_obfuscated.wasm", "")  
        avg_wasm_obf_clang_time = get_execution_time(f"wasmtime {os.path.join(wasm_obf_clang_dir, wasm_obf_clang)}")  #time wasmtime name.wasm
        if name in results:
            results[name][1] = avg_wasm_obf_clang_time
        else:
            results[name] = [None, avg_wasm_obf_clang_time, None]
    
    #wasm_obf_emscripten times
    wasm_obf_emscripten_files = [f for f in os.listdir(wasm_obf_emscripten_dir) if f.endswith("_obfuscated.wasm")]
    for wasm_obf_emscripten in wasm_obf_emscripten_files:
        name = wasm_obf_emscripten.replace("_obfuscated.wasm", "")  
        avg_wasm_obf_emscripten_time = get_execution_time(f"wasmtime {os.path.join(wasm_obf_emscripten_dir, wasm_obf_emscripten)}")  
        if name in results:
            results[name][2] = avg_wasm_obf_emscripten_time
        else:
            results[name] = [None, None, avg_wasm_obf_emscripten_time]

    
    return results



#path of this directory 
this_directory = os.path.dirname(os.path.abspath(__file__))

benchmark_results = benchmark_files(this_directory)


def save_to_csv(results, output_file):
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["name", "wasm_clang", "wasm_obf_clang", "wasm_obf_emscripten"])
        
        for name, values in results.items():
            writer.writerow([name] + values)





output_dir = os.path.join(this_directory, "runtime_distribution")
#verify "runtime_distribution" exists. If not, it creates it
os.makedirs(output_dir, exist_ok=True)
#save there the csv file
output_csv = os.path.join(output_dir, "runtime2_results.csv")
save_to_csv(benchmark_results, output_csv)






