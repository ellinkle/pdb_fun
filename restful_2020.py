import requests
import pypdb
from datetime import datetime

start_date = "2020-03-12"
today = datetime.now()
end_date = today.strftime("%Y-%m-%d")

def PDB_searcher():

    # RESTful search interface
    url = 'http://www.rcsb.org/pdb/rest/search'

    # add XML formatted search query here. Generator can help: http://www.rcsb.org/pdb/software/rest.do
    query_text = f"""

    <orgPdbQuery>

    <queryType>org.pdb.query.simple.DepositDateQuery</queryType>

    <pdbx_database_status.recvd_initial_deposition_date.min>{start_date}</pdbx_database_status.recvd_initial_deposition_date.min>

    <pdbx_database_status.recvd_initial_deposition_date.max>{end_date}</pdbx_database_status.recvd_initial_deposition_date.max>

    </orgPdbQuery>

    """
    #print("Query: %s" % query_text)
    #print("Querying RCSB PDB REST API...")


    # pulls the header of the search results from the url (PDB ID)
    header = {'Content-Type': 'application/x-www-form-urlencoded'}

    response = requests.post(url, data=query_text, headers = header)

    return response

# converts the big string of PDB IDs into a list and removes empty spaces
def convert_to_ID(results):
    text = results.text
    PDB_list = list(text.split('\n'))
    PDB_list = [string for string in PDB_list if string != ""]
    return PDB_list

response = PDB_searcher()

PDB_list = convert_to_ID(response)

print(f"PDBs since {start_date}: {len(PDB_list)}.")
