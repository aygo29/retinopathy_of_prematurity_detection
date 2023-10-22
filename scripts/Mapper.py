"""
Script that encodes the directory names using SHA-256 and generates a .json for the files
"""

import os
from pathlib import Path
import json
import sys
import hashlib
import argparse

parser = argparse.ArgumentParser(
    prog=f"{Path(sys.argv[0]).name}",
    description="File for encoding and decoding the data"
)

group = parser.add_mutually_exclusive_group()
group.add_argument("-e", help="Encode the dataset", action="store_true")
group.add_argument("-d", help="Decode the dataset", action="store_true")

parser.add_argument("src", help="Path to the dataset")
parser.add_argument("keys", help="JSON file to decode the data")

args = parser.parse_args()

if __name__ == "__main__":
    if args.e is None and args.d is None:
        parser.error("Either -e or -d is required")

    elif args.e:
        print("Encoding...")
        source = Path(args.src).resolve().as_posix()
        dirs = os.listdir(source)
        mapping = {}

        for i in dirs:
            mapping[i] = hashlib.sha256(i.encode()).hexdigest()
            os.rename(
                source + f"/{i}",
                source + f"/{mapping[i]}"
            )
            print(i, " -> ", mapping[i])
        
        print(f"Writing keys to {args.keys}")
        with open(args.keys, "w") as f:
            f.write(json.dumps(mapping, indent=4))
        print("Done")
            

    elif args.d:
        print("Decoding...")
        source = Path(args.src).resolve().as_posix()
        with open(args.keys, "r") as f:
            mapping = json.load(f)
        
        for i in mapping:
            try:
                os.rename(
                    source + f"/{mapping[i]}",
                    source + f"/{i}"
                )
                print(mapping[i], " -> ", i)
            except Exception as e:
                print(e)

        print("Done")
            

    # source = Path("Data").resolve().as_posix()
    # if len(sys.argv) == 2:
    #     if sys.argv[1] == "-e":
    #         dirs = os.listdir(source)
    #         mapping = {}

    #         for i in dirs:
    #             mapping[i] = hashlib.sha256(i.encode()).hexdigest()
    #             os.rename(
    #                 source + f"/{i}",
    #                 source + f"/{mapping[i]}"
    #             )

    #         with open("Mapping.json", "w") as f:
    #             f.write(json.dumps(mapping, indent=4))


    #     elif sys.argv[1] == "-d":
    #         with open("Mapping.json", "r") as f:
    #             mapping = json.load(f)

    #         for i in mapping:
    #             os.rename(
    #                 source + f"/{mapping[i]}",
    #                 source + f"/{i}"
    #             )
    #     else:
    #         print(f"python {sys.argv[0]} [-e | -d]\n\t-e -> Encode\n\t-d -> Decode")
    # else:
    #     print(f"python {sys.argv[0]} [-e | -d]\n\t-e -> Encode\n\t-d -> Decode")
