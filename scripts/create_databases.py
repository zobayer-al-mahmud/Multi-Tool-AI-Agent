import os
import pandas as pd
import sqlite3

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_DIR = os.path.join(BASE_DIR, "databases")

os.makedirs(DB_DIR, exist_ok=True)

def csv_to_sqlite(csv_path: str, db_path: str, table_name: str):
    """Load a CSV into a SQLite database table."""
    print(f"[INFO] Loading {csv_path} -> {db_path} (table: {table_name})")

    df = pd.read_csv(csv_path)

    # Basic clean-up (optional)
    df.columns = [c.strip().replace(" ", "_").lower() for c in df.columns]

    conn = sqlite3.connect(db_path)
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    conn.close()

    print(f"[DONE] Created {db_path} with table '{table_name}'")

def main():
    # Heart Disease
    heart_csv = os.path.join(DATA_DIR, "heart.csv")      # change if needed
    heart_db  = os.path.join(DB_DIR, "heart_disease.db")
    csv_to_sqlite(heart_csv, heart_db, "heart_patients")

    # Cancer
    cancer_csv = os.path.join(DATA_DIR, "cancer.csv")    # change if needed
    cancer_db  = os.path.join(DB_DIR, "cancer.db")
    csv_to_sqlite(cancer_csv, cancer_db, "cancer_patients")

    # Diabetes
    diabetes_csv = os.path.join(DATA_DIR, "diabetes.csv")  # change if needed
    diabetes_db  = os.path.join(DB_DIR, "diabetes.db")
    csv_to_sqlite(diabetes_csv, diabetes_db, "diabetes_patients")

if __name__ == "__main__":
    main()
