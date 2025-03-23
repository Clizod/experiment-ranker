
import os
import re
import pandas as pd

reg_exp_file_result = re.compile("(?P<model>[A-za-z0-9-]+)_(?P<exp>[A-za-z0-9-]+).csv")

csv_col_map = {
    0: 'id',
    1: 'response'
}

def process_results(df_source, exp_to_load, results_root_dir, parser):
    df_results = pd.DataFrame()
    for root_path, sub_dir, files in os.walk(results_root_dir):
        
        if len(files) == 0:
            continue        

        if len([item for item in exp_to_load if(item in root_path)]) == 0:
            continue
        
        keys = os.path.basename(root_path)
        print(f"Reading - {root_path}")    

        df_exp = pd.concat([read_csv_results(root_path, f, keys, parser) for f in files], axis=0, ignore_index=True)
        df_results = pd.concat([df_results, df_exp])
            
    print(f"There are {len(df_results)} rows in this dataset.")

    df_comb_results = pd.merge(
        df_results, 
        df_source[['id', 'tag', 'reference']], 
        how='left',
        left_on="id", 
        right_on="id"
    )

    return df_comb_results

def read_csv_results(base_path, file_name, keys, parser):
    #Split the file name into its components
    components = reg_exp_file_result.search(file_name).groupdict()
    
    model = components["model"]
    exp = components["exp"]

    path = os.path.join(base_path, file_name)
    df = pd.read_csv(path)
        
    # Rename the columns for clarity
    df.columns = [csv_col_map.get(i, col) for i, col in enumerate(df.columns)]

    answer_columns = df['response'].apply(parser)
    df = pd.concat([df.drop(columns=['response']), answer_columns], axis=1)
    
    key_parts = keys.split('-')
    df.insert(loc=1, column='experiment', value=exp)
    df.insert(loc=2, column='model', value=model)
    df.insert(loc=3, column='disease', value=key_parts[0])
    df.insert(loc=4, column='variable', value=key_parts[1])
    return df


def apply_len_tie_breaker(df_source, df_ranked, rank_column_name):
    # Creating a tie breaker column - using text length for now
    df_tie = df_source[['id','target']].copy()
    df_tie['target_len'] = df_tie['target'].str.len()

    df_rerank = pd.merge(
        df_ranked, 
        df_tie, 
        how='left',
        left_on="id", 
        right_on="id"
    )

    # Ensure there are no duplicate labels by resetting the index after sorting
    df_rerank = (
        df_rerank
        .sort_values(by=['experiment', 'model', 'disease', 'variable', rank_column_name, 'target_len'], ascending=[True, True, True, True, False, False])
        .reset_index(drop=True)
    )

    # Create the index column stratified by experiment, model, disease, and variable
    df_rerank['ranking'] = (
        df_rerank
        .groupby(['experiment', 'model', 'disease', 'variable'])
        .cumcount() + 1
    )
    return df_rerank