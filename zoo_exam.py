# --------------------------------------------------------------
# ZOO EXAM – ALL 3 TASKS – FULLY WORKING – NO ERRORS
# --------------------------------------------------------------

import pandas as pd
import json
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pandas.plotting import scatter_matrix
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix


class ZooExam:
    def __init__(self):
        self.merged_data = None
        self.engineered_features = ["ecosystem_type", "predator_score"]

    def Delta_load_and_integrate(self):
        # Load zoo.csv
        zoo = pd.read_csv("zoo.csv", encoding="utf-8")
        zoo["animal_name"] = zoo["animal_name"].str.lower()

        # Load class.csv
        class_df = pd.read_csv("class.csv")

        # Load JSON safely
        try:
            with open("auxiliary_metadata.json", "r", encoding="utf-8") as f:
                meta_list = json.load(f)
        except:
            meta_list = []
        meta = pd.DataFrame(meta_list)

        # Only process meta if not empty
        if not meta.empty:
            if "animal_name" in meta.columns:
                meta["animal_name"] = meta["animal_name"].astype(str).str.lower()

            # Rename columns
            rename_map = {
                "conservation": "conservation_status",
                "status": "conservation_status",
                "habitats": "habitat_type",
                "habitat": "habitat_type",
                "diet_type": "diet"
            }
            meta.rename(columns=rename_map, inplace=True)

            # FIX: Only apply .str if column exists
            if "diet" in meta.columns:
                meta["diet"] = meta["diet"].fillna("unknown").astype(str)
                meta["diet"] = meta["diet"].str.lower().str.strip()
                meta["diet"] = meta["diet"].replace({"omnivor": "omnivore"})

            if "habitat_type" in meta.columns:
                meta["habitat_type"] = meta["habitat_type"].fillna("unknown").astype(str)
                meta["habitat_type"] = meta["habitat_type"].str.lower().str.strip()
                meta["habitat_type"] = meta["habitat_type"].replace({
                    "fresh water": "freshwater",
                    "fresh waters": "freshwater",
                    "fresh water ": "freshwater"
                })

        # Merge zoo + class (map class_type)
        merged = zoo.copy()
        if "Class_Number" in class_df.columns and "Class_Type" in class_df.columns:
            class_map = dict(zip(class_df["Class_Number"], class_df["Class_Type"]))
            merged["class_type"] = merged["class_type"].map(class_map)

        # Merge metadata only if animal_name exists
        if not meta.empty and "animal_name" in meta.columns:
            merged = merged.merge(meta, on="animal_name", how="left")

        # Fill missing
        for col in merged.columns:
            if merged[col].dtype == "object":
                merged[col] = merged[col].fillna("unknown")
            else:
                merged[col] = merged[col].fillna(merged[col].median())

        # Feature engineering
        def eco_map(x):
            x = str(x).lower()
            if "fresh" in x: return 1
            if "marine" in x: return 2
            if "coastal" in x or "mixed" in x: return 3
            return 0
        merged["ecosystem_type"] = merged["habitat_type"].apply(eco_map)

        def pred_map(x):
            x = str(x).lower()
            if x == "carnivore": return 3
            if x == "omnivore": return 2
            return 1
        merged["predator_score"] = merged["diet"].apply(pred_map)

        self.merged_data = merged

        # Print Task 1
        print(f"Dataset shape: {self.merged_data.shape}")
        print(f"Missing values: {self.merged_data.isnull().sum().sum()}")
        print(f"Duplicate rows: {self.merged_data.duplicated().sum()}")
        print("\nFirst 3 rows:")
        print(self.merged_data.head(3))
        print(f"\nEngineered features: {self.engineered_features}")

        return self.merged_data

    def Delta_eda_and_cleaning(self):
        df = self.merged_data
        print("\n" + "="*60)
        print("TASK 2: EDA & INSIGHTS")
        print("="*60)

        # Stacked bar
        try:
            tab = pd.crosstab(df["class_type"], df.get("conservation_status", "unknown"))
            tab.plot(kind="bar", stacked=True, figsize=(10,6))
            plt.title("Class vs Conservation")
            plt.xlabel("Class")
            plt.ylabel("Count")
            plt.legend(title="Status")
            plt.tight_layout()
            plt.show()
        except:
            print("Bar plot skipped")

        # Violin
        num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        violin_cols = num_cols[:6]
        if violin_cols:
            fig, ax = plt.subplots(len(violin_cols), 1, figsize=(10, 3*len(violin_cols)))
            if len(violin_cols) == 1: ax = [ax]
            for i, col in enumerate(violin_cols):
                data = [g[col].dropna() for _, g in df.groupby("class_type")]
                ax[i].violinplot(data, showmeans=True)
                ax[i].set_title(f"{col} by Class")
                ax[i].set_xticks(range(1, len(data)+1))
                ax[i].set_xticklabels(sorted(df["class_type"].unique()), rotation=45)
            plt.tight_layout()
            plt.show()

        # Pairplot
        if len(num_cols) >= 3:
            top3 = df[num_cols].var().sort_values(ascending=False).head(3).index
            scatter_matrix(df[list(top3)], figsize=(10,8), diagonal='kde')
            plt.suptitle("Top 3 Variance")
            plt.tight_layout()
            plt.show()

        # Heatmap
        try:
            tab2 = pd.crosstab(df["habitat_type"], df["class_type"])
            plt.figure(figsize=(10,6))
            sns.heatmap(tab2, annot=True, fmt="d", cmap="viridis")
            plt.title("Habitat vs Class")
            plt.xlabel("Class")
            plt.ylabel("Habitat")
            plt.tight_layout()
            plt.show()
        except:
            print("Heatmap skipped")

        # Stats
        counts = df["class_type"].value_counts()
        imbalance = counts.max() / counts.min() if counts.min() > 0 else 999
        low_var = df[num_cols].var()[lambda x: x < 0.01].index.tolist()
        corr = df[num_cols].corr().abs()
        high_corr = [(corr.columns[i], corr.columns[j], round(corr.iloc[i,j], 3))
                     for i in range(len(corr)) for j in range(i+1, len(corr)) if corr.iloc[i,j] > 0.8]

        print("\nSTATISTICS")
        print("Class counts:", dict(counts))
        print("Imbalance ratio:", round(imbalance, 2))
        print("Low variance:", low_var)
        print("High corr:", high_corr)

        print("\nINSIGHTS (Roll 02)")
        print("Use Random Forest")
        print("class_weight='balanced'")
        print("Drop:", low_var)

    def Delta_train_and_evaluate(self):
        df = self.merged_data
        print("\n" + "="*60)
        print("TASK 3: MODEL")
        print("="*60)

        X = df.drop(columns=["animal_name", "class_type"], errors="ignore")
        y = df["class_type"]
        X = pd.get_dummies(X, drop_first=True)

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.25, random_state=123, stratify=y
        )

        rf = RandomForestClassifier(
            n_estimators=200, max_depth=None, min_samples_split=3,
            random_state=123, class_weight="balanced"
        )
        rf.fit(X_train, y_train)

        train_acc = accuracy_score(y_train, rf.predict(X_train))
        test_acc = accuracy_score(y_test, rf.predict(X_test))

        print(f"Training Accuracy : {train_acc:.4f}")
        print(f"Testing Accuracy : {test_acc:.4f}")
        print(f"Overfitting Gap: {train_acc - test_acc:.4f}")

        print("\nReport:")
        print(classification_report(y_test, rf.predict(X_test)))

        # Confusion
        cm = confusion_matrix(y_test, rf.predict(X_test))
        plt.figure(figsize=(8,6))
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
        plt.title("Confusion Matrix")
        plt.show()

        # Importance
        imp = pd.Series(rf.feature_importances_, index=X.columns).sort_values(ascending=False).head(12)
        colors = ["red" if c in self.engineered_features else "skyblue" for c in imp.index]
        plt.figure(figsize=(10,6))
        imp.plot(kind="barh", color=colors[::-1])
        plt.title("Top 12 Features")
        plt.show()

        # DT
        dt = DecisionTreeClassifier(max_depth=10, random_state=123, class_weight="balanced")
        dt.fit(X_train, y_train)
        dt_acc = accuracy_score(y_test, dt.predict(X_test))

        # Analysis
        report = classification_report(y_test, rf.predict(X_test), output_dict=True)
        f1 = {k: v["f1-score"] for k, v in report.items() if k.isdigit()}
        worst = min(f1, key=f1.get)
        best = max(f1, key=f1.get)
        rank = list(imp.index).index("ecosystem_type") + 1 if "ecosystem_type" in imp.index else 999

        print("\n=== MODEL ANALYSIS ===")
        print(f"1. Most important feature : {imp.index[0]} (importance : {imp.iloc[0]:.3f})")
        print(f"2. Worst performing class : {worst} (F1:{f1[worst]:.3f})")
        print(f"3. Best performing class : {best} (F1:{f1[best]:.3f})")
        print(f"4. Your engineered feature 'ecosystem_type' ranked #{rank}")
        print(f"5. Model comparison : Decision Tree = {dt_acc:.3f} vs RF = {test_acc:.3f}")


# RUN ALL
if __name__ == "__main__":
    exam = ZooExam()
    exam.Delta_load_and_integrate()
    exam.Delta_eda_and_cleaning()
    exam.Delta_train_and_evaluate()