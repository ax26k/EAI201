import json
from turtle import pd


def load_and_clean():
    
    zoo = pd.read_csv("zoo.csv", encoding="utf-8")
    class_df = pd.read_csv("class.csv")
    
    try:
        with open("auxiliary_metadata.json", "r", encoding="utf-8") as f:
            meta_list = json.load(f)
    except:
        meta_list = []
    meta = pd.DataFrame(meta_list)

    zoo["animal_name"] = zoo["animal_name"].str.lower()
    class_df["animal_name"] = class_df["animal_name"].str.lower()
    if not meta.empty:
        meta["animal_name"] = meta["animal_name"].astype(str).str.lower()

    rename_map = {
        "conservation": "conservation_status",
        "status": "conservation_status",
        "habitats": "habitat_type",
        "habitat": "habitat_type",
        "diet_type": "diet"
    }
    meta.rename(columns=rename_map, inplace=True)

    if "diet" in meta.columns:
        meta["diet"] = meta["diet"].astype(str).str.lower().str.strip()
        meta["diet"] = meta["diet"].replace({"omnivor": "omnivore"})
    if "habitat_type" in meta.columns:
        meta["habitat_type"] = meta["habitat_type"].astype(str).str.lower().str.strip()
        meta["habitat_type"] = meta["habitat_type"].replace({
            "fresh water": "freshwater",
            "fresh waters": "freshwater",
            "fresh water ": "freshwater"
        })

    merged = zoo.merge(class_df, on="animal_name", how="left")
    merged = merged.merge(meta, on="animal_name", how="left")

    for col in merged.columns:
        if merged[col].dtype == "object":
            merged[col] = merged[col].fillna("unknown")
        else:
            merged[col] = merged[col].fillna(merged[col].median())

    def eco_map(x):
        x = str(x).lower()
        if "fresh" in x: return 1
        if "marine" in x: return 2
        if "coastal" in x: return 3
        return 0
    merged["ecosystem_type"] = merged["habitat_type"].apply(eco_map)

    def pred_map(x):
        x = str(x).lower()
        if x == "carnivore": return 3
        if x == "omnivore": return 2
        return 1
    merged["predator_score"] = merged["diet"].apply(pred_map)

    return merged