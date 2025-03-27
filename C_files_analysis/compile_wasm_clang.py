import os
import subprocess
import shutil


def check_wasi_sdk():
    wasi_sdk_path = "/opt/wasi-sdk/bin/clang"
    if not shutil.which(wasi_sdk_path):
        print("Error: wasi-sdk is not installed.")
        return False
    return True


def check_clang():
    if not shutil.which("clang"):
        print("Error: Clang is not installed.")
        return False
    return True

def compile_c_to_wasm(directory, output_directory):

    #check wasi-sdk and clang
    if not (check_wasi_sdk() and check_clang()):
        print("Aborted due to missing dependencies.")
        return
        
    c_files = [f for f in os.listdir(directory) if f.endswith(".c")]
    
    if not c_files:
        print("No C file in the directory")
        return
        
        
    #create output directory if it doesn't exist    
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
        
        
    for c_file in c_files:
        c_path = os.path.join(directory, c_file)
        wasm_output = os.path.join(output_directory, os.path.splitext(c_file)[0] + ".wasm")
        
        command = f'/opt/wasi-sdk/bin/clang --target=wasm32-wasi -o "{wasm_output}" "{c_path}"'
        
        print(f"Compile {c_file}...")
        subprocess.run(command, shell=True, executable='/bin/bash',  cwd=directory)
    
    print("Completed")


#this path
script_directory = os.getcwd()

#input path
source_directory = os.path.join(script_directory, "C")

#output path
output_directory = os.path.join(script_directory, "wasm_clang")

#compile C to wasm
compile_c_to_wasm(source_directory, output_directory)

