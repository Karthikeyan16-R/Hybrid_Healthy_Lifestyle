import os
import pandas as pd


def load_food_dataset(
    path: str = "app/data/Indian_Food_Nutrition_Processed.csv"
) -> pd.DataFrame:
    """
    Loads and cleans the Indian Food Nutrition dataset.

    Args:
        path (str): Path to the CSV file. Default is "app/data/Indian_Food_Nutrition_Processed.csv".

    Returns:
        pd.DataFrame: Cleaned DataFrame with normalized column names and numeric values for nutrition data.
    """
    # 🔹 Ensure the file exists
    if not os.path.exists(path):
        raise FileNotFoundError(f"❌ Dataset not found at: {os.path.abspath(path)}")

    # 🔹 Read CSV safely
    try:
        df = pd.read_csv(path, encoding="utf-8")
    except UnicodeDecodeError:
        # fallback if file is not utf-8 encoded
        df = pd.read_csv(path, encoding="latin1")

    # 🔹 Normalize column names (lowercase, no spaces)
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    # 🔹 Clean numeric columns if they exist
    for col in ["calories", "protein", "carbohydrates", "fat"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
        else:
            print(f"⚠️ Warning: Column '{col}' not found in dataset.")

    print(f"✅ Loaded dataset successfully from: {path}")
    print(f"📊 Shape: {df.shape[0]} rows × {df.shape[1]} columns")
    return df


# 🔹 Run directly
if __name__ == "__main__":
    try:
        df = load_food_dataset()
        print("\n🔍 Preview of the dataset:")
        print(df.head(10))  # show first 10 rows
        print("\n📘 Data Info:")
        print(df.info())
    except Exception as e:
        print(f"🚨 Error loading dataset: {e}")
