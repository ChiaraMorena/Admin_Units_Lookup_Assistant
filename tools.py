import pandas as pd
import rapidfuzz
from rapidfuzz import process, fuzz

## FUNCTIONS ##

#Load the FAO GAUL 2024 dataset from a CSV file and return it as a pandas DataFrame
def get_fao_gaul24():
    """
    Load the FAO GAUL 2024 dataset from a CSV file and return it as a pandas DataFrame.
    
    Returns:
        pd.DataFrame: The FAO GAUL 2024 dataset.
    """
    fao_gaul24 = pd.read_csv('data/fao_gaul24.csv',sep=';',encoding='latin-1')
    return fao_gaul24

#search for a row in the FAO GAUL dataset based on a text query and a specified level

def find_row_by_text(query,level,n_results=5):

    #search for the query in the specified level of the FAO GAUL dataset using fuzzy matching
    level_filter = f'gaul{level}_name'
    fao_gaul24 = get_fao_gaul24()
    choices = fao_gaul24[level_filter].to_dict()
    matches = process.extract(query, choices, scorer=fuzz.WRatio, limit=None, score_cutoff=90)

    #create a dataframe with the matches and their corresponding indices in the original dataset
    df_matches = pd.DataFrame(matches)
    results = fao_gaul24.iloc[df_matches[2]]

    #drop duplicates based on the specified level to ensure unique results
    results = results.drop_duplicates(subset=[level_filter])

    #manage the case when no results are found
    if results.empty:
        return {
            "success": False,
            "error": f'No results found for code "{query}" at level "{level}".'
        }

    return results.head(n_results)

#search for a row in the FAO GAUL dataset based on a codeand a specified level

def find_row_by_code(query,level,n_results=5):

    fao_gaul24 = get_fao_gaul24()
    #set the query to integer and filter the FAO GAUL dataset based on the specified level and code
    query = int(query)
    level_filter = f'gaul{level}_code'
    results = fao_gaul24[fao_gaul24[level_filter] == query]

    #manage the case when no results are found
    if results.empty:
        return {
            "success": False,
            "error": f'No results found for code "{query}" at level "{level}".'
        }
    
    return results.head(n_results)


## @TOOLS ###

def query_fao_gaul24(query,level,n_results=5) -> pd.DataFrame:
    """
    Query the FAO GAUL 2024 dataset based on a text or code query and a specified level.
    
    Args:
        query (str): The text query to search for.
        level (str): The level of the GAUL dataset to search in (e.g., 'country', 'region').
        n_results (int): The number of results to return.
    
    Returns:
        pd.DataFrame: A DataFrame containing the matching rows from the FAO GAUL 2024 dataset.
    """
    #1. Laod the FAO GAUL 2024 dataset
    

    #2. Determine if the query is a code (numeric) or text (string)
    if isinstance(query, int) or query.isdigit():
        return find_row_by_code(query, level)
    else:
        return find_row_by_text(query, level, n_results)