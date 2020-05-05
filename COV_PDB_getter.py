import requests
import pypdb

# list of pdbs to acquire collection dates from (use restful_ex.py to get MX list)
pdb_list = ['4P15', '3BFO', '4Z9C']
# search term in cif file for collection date
string = '_diffrn_detector.pdbx_collection_date'

# a tool for downloading and saving cif files from the databank. Files save to working dir.
def cif_downloader(ID):
    full_url = "https://files.rcsb.org/download/"
    full_url += ID + ".cif"
    response = requests.get(full_url)
    open(f"{ID}.cif", 'wb').write(response.content)

# func from pypdb that gets cif data for given ID (does not save file)
def get_pdb(ID):
    pdb_data = pypdb.get_pdb_file(ID, filetype = 'cif', compression=False)
    return pdb_data

# searches for line in file fp containing search term 'string'
def lines_that_contain(string, fp):
    return [line for line in fp.splitlines() if string in line]

# searches cif for string, outputs date in format YY-MM-DD as a string
def collection_date(cif_file):
    result = lines_that_contain(string, cif_file)
    date1 = str(result).split('20')[1]
    date2 = date1.split(' ')[0]
    return(date2)


for ID in pdb_list:
    pdb_string = get_pdb(ID)
    date = collection_date(pdb_string)
    print(date)

