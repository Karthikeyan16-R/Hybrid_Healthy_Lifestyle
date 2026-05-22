import os
import pandas as pd

def load_food_dataset(path: str = None) -> pd.DataFrame:
    """
    Load and clean the Indian food nutrition dataset safely.
    Automatically detects missing columns and adjusts naming.
    """
    try:
        # ✅ Auto-detect default CSV path if not provided
        if path is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            path = os.path.join(base_dir, "../data/Indian_Food_Nutrition_Processed.csv")

        path = os.path.normpath(path)
        print(f"[INFO] Loading dataset from: {path}")

        if not os.path.exists(path):
            raise FileNotFoundError(f"Dataset file not found at path: {path}")

        # ✅ Load dataset
        df = pd.read_csv(path)
        print(f"[INFO] Raw dataset loaded — Rows: {len(df)}, Columns: {list(df.columns)}")

        # ✅ Normalize column names
        df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

        # ✅ Auto-rename common nutrition columns
        rename_map = {
            "calories_(kcal)": "calories",
            "energy_(kcal)": "calories",
            "energy": "calories",
            "protein_(g)": "protein",
            "fat_(g)": "fat",
            "carbohydrates_(g)": "carbohydrates",
            "carbs_(g)": "carbohydrates",
            "name_of_food": "name",
            "dish_name": "name",
            "food_name": "name"
        }

        # Rename columns if found in dataset
        for old, new in rename_map.items():
            if old in df.columns:
                df.rename(columns={old: new}, inplace=True)

        # ✅ Ensure numeric conversion for nutrition columns
        numeric_cols = ["calories", "protein", "carbohydrates", "fat"]
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
            else:
                print(f"[⚠️ WARNING] Column '{col}' not found in dataset — filled with zeros.")
                df[col] = 0

        # ✅ Drop duplicates and clean up
        if "name" in df.columns:
            df.drop_duplicates(subset=["name"], inplace=True)

        df.dropna(subset=["calories"], inplace=True)
        df = df[df["calories"] > 0]

        print(f"[INFO] Cleaned dataset — Rows: {len(df)}, Columns: {list(df.columns)}")
        return df

    except FileNotFoundError as fnf:
        print(f"[ERROR] {fnf}")
        return pd.DataFrame()  # Return empty DataFrame if file missing

    except Exception as e:
        print(f"[ERROR] Failed to load dataset: {str(e)}")
        return pd.DataFrame()
