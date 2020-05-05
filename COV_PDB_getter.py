import requests

string = '_diffrn_detector.pdbx_collection_date'


def cif_downloader(ID):
    full_url = "https://files.rcsb.org/download/"
    full_url += ID + ".cif"
    response = requests.get(full_url)
    open(f"{ID}.cif", 'wb').write(response.content)


def lines_that_contain(string, fp):
    return [line for line in fp if string in line]


def collection_date(cif_file):
    result = lines_that_contain(string, pdb_file)
    date = str(result).split(' ')[9]
    return(date)

# example!
PDB_ID = '3FY7'

cif_downloader(PDB_ID)
print(collection_date(PDB_ID))
