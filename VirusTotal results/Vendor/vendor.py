import os
import json
import matplotlib.pyplot as plt
from collections import defaultdict

# Cartelle da analizzare
folders = [
    "vt_wasm",
    "vt_wasm_obf",
    "vt_wasm_obf_js_obf",
    "vt_wasm_js_obf"
]

def process_folder(folder_path):
    vendor_counts = defaultdict(int)
    
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            full_path = os.path.join(folder_path, filename)
            with open(full_path, "r") as f:
                try:
                    data = json.load(f)
                    results = data["data"]["attributes"]["results"]
                    for vendor, info in results.items():
                        category = info.get("category")
                        if category and category != "type-unsupported":
                            if category == "malicious":
                                vendor_counts[vendor] += 1
                except Exception as e:
                    print(f"Errore nel file {filename}: {e}")
    return vendor_counts

def plot_vendor_counts(vendor_counts, title):
    if not vendor_counts:
        print(f"Nessun dato da plottare per {title}")
        return
    
    vendors = list(vendor_counts.keys())
    counts = [vendor_counts[v] for v in vendors]
    
    plt.figure(figsize=(12, 6))
    plt.bar(vendors, counts, color='darkred')
    plt.xlabel('Antivirus')
    plt.ylabel('Number of files marked as malicious')
    plt.title(f'Files marked as "malicious" by vendor - {title}')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()

# Esegui per ciascuna cartella
for folder in folders:
    counts = process_folder(folder)
    plot_vendor_counts(counts, folder)
