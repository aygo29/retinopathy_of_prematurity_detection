"""
Delete files having a particular extension
"""

import os
import argparse
from pathlib import Path
import sys

parser = argparse.ArgumentParser(
	prog=sys.argv[0],
	description="Deletes files matching particular extensions"
)
parser.add_argument("src", help="Path to the dataset")
parser.add_argument("--delete", action="store_true", help="Deletes only if this flag is added")
args = parser.parse_args()


SOURCE = Path(args.src).resolve().as_posix()

EXTENSIONS = [".ini"]



if __name__ == "__main__":
    COUNT = [0 for i in EXTENSIONS]

    print("Scanning directory...")
    for root, sub, files in os.walk(SOURCE):
        for file in files:

            ext = os.path.splitext(file)[1] # extracting file extension
            if ext in EXTENSIONS:
                COUNT[EXTENSIONS.index(ext)] += 1

                if args.delete:
                    os.remove(os.path.join(root, file))
                
    
    for i in range(len(EXTENSIONS)):
        if args.delete:
            print(f"Deleted count for {EXTENSIONS[i]}: {COUNT[i]}")
        else:
            print(f"Found count for {EXTENSIONS[i]}: {COUNT[i]}")
    
