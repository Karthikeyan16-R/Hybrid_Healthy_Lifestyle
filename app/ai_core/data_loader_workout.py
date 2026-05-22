import os
import pandas as pd

def load_workout_dataset(path: str = None) -> pd.DataFrame:
    """
    Load and clean the Fitbit daily activity dataset safely.
    """

    try:
        # Auto-detect default path
        if path is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            path = os.path.join(base_dir, "../data/dailyActivity_merged.csv")

        path = os.path.normpath(path)
        print(f"[INFO] Loading workout dataset from: {path}")

        if not os.path.exists(path):
            raise FileNotFoundError(f"Workout dataset not found at path: {path}")

        # Load dataset
        df = pd.read_csv(path)
        print(f"[INFO] Raw workout dataset loaded — Rows: {len(df)}")

        # Normalize column names
        df.columns = [c.strip().lower() for c in df.columns]

        # Required columns
        required_cols = [
            "veryactiveminutes",
            "fairlyactiveminutes",
            "lightlyactiveminutes",
            "sedentaryminutes",
            "calories"
        ]

        for col in required_cols:
            if col not in df.columns:
                print(f"[⚠️ WARNING] Missing column '{col}', filling with 0")
                df[col] = 0

        # Convert to numeric
        for col in required_cols:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

        # Remove invalid rows
        df = df[df["calories"] > 0]

        print(f"[INFO] Cleaned workout dataset — Rows: {len(df)}")
        return df

    except Exception as e:
        print(f"[ERROR] Failed to load workout dataset: {str(e)}")
        return pd.DataFrame()
