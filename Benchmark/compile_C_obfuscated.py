import os
import subprocess

def compile_obfuscated_c_files(directory):
    
    c_files = [f for f in os.listdir(directory) if f.endswith("_tigress.c")]
    
    if not c_files:
        print("No file _tigress.c in the directory")
        return
    
    for c_file in c_files:
        #take the name
        c_file_name = os.path.basename(c_file)
        
        #rename
        output_file = c_file_name.replace("_tigress.c", "") + "_native_obfuscated"
        
        #create command
        gcc_command = f' gcc {c_file_name} -o {output_file}'
        
        #compile the file
        print(f"Compile {c_file_name} with gcc")
        subprocess.run(gcc_command, shell=True, executable='/bin/bash', cwd=directory)
    
    print("Completed")


directory_path = "/home/ubuntu/Desktop/Benchmark/C_obfuscated"  
compile_obfuscated_c_files(directory_path)

