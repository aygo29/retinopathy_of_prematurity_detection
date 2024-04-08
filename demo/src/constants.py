APP_TITLE = "ROP Detection"

TEMPDIR = "./temp/"

MODELS = [
    "Stage Classification (All images)", 
    "Stage Classification (Temporal images)", 
    "Stage Classification (Manual Annotated)", 
    "Stage Classification (Manual + Temporal)", 
    "Decision Classification"
]

MODEL_H5 = [
    "./src/models/stage123_enh_all.h5",
    "./src/models/stage123_enh_temporal.h5",
    "./src/models/stage23_enh_manual.h5",
    "./src/models/stage23_enh_manual_temporal.h5",
    "./src/models/decision_enh_all.h5"
]

MODEL_LABELS = [
    ['stage 1', 'stage 2', 'stage 3'],    
    ['stage 1', 'stage 2', 'stage 3'],
    ['stage 2', 'stage 3'],
    ['stage 2', 'stage 3'],
    ["needs urgent treatment", "needs follow up", "discharged from rop"]
]