#Task 1
import pandas as pd
import json

def Delta_load_and_integrate():

    
    # A. LOAD FILES (
 
    zoo = pd.read_csv("zoo.csv", encoding="utf-8", errors="replace")
    class_df = pd.read_csv("class.csv")

    try:
        with open("auxiliary_metadata.json", "r", encoding="utf-8") as f:
            metadata = json.load(f)
    except:
        metadata = []

    # turn JSON list into DataFrame
    meta = pd.DataFrame(metadata)

  
    # B. NORMALIZE ANIMAL NAMES
   
    zoo["animal_name"] = zoo["animal_name"].str.lower()
    class_df["animal_name"] = class_df["animal_name"].str.lower()
    meta["animal_name"] = meta["animal_name"].str.lower()

   
    # C. FIX JSON DATA
    

    # rename conservation fields
    if "conservation" in meta.columns:
        meta.rename(columns={"conservation": "conservation_status"}, inplace=True)
    if "status" in meta.columns:
        meta.rename(columns={"status": "conservation_status"}, inplace=True)

    # rename habitat fields
    if "habitats" in meta.columns:
        meta.rename(columns={"habitats": "habitat_type"}, inplace=True)
    if "habitat" in meta.columns:
        meta.rename(columns={"habitat": "habitat_type"}, inplace=True)

    # diet type → diet
    if "diet_type" in meta.columns:
        meta.rename(columns={"diet_type": "diet"}, inplace=True)

    # fix diet typos
    if "diet" in meta.columns:
        meta["diet"] = meta["diet"].str.lower().str.strip()
        meta["diet"] = meta["diet"].replace({
            "omnivor": "omnivore",
            "insectivore": "insectivore",
            "filter_feeder": "filter_feeder"
        })

    # standardize habitat values
    if "habitat_type" in meta.columns:
        meta["habitat_type"] = meta["habitat_type"].str.lower().str.strip()
        meta["habitat_type"] = meta["habitat_type"].replace({
            "fresh water": "freshwater",
            "fresh water ": "freshwater",
            "freshwater ": "freshwater"
        })

    # D. MERGE ALL DATASETS
  
    merged = zoo.merge(class_df, on="animal_name", how="left")
    merged = merged.merge(meta, on="animal_name", how="left")

 
    # E. HANDLE MISSING VALUES
    # categorical → "unknown"
    # numerical → median
    
    for col in merged.columns:
        if merged[col].dtype == "object":
            merged[col] = merged[col].fillna("unknown")
        else:
            merged[col] = merged[col].fillna(merged[col].median())

    # F. FEATURE ENGINEERING
  

    # ecosystem_type (terrestrial=0, freshwater=1, marine=2, mixed=3)
    def eco_map(x):
        x = str(x)
        if "fresh" in x:
            return 1
        if "marine" in x:
            return 2
        if "coastal" in x:
            return 3
        return 0

    merged["ecosystem_type"] = merged["habitat_type"].apply(eco_map)

    # predator_score (carnivore=3, omnivore=2, else=1)
    def pred_map(x):
        x = str(x)
        if x == "carnivore":
            return 3
        if x == "omnivore":
            return 2
        return 1

    merged["predator_score"] = merged["diet"].apply(pred_map)

    engineered_feature_names = ["ecosystem_type", "predator_score"]

    # G. REQUIRED OUTPUT
  
    print(f"Dataset shape: {merged.shape}")
    print(f"Missing values: {merged.isnull().sum().sum()}")
    print(f"Duplicate rows: {merged.duplicated().sum()}")

    print("\nFirst 3 rows:")
    print(merged.head(3))

    print("\nEngineered features:", engineered_feature_names)

    return merged




