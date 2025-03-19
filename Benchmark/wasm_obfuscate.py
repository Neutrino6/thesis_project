import os
import subprocess

def obfuscate_wasm_files(directory):
    
    wasm_files = [f for f in os.listdir(directory) if f.endswith(".wasm")]
    
    if not wasm_files:
        print("No wasm file in the directory")
        return
    
    for wasm_file in wasm_files:
        obfuscated_output = os.path.splitext(wasm_file)[0] + "_obfuscated.wasm"
        
        #obfuscation with bynarien
        obfuscate_command = f'wasm-opt -Oz "{wasm_file}" -o "{obfuscated_output}"'
        
        print(f"Obfuscate {wasm_file}...")
        subprocess.run(obfuscate_command, shell=True, executable='/bin/bash')
    
    print("Completed")


directory_path = "/home/ubuntu/Desktop/Benchmark/wasm"  
obfuscate_wasm_files(directory_path)
