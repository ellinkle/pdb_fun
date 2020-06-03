from beamline import redis
import pickle
import pandas as pd

# for getting the COVID pdbs off redis and into a spreadsheet

redpickle = redis.get('eleanor:covid_pdb_getter:something')

cov_data = pickle.loads(redpickle)

# convert dataframe to csv
cov_data.to_csv(r"Rapid_access_PDBs_2020.csv",
           header=True, index = False)
