import os
import subprocess

def compile_c_to_wasm(directory):
    #initialize emscripten
    emsdk_command = 'source "/home/ubuntu/Desktop/emsdk/emsdk_env.sh"'
    
    
    c_files = [f for f in os.listdir(directory) if f.endswith(".c")]
    
    if not c_files:
        print("No C file in the directory")
        return
    
    for c_file in c_files:
        c_path = os.path.join(directory, c_file)
        wasm_output = os.path.splitext(c_file)[0] + ".wasm"
        compile_command = f'emcc "{c_path}" -o "{os.path.join(directory, wasm_output)}"'
        
        full_command = f'{emsdk_command} && {compile_command}'
        
        print(f"Compile {c_file}...")
        subprocess.run(full_command, shell=True, executable='/bin/bash')
    
    print("Completed")


directory_path = "/home/ubuntu/Desktop/Benchmark/C" 
compile_c_to_wasm(directory_path)

