import os
import csv

def write_csv():

    this_directory = os.path.dirname(os.path.abspath(__file__))

    #schema
    directories_info = {
        "Malware_Bazaar/Wasm": {
            "source_file": "javascript",
            "malware_type": "unknown",
            "paper": "no",
            "origin": "Malware Bazaar"
        },
        "MinerRay/Wasm": {
            "source_file": "unknown",
            "malware_type": "cryptojacking",
            "paper": "yes",
            "origin": "MinerRay: Semantics-Aware Analysis for Ever-Evolving Cryptojacking Detection"
        },
        "MineSweeper/miner_samples": {
            "source_file": "unknown",
            "malware_type": "cryptojacking",
            "paper": "yes",
            "origin": "MineSweeper: An In-depth Look into Drive-by Cryptocurrency Mining and Its Defense"
        },
        "Hynek_Petrak/Wasm_Petrak": {
            "source_file": "javascript",
            "malware_type": "unknown",
            "paper": "no",
            "origin": "Hynek Petrak"
        }, 
        "geeksonsecurity/Wasm": {
            "source_file": "javascript",
            "malware_type": "unknown",
            "paper": "no",
            "origin": "GeeksOnSecurity"
        }, 
        "MINOS/malign": {
            "source_file": "unknown",
            "malware_type": "cryptojacking",
            "paper": "yes",
            "origin": "MINOS: A Lightweight Real-Time Cryptojacking Detection System"
        }
    }

    
    rows = []

    #take data
    for rel_path, metadata in directories_info.items():
        abs_path = os.path.join(this_directory, rel_path)
        if not os.path.isdir(abs_path):
            print(f"Directory not found")
            continue

        for file in os.listdir(abs_path):
            if file.endswith(".wasm"):
                row = {
                    "wasm_file_name": file,
                    "source_file": metadata["source_file"],
                    "malware_type": metadata["malware_type"],
                    "paper": metadata["paper"],
                    "origin": metadata["origin"]
                }
                rows.append(row)

    #write into CSV
    csv_file_path = os.path.join(this_directory, "dataset_info.csv")
    with open(csv_file_path, mode='w', newline='') as csvfile:
        fieldnames = ["wasm_file_name", "source_file", "malware_type", "paper", "origin"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in rows:
            writer.writerow(row)

    print(f"Done")


if __name__ == "__main__":
    write_csv()

