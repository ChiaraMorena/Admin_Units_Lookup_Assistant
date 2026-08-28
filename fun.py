import pandas as pd
import rapidfuzz
from rapidfuzz import process, fuzz

## FUNCTIONS ##

#Load the FAO GAUL dataset from a CSV file and return it as a pandas DataFrame

def get_fao_gaul(fao_gaul_version):

    #load the FAO GAUL dataset based on the specified version (fao_gaul24 or fao_gaul15)
    if fao_gaul_version == 'fao_gaul24':

        fao_gaul_db = pd.read_csv('data/fao_gaul24.csv',sep=';')
   
    elif fao_gaul_version == 'fao_gaul15':
    
        fao_gaul_db = pd.read_csv('data/fao_gaul15.csv',sep=';')

    #return as a pandas DataFrame
    return fao_gaul_db

#find a row in the FAO GAUL dataset based on a code and a specified level
def find_row_by_code(db,query,level):

    #make sure the query is a integer
    query = int(query)

    #set the level filter
    level_filter = f'gaul{level}_code'

    #show results based on the specified level and code
    results = db[db[level_filter] == query]
    return results

#Find a row in the FAO GAUL dataset based on a text query and a specified level
def find_row_by_text(db,query,level):

    #set the level filter
    level_filter = f'gaul{level}_name'

    #fuzzy search for the query
    choices = db[level_filter].to_dict()
    matches = process.extract(query, choices, scorer=fuzz.WRatio, limit=None, score_cutoff=90)
    df_matches = pd.DataFrame(matches)

    #show results
    results = db.iloc[df_matches[2]]
    #results = results.drop_duplicates(subset=[level_filter])
    return results