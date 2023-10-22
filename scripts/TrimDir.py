"""
Script that checks the data dir and the trimmed csv and searches of folders whose entries do not exist
in the csv, then deletes those entries
"""

import os
from pathlib import Path
import argparse
import sys
import pandas as pd
import shutil


parser = argparse.ArgumentParser(
    prog=sys.argv[0],
    description="Cleanup mistmatch folders from the data directory by comparing with trimmmed csv"
)

parser.add_argument("src", help="Path to dataset source")
parser.add_argument("csv", help="Path to trimmed CSV")
parser.add_argument("--delete", action="store_true", help="Will delete only if this flag is added, else it will just count and list")
args = parser.parse_args()

# resolving paths
SOURCE = Path(args.src).resolve().as_posix()
DATA_CSV = Path(args.csv).resolve().as_posix()


if __name__ == "__main__":
    print("Reading csv...")
    df = pd.read_csv(DATA_CSV)

    count = 0

    print("Starting scan...\n")
    for patient_id in os.listdir(SOURCE):
        if patient_id not in df["MRD"].values:
            if args.delete:
                # delete flag added
                shutil.rmtree(
                    os.path.join(SOURCE, patient_id)
                )
                count += 1
            else:
                # delete flag not added
                print(patient_id)
                count += 1

    if args.delete:
        print("Deleted folders:", end=' ')
    else:
        print("Mistmatch folders:", end='')
    print(f"{count}\n\n")

