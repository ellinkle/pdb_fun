import pypdb

pdb_file = pypdb.get_pdb_file('6W9Q', filetype='cif', compression=False)
print(pdb_file[:200])

def lines_that_contain(string, fp):
    return [line for line in fp if string in line]

string = '_diffrn_detector.pdbx_collection_date'
result = lines_that_contain(string, pdb_file)
date = str(result).split(' ')
print(date)
