import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix

def Delta_eda_and_cleaning(zoo_df, class_df, metadata_df):

    meta = metadata_df.copy()

    zoo_df["animal_name"] = zoo_df["animal_name"].str.lower()
    class_df["animal_name"] = class_df["animal_name"].str.lower()
    new_func(meta)

    if "conservation" in meta.columns:
        meta = meta.rename(columns={"conservation": "conservation_status"})
    if "status" in meta.columns:
        meta = meta.rename(columns={"status": "conservation_status"})
    if "habitats" in meta.columns:
        meta = meta.rename(columns={"habitats": "habitat_type"})
    if "habitat" in meta.columns:
        meta = meta.rename(columns={"habitat": "habitat_type"})
    if "diet_type" in meta.columns:
        meta = meta.rename(columns={"diet_type": "diet"})

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

    merged = zoo_df.merge(class_df, on="animal_name", how="left")
    merged = merged.merge(meta, on="animal_name", how="left")

    for col in merged.columns:
        if merged[col].dtype == object:
            merged[col] = merged[col].fillna("unknown")
        else:
            merged[col] = merged[col].fillna(merged[col].median())

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

    def pred_map(x):
        x = str(x)
        if x == "carnivore":
            return 3
        if x == "omnivore":
            return 2
        return 1

    merged["predator_score"] = merged["diet"].apply(pred_map)

    try:
        table = pd.crosstab(merged["class_type"], merged["conservation_status"])
        table.plot(kind="bar", stacked=True, figsize=(8, 5))
        plt.title("Class Distribution by Conservation Status")
        plt.show()
    except:
        print("Error in stacked bar chart")

    numeric_cols = merged.select_dtypes(include=[np.number]).columns.tolist()
    violin_cols = numeric_cols[:6]

    if violin_cols:
        fig, ax = plt.subplots(len(violin_cols), 1, figsize=(8, 3*len(violin_cols)))
        if len(violin_cols) == 1:
            ax = [ax]

        for i, col in enumerate(violin_cols):
            groups = [grp[col].values for _, grp in merged.groupby("class_type")]
            ax[i].violinplot(groups, showmeans=True)
            ax[i].set_title(f"{col} by class")

        plt.tight_layout()
        plt.show()

    if len(numeric_cols) >= 3:
        top3 = merged[numeric_cols].var().sort_values(ascending=False).index[:3]
        scatter_matrix(merged[top3], figsize=(8, 8))
        plt.show()
    else:
        top3 = []

    try:
        table2 = pd.crosstab(merged["habitat_type"], merged["class_type"])
        plt.imshow(table2, cmap="viridis", aspect="auto")
        plt.xticks(range(len(table2.columns)), table2.columns)
        plt.yticks(range(len(table2.index)), table2.index)
        plt.colorbar()
        plt.title("Heatmap: Habitat vs Class")
        plt.show()
    except:
        print("Heatmap failed")

    class_counts = merged["class_type"].value_counts()
    imbalance_ratio = class_counts.max() / class_counts.min()

    var_series = merged[numeric_cols].var()
    low_variance = var_series[var_series < 0.01].index.tolist()

    corr_matrix = merged[numeric_cols].corr().abs()
    high_corr_pairs = []

    for i in range(len(corr_matrix.columns)):
        for j in range(i+1, len(corr_matrix.columns)):
            if corr_matrix.iloc[i, j] > 0.8:
                high_corr_pairs.append((
                    corr_matrix.columns[i],
                    corr_matrix.columns[j],
                    corr_matrix.iloc[i, j]
                ))

    print("\nSTATISTICS")
    print("Class counts:", class_counts.to_dict())
    print("Imbalance ratio:", imbalance_ratio)
    print("Low variance features:", low_variance)
    print("Highly correlated pairs:", high_corr_pairs)

    print("\nINSIGHTS FOR ROLL NUMBER 02")
    print("Recommended model: Random Forest (handles imbalance + correlations)")
    print("Use class_weight='balanced' because imbalance ratio is:", imbalance_ratio)
    print("Drop low-variance features:", low_variance)
    print("Check correlated pairs:", high_corr_pairs)

    return merged

def new_func(meta):
    meta["animal_name"] = meta["animal_name"].astype(str).str.lower()
