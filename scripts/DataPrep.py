"""
Script to categorize the data according to the ROP Stages, by looking at the 
"""

import os
from pathlib import Path
import argparse
import sys
import pandas as pd
from datetime import datetime
import shutil

# argparse stuff
parser = argparse.ArgumentParser(
    prog=sys.argv[0],
    description="Prepare data directory structure according to csv"
)
parser.add_argument("src", help="Path to dataset source")
parser.add_argument("csv", help="Path to the Trimmed CSV containing the stages")
parser.add_argument("dest", help="Destination directory in which the data will be created")
parser.add_argument("--move",  action="store_true", help="If flag is added then the images are moved instead of copying")
parser.add_argument("--decision", action="store_true", help="Add this falg to setup prep data according to decision column and not LS")

args = parser.parse_args()


# resolving paths
SOURCE = Path(args.src).resolve().as_posix()
DATA_CSV = Path(args.csv).resolve().as_posix()

# output file path
OUTPUT = Path(
    os.path.join(args.dest, "data")
).resolve().as_posix()

# string patterns for converting date time into ideal format
DATE_PARSE= r"%Y%m%d%H%M%S"
DATE_TO_STR = r"%Y-%m-%d"


if __name__ == "__main__":
    print("Reading csv...")
    df = pd.read_csv(DATA_CSV)
    
    # creating folder
    print("Starting job...")
    try:
        os.mkdir(OUTPUT)
    except:
        pass

    if args.decision:
        for i in df["Decision"].unique().tolist():
            try:
                os.mkdir(os.path.join(OUTPUT, str(i)))
            except:
                pass

    else:
        for i in df["LS"].unique().tolist():
            try:
                os.mkdir(os.path.join(OUTPUT, i))
            except:
                pass


    # get a list of multiple common entries of patient id
    temp = df["MRD"].value_counts()
    multiple_visits = temp[temp > 1].index.tolist()
    del temp

    for patient_id in os.listdir(SOURCE):
        # current folder has multiple entries in csv 
        curr_id = os.path.join(SOURCE, patient_id)

        if patient_id in multiple_visits:
            
            for visit_date in os.listdir(curr_id):
                regularized_date = datetime.strptime(visit_date, DATE_PARSE).strftime(DATE_TO_STR) # parse date from folder name

                try:
                    if args.decision:
                        dest = df.loc[(df["MRD"] == patient_id) & (df["Date of visit"] == regularized_date), "Decision"].tolist()[0] # collect rop status
                    else:
                        dest = df.loc[(df["MRD"] == patient_id) & (df["Date of visit"] == regularized_date), "LS"].tolist()[0] # collect rop status
                except IndexError:
                    pass

                curr_date = os.path.join(curr_id, visit_date) # get path for directory acc to date
                
                for image in os.listdir(curr_date):
                    # iterate through images in the a given date under given patient id and add to matching destination
                    if args.move:
                        shutil.move(
                            os.path.join(curr_date, image),
                            os.path.join(OUTPUT, str(dest))
                        )
                    else:
                        shutil.copy(
                            os.path.join(curr_date, image),
                            os.path.join(OUTPUT, str(dest))
                        )

        else:
            # current folder has single entry in csv
            try:
                if args.decision:
                    dest = df.loc[df["MRD"] == patient_id, "Decision"].tolist()[0] # collected rop status                
                else:
                    dest = df.loc[df["MRD"] == patient_id, "LS"].tolist()[0] # collected rop status
            except IndexError:
                pass

            curr_date = os.path.join(
                curr_id,
                os.listdir(curr_id)[0]
            )

            for image in os.listdir(curr_date):
                if args.move:
                    shutil.move(
                        os.path.join(curr_date, image),
                        os.path.join(OUTPUT, str(dest))
                    )
                else:
                    shutil.copy(
                        os.path.join(curr_date, image),
                        os.path.join(OUTPUT, str(dest))
                    )

    print("Done")