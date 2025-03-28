# Source: git clone https://github.com/onetcenter/web-services-samples 
# Python3 code for interacting with the API. 
# This code is released into the public domain.
import sys
import os 


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'onetjobsInf')))

from OnetWebService import OnetWebService
from onet_credentials import get_credentials, get_user_input, check_for_error

def get_abilities(onet_service, job_code):
    """
    Get abilities for a specific job code using the O*NET Web Service.
    
    Args:
        onet_service: An initialized OnetWebService instance
        job_code (str): The O*NET job code (e.g., '17-2051.00')
        
    Returns:
        dict: Abilities data for the specified job code
    """
    abilities_rslt = onet_service.call(f'mnm/careers/{job_code}/abilities')
    if check_for_error(abilities_rslt):
        return None
    return abilities_rslt

def print_abilities_result(abilities_data):
    """
    Format and print abilities data in a readable way
    
    Args:
        abilities_data (dict): The abilities data from the API response
    """
    print(f"\nAbilities for Occupation: {abilities_data.get('code', 'Unknown')}")
    print("=" * 50)
    
    if 'group' not in abilities_data or not abilities_data['group']:
        print("No abilities data available for this occupation.")
        return
    
    for group in abilities_data['group']:
        # Print the abilities group title
        group_title = group.get('title', {})
        print(f"\n{group_title.get('id', '')} - {group_title.get('name', 'Unknown Group')}")
        print("-" * 50)
        
        # Print each abilities element in the group
        if 'element' in group:
            for idx, element in enumerate(group['element'], 1):
                print(f"  {idx}. {element.get('id', '')} - {element.get('name', 'Unknown Ability')}")
        else:
            print("  No specific abilities listed in this group.")

def extract_ability_ids(abilities_data):
    """
    Extract all ability IDs from the abilities data structure.
    
    Args:
        abilities_data (dict): The abilities data from the API response
        
    Returns:
        list: A list of all ability IDs found in the data
    """
    ability_ids = []
    
    # Check if there's abilities group data
    if 'group' not in abilities_data or not abilities_data['group']:
        return ability_ids
    
    # Iterate through each group
    for group in abilities_data['group']:
        # Check if the group has elements
        if 'element' in group:
            # Extract the ID from each element
            for element in group['element']:
                if 'id' in element:
                    ability_ids.append(element['id'])
    
    return ability_ids

if __name__ == "__main__":
    # Get credentials from cache or prompt user
    username, password = get_credentials()
    onet_ws = OnetWebService(username, password)

    vinfo = onet_ws.call('about')
    check_for_error(vinfo)
    print("Connected to O*NET Web Services version " + str(vinfo['api_version']))
    print("")
    
    job_code = get_user_input('Job code for abilities query (e.g., 17-2051.00)')
    abilities_rslt = get_abilities(onet_ws, job_code)
    if abilities_rslt:
        print_abilities_result(abilities_rslt)
        ability_ids = extract_ability_ids(abilities_rslt)
        print(f"\nExtracted Ability IDs: {ability_ids}")
    else:
        print("Failed to retrieve abilities data.")