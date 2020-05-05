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
    result = lines_that_contain(string, cif_file)
    date = str(result).split('20')[1]
    return(date)

PDB_ID = '3FY7'
PDB_file = open(PDB_ID + ".cif")

cif_downloader(PDB_ID)
print(collection_date(PDB_file))
