import pandas as pd

# Data Extraction


def run_extraction():
    try:
        data = pd.read_csv(r"zipco_transaction.csv")
        print("Data extracted successfully")
    except Exception as e:
        print(f"An error occured: {e}")


if __name__ == "__main__":
    run_extraction()
