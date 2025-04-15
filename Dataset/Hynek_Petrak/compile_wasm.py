import os
import re
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed

# dependency
libraries = {
    "angular": [r'\bangular\b', r'import .*angular', r'require\(.*angular.*\)'],
    "bootstrap": [r'bootstrap', r'import .*bootstrap', r'require\(.*bootstrap.*\)'],
    "jquery": [r'\$', r'jQuery', r'import .*jquery', r'require\(.*jquery.*\)'],
    "electron": [r'\belectron\b', r'import .*electron', r'require\(.*electron.*\)'],
    "react": [r'\breact\b', r'import .*react', r'require\(.*react.*\)'],
}

# check dependency
def has_dependency(js_path):
    try:
        with open(js_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            for patterns in libraries.values():
                for pattern in patterns:
                    if re.search(pattern, content):
                        return True
    except Exception as e:
        print(f"Errore leggendo {js_path}: {e}")
    return False

# check if .wasm already exists
def wasm_exists(js_filename, wasm_output_base):
    return any(os.path.exists(path) for path in [
        os.path.join(wasm_output_base, js_filename + ".wasm"),
        os.path.join(wasm_output_base, "With_dependency", js_filename + ".wasm")
    ])

# task eseguito in parallelo
def process_single_file(js_path, wasm_output_base):
    filename = os.path.basename(js_path)
    filename_wo_ext = os.path.splitext(filename)[0]

    # controlla se già esiste
    if wasm_exists(filename_wo_ext, wasm_output_base):
        return f"{filename} già compilato, salto."

    # controlla dipendenze
    has_dep = has_dependency(js_path)
    wasm_subdir = "With_dependency" if has_dep else ""
    wasm_output_dir = os.path.join(wasm_output_base, wasm_subdir)
    os.makedirs(wasm_output_dir, exist_ok=True)

    # compila
    wasm_output_path = os.path.join(wasm_output_dir, filename_wo_ext + ".wasm")
    compile_cmd = f'./javy build "{js_path}" -o "{wasm_output_path}"'
    result = subprocess.run(compile_cmd, shell=True, executable='/bin/bash')

    if result.returncode == 0:
        return f"{filename} compilato in {wasm_output_path}"
    else:
        return f"Errore compilando {filename}"

# funzione principale
def process_js_files(base_directory, wasm_output_base, max_workers=4):
    all_js_files = []
    for root, _, files in os.walk(base_directory):
        for file in files:
            if file.endswith(".js"):
                all_js_files.append(os.path.join(root, file))

    print(f"Trovati {len(all_js_files)} file JavaScript. Inizio compilazione parallela...")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(process_single_file, path, wasm_output_base) for path in all_js_files]
        for future in as_completed(futures):
            print(future.result())

    print("Operazione completata.")

# directory
script_directory = os.getcwd()
base_input_directory = os.path.join(script_directory, "Javascript")
wasm_output_directory = os.path.join(script_directory, "Wasm_Petrak")

# avvio
process_js_files(base_input_directory, wasm_output_directory)

