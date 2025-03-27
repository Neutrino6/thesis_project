import os
import subprocess

def obfuscate_wasm_files(directory, output_directory):
    
    wasm_files = [f for f in os.listdir(directory) if f.endswith(".wasm")]
    
    if not wasm_files:
        print("No wasm file in the directory")
        return
        
    #create output directory if it doesn't exist    
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
        
        
    for wasm_file in wasm_files:
        obfuscated_output = os.path.splitext(wasm_file)[0] + "_obfuscated.wasm"
        
        
        #output path
        output_file_path = os.path.join(output_directory, obfuscated_output)
        
        
        #obfuscation with bynarien
        obfuscate_command = f'wasm-opt -Oz "{wasm_file}" -o "{output_file_path}"'
        
        print(f"Obfuscate {wasm_file}...")
        subprocess.run(obfuscate_command, shell=True, executable='/bin/bash', cwd=directory)
    
    print("Completed")


#this path
script_directory = os.getcwd()


source_directory = os.path.join(script_directory, "wasm_emscripten")
output_directory = os.path.join(script_directory, "wasm_obfuscated_bynarien")

#obfuscate
obfuscate_wasm_files(source_directory, output_directory)
