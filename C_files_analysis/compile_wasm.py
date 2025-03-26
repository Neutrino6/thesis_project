import os
import subprocess
import shutil

def find_emscripten():
    
    #check for environment variable
    emsdk_path = os.environ.get("EMSDK")
    if emsdk_path and os.path.exists(emsdk_path):
        return os.path.join(emsdk_path, "emsdk_env.sh")
    
    #find emcc 
    emcc_path = shutil.which("emcc")
    if emcc_path:
        #find directory
        emsdk_dir = os.path.dirname(os.path.dirname(emcc_path))
        emsdk_env = os.path.join(emsdk_dir, "emsdk_env.sh")
        if os.path.exists(emsdk_env):
            return emsdk_env

    return None  #not found

def compile_c_to_wasm(directory, output_directory):
    
    #find path for emscripten
    emscripten_path = find_emscripten()

    if not emscripten_path:
        print("Error: emsdk_env.sh not found.")
        print("Install Emscripten.")
        return

    emsdk_command = f'source "{emscripten_path}"'
    
    c_files = [f for f in os.listdir(directory) if f.endswith(".c")]
    
    if not c_files:
        print("No C file in the directory")
        return
        
        
    #create output directory if it doesn't exist    
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
        
        
    for c_file in c_files:
        c_path = os.path.join(directory, c_file)
        wasm_output = os.path.splitext(c_file)[0] + ".wasm"
        compile_command = f'emcc "{c_path}" -o "{os.path.join(directory, wasm_output)}"'
        
        full_command = f'{emsdk_command} && {compile_command}'
        
        print(f"Compile {c_file}...")
        subprocess.run(full_command, shell=True, executable='/bin/bash',  cwd=directory)
    
    print("Completed")


#this path
script_directory = os.getcwd()

#input path
source_directory = os.path.join(script_directory, "C_files_analysis", "C")

#output path
output_directory = os.path.join(script_directory, "C_files_analysis", "wasm")

#compile C to wasm
compile_c_to_wasm(source_directory, output_directory)

