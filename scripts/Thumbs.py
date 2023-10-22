"""
Script that will delete all thumbnails from the data
"""

import os
import argparse
from pathlib import Path
import sys

# argparse stuff
parser = argparse.ArgumentParser(
	prog=sys.argv[0],
	description="Deletes thumbnails by checking if the filename consists of _TN"
)
parser.add_argument("src", help="Path to the dataset")
parser.add_argument("--delete", action="store_true", help="Deletes only if this flag is added")
args = parser.parse_args()


# default data
TN = "_TN"
DATA_DIR = Path(args.src).resolve().as_posix()


if __name__ == "__main__":
	count = 0
	if args.delete:
		print("Deleting files...")
	else:
		print("Scanning for thumbnails...")
		
	for root, sub, files in os.walk(DATA_DIR):
		for file in files:
						
			if TN in file:
				if args.delete:
					os.remove(os.path.join(root, file))
				else:
					print(file)
				count += 1



	print()
	if args.delete:
		print("Total thumbnails deleted:", end=" ")
	else:
		print("Total thumbnails found:", end=" ")
	print(count, end="\n\n")