import os
import re
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed

#dependency
libraries = {
    "angular": [r'\bangular\b', r'import .*angular', r'require\(.*angular.*\)'],
    "bootstrap": [r'bootstrap', r'import .*bootstrap', r'require\(.*bootstrap.*\)'],
    "jquery": [r'\$', r'jQuery', r'import .*jquery', r'require\(.*jquery.*\)'],
    "electron": [r'\belectron\b', r'import .*electron', r'require\(.*electron.*\)'],
    "react": [r'\breact\b', r'import .*react', r'require\(.*react.*\)'],
}

#check dependency
def has_dependency(js_path):
    try:
        with open(js_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            for patterns in libraries.values():
                for pattern in patterns:
                    if re.search(pattern, content):
                        return True
    except Exception as e:
        print(f"Error {js_path}: {e}")
    return False


def process_single_file(js_path, wasm_output_base):
    filename = os.path.basename(js_path)
    filename_wo_ext = os.path.splitext(filename)[0]


    #check dependency
    has_dep = has_dependency(js_path)
    wasm_subdir = "With_dependency" if has_dep else ""
    wasm_output_dir = os.path.join(wasm_output_base, wasm_subdir)
    os.makedirs(wasm_output_dir, exist_ok=True)

    #compile in wasm
    wasm_output_path = os.path.join(wasm_output_dir, filename_wo_ext + ".wasm")
    compile_cmd = f'./javy build "{js_path}" -o "{wasm_output_path}"'
    result = subprocess.run(compile_cmd, shell=True, executable='/bin/bash')

    if result.returncode == 0:
        return f"{filename} compiled in {wasm_output_path}"
    else:
        return f"Error {filename}"

#js files
def process_js_files(base_directory, wasm_output_base, max_workers=4):
    all_js_files = []
    for root, _, files in os.walk(base_directory):
        for file in files:
            if file.endswith(".js"):
                all_js_files.append(os.path.join(root, file))

    print(f"There are {len(all_js_files)} JavaScript files. Let's start")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(process_single_file, path, wasm_output_base) for path in all_js_files]
        for future in as_completed(futures):
            print(future.result())

    print("Done")

#directory
script_directory = os.getcwd()
base_input_directory = os.path.join(script_directory, "Malware")
wasm_output_directory = os.path.join(script_directory, "Wasm")

#let's go
process_js_files(base_input_directory, wasm_output_directory)

