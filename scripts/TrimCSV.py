"""
Script to build a csv with encoded names for DataPrep
"""

import os
from pathlib import Path
import argparse
import sys
import pandas as pd
import json
import re

# argparse stuff
parser = argparse.ArgumentParser(
    prog=sys.argv[0],
    description="Build a csv with encoded names and relevant columns"
)

parser.add_argument("xlsx", help="Path to original data spreasheet")
parser.add_argument("json", help="Path to the json holding the mappings")
parser.add_argument("csv", help="Path where the trimmed csv will be written")
args = parser.parse_args()

# resolving paths
DATA_CSV = Path(args.xlsx).resolve().as_posix()
MAP_JSON = Path(args.json).resolve().as_posix()
TRIM_CSV = Path(args.csv).resolve().as_posix()



def parse_patient_id_csv(id: str) -> str:
    PATTERN = '[^A-Za-z0-9]+'
    return re.sub(PATTERN, '', id)

def parse_patient_id_json(id: str) -> str:
    PATTERN = "[^A-Za-z0-9]+"
    return re.sub(PATTERN, '', id.split("_")[1])


if __name__ == "__main__":
    print("Reading files...")

    df = pd.read_excel(DATA_CSV)


    # preparing json
    with open(MAP_JSON, "r") as f:
        MAPPING = json.load(f)
            
    try:
        # deleting useless entry from MAPPING.json if it exists
        del MAPPING["ROP.db"]
    except:
        pass

    print("Preparing csv")

    # preparing csv
    df = df[["MRD", "Date of visit", "LS", "RS", "Dicision"]]
    df["MRD"] = df["MRD"].apply(lambda x: parse_patient_id_csv(str(x)))
    # creating a column with default value of false
    df["flag"] = False

    for i in MAPPING:
        # WARNING:
        #   The flag set to true must happen before the name is changed
        #   else it will not be able to locate it
        parsed_id = parse_patient_id_json(i)
        df.loc[df["MRD"] == parsed_id, "flag"] = True
        df.loc[df["MRD"] == parsed_id, "MRD"] = MAPPING[i]
        # Using the true flag to confirm existence of patient id in csv 
        # and directory

    print("Cleaning up...")
    # dropping values which lack true flag
    df = df[df["flag"] != False]
    # dropping flag column since it's no longer needed
    df = df.drop(columns=["flag"])
    df.dropna(inplace=True)

    df.rename(columns={
        "Dicision":"Decision"
    }, inplace=True)    # renaming columns

    print("Writing to disk...")
    df.to_csv(f"{TRIM_CSV}/TrimmedCSV.csv", index=False)
    print("Done")
    