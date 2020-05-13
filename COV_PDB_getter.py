import requests
import pypdb
import pandas as pd
import restful_2020
from beamline import redis
import pickle

# define redis key and expiry
KEY = 'eleanor:covid_pdb_getter:something'
EXP = 60 * 60 * 24 * 30

# queries PDB using restful API
response = restful_2020.PDB_searcher()
pdb_list = restful_2020.convert_to_ID(response)

# search terms in cif file for collection site and date
synch_string = '_diffrn_source.pdbx_synchrotron_site'
date_string = '_diffrn_detector.pdbx_collection_date'

# func from pypdb that gets cif data for given ID (does not save file)
def get_pdb(ID):
    pdb_data = pypdb.get_pdb_file(ID, filetype = 'cif', compression=False)
    return pdb_data

# searches for line in file fp containing search term 'string'
def lines_that_contain(string, fp):
    return [line for line in fp.splitlines() if string in line]

# searches cif for collection site string, strips empty spaces
def collection_site(cif_file):
    result = lines_that_contain(synch_string, cif_file)
    site = (result[0].split('       ')[1]).strip()
    return site

# searches cif for collection date string, strips empty spaces
def collection_date(cif_file):
        result = lines_that_contain(date_string, cif_file)
        date = (result[0].split('         ')[1]).strip()
        return date

# Aus Synch IDs will get put here
results = []

# Checks all PDBs and grabs Aus Synch ones, puts into 'results' list
# bad error handling, but sometimes cifs have empty fields and upset program
for ID in pdb_list:
    print(f"Checking {ID}...")
    pdb_string = get_pdb(ID)
    try:
        site = collection_site(pdb_string)
        if site == "'Australian Synchrotron'":
            results.append(ID)
        else:
            continue
    except:
        continue

# make an empty dataframe to put PDB info into
data = {'PDB ID': [], 'TITLE': [], 'AUTHORS': [], 'COLLECTION DATE': []}
df = pd.DataFrame.from_dict(data)

# using pypdb to fetch description data for given ID, append to dataframe
# collection date is sometimes empty or a ? so error exception to output empty field rather than crashing
for ID in results:
    print(f"Adding {ID}...")
    pdb_string = get_pdb(ID)
    pypdb.describe_pdb(ID)
    out = pypdb.get_info(ID, url_root = 'http://www.rcsb.org/pdb/rest/describePDB?structureId=')
    out = pypdb.to_dict(out)
    outdict = pypdb.remove_at_sign(out['PDBdescription']['PDB'])
    try:
        date = collection_date(pdb_string)
    except:
        date = []
    newer = {'PDB ID':(outdict['structureId']), 'TITLE':(outdict['title']), 'AUTHORS': (outdict['structure_authors']), 'COLLECTION DATE': (collection_date(pdb_string))}
    df = df.append(newer,ignore_index=True,sort=False)

# pickle --> object serialization (better format for pushing to redis and then getting and depickling)
df_pickle = pickle.dumps(df)


# putting df_pickle in redis under KEY with expiry time EXP
redis.setex(KEY, EXP, df_pickle)



# convert dataframe to csv
#df.to_csv(r"Aus_Synch_PDBs_2020.csv",
#           header=True, index = False)


print(f"Check finished. {len(results)} PDB IDs in dataframe, pickled and sent to redis.")
