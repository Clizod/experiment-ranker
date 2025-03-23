import pandas as pd

def load_data(input_file_path, show_count = True):
    df_raw = pd.read_csv(input_file_path)

    if show_count:
        print(f"There are {len(df_raw)} rows in this dataset.")

    return df_raw