import os
import subprocess

def obfuscate_c_files(directory):
    
    c_files = [f for f in os.listdir(directory) if f.endswith(".c")]
    
    if not c_files:
        print("No C file in the directory")
        return
    
    for c_file in c_files:
        c_path = os.path.join(directory, c_file)
        output_file = os.path.splitext(c_file)[0] + "_tigress.c"
        
        #tigress command
        tigress_command = f'./tigress --Environment=x86_64:Linux:Gcc:13.1 --Transform=Flatten --Functions=main --out={output_file} {c_file}'
        
        #execute
        print(f"Obfuscate {c_file}...")
        subprocess.run(tigress_command, shell=True, executable='/bin/bash', cwd=directory)
    
    print("Completed")

#tigress was working in its directory
directory_path = "/home/ubuntu/Desktop/tigress/3.3.3"  
obfuscate_c_files(directory_path)

