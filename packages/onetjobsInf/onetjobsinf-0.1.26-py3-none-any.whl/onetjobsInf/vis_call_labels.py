
# This script connects to the O*NET Web Services API, 
# Retrieves all unique "Element Name" values for various tables (skills, knowledge, etc.),
# and saves them in a dictionary. 
# The dictionary is then saved to a JSON file for later use in visualizations.
import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'onetjobsInf')))

from OnetWebService import OnetWebService
from onet_credentials import get_credentials, check_for_error
from vis_call_elements import get_elements


# Get credentials from cache or prompt user
username, password = get_credentials()
onet_ws = OnetWebService(username, password)

vinfo = onet_ws.call('about')
check_for_error(vinfo)
print("Connected to O*NET Web Services version " + str(vinfo['api_version']))
print("")

element_dict = {}
# Define the tables we want to retrieve elements from
# could add : 'interests', 'work_values', 'work_styles' (also have element name and CI bounds)
for table in ['skills', 'knowledge', 'abilities']:
    # To get all possible values for a table, we can use the end filter
    # This ensures we get all values, since we use first 100 rows rather than just first 20
    qp = { 'end': "100" }
    els = get_elements(onet_ws, table, colname='element_name', **qp)
    element_dict[table] = sorted(els)

# Save element_dict to a file
output_file = 'onetjobsInf/src_data/element_name_dict.json'
with open(output_file, 'w') as f:
    json.dump(element_dict, f, indent=4)

print(f"Element Name Dictionary saved to {output_file}")
