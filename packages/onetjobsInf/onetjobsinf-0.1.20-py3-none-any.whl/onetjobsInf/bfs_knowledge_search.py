# Source: git clone https://github.com/onetcenter/web-services-samples 
# Python3 code for interacting with the API. 
# This code is released into the public domain.
import sys
import os 

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'onetjobsInf')))
from OnetWebService import OnetWebService
from onet_credentials import get_credentials, get_user_input, check_for_error


def print_knowledge_result(knowledge_data):
    """
    Format and print knowledge data in a readable way
    
    Args:
        knowledge_data (dict): The knowledge data from the API response
    """
    print(f"\nKnowledge for Occupation: {knowledge_data.get('code', 'Unknown')}")
    print("=" * 50)
    
    if 'group' not in knowledge_data or not knowledge_data['group']:
        print("No knowledge data available for this occupation.")
        return
    
    for group in knowledge_data['group']:
        # Print the knowledge group title
        group_title = group.get('title', {})
        print(f"\n{group_title.get('id', '')} - {group_title.get('name', 'Unknown Group')}")
        print("-" * 50)
        
        # Print each knowledge element in the group
        if 'element' in group:
            for idx, element in enumerate(group['element'], 1):
                print(f"  {idx}. {element.get('id', '')} - {element.get('name', 'Unknown Knowledge')}")
        else:
            print("  No specific knowledge listed in this group.")

def get_knowledge(onet_service, job_code):
    """
    Get knowledge data for a specific job code using the O*NET Web Service.
    
    Args:
        onet_service: An initialized OnetWebService instance
        job_code (str): The O*NET job code (e.g., '17-2051.00')
        
    Returns:
        dict: Knowledge data for the specified job code
    """
    knowledge_rslt = onet_service.call(f'mnm/careers/{job_code}/knowledge')
    if check_for_error(knowledge_rslt):
        return None
    return knowledge_rslt

def extract_knowledge_ids(knowledge_data):
    """
    Extract all knowledge IDs from the knowledge data structure.
    
    Args:
        knowledge_data (dict): The knowledge data from the API response
        
    Returns:
        list: A list of all knowledge IDs found in the data
    """
    knowledge_ids = []
    
    # Check if there's knowledge group data
    if 'group' not in knowledge_data or not knowledge_data['group']:
        return knowledge_ids
    
    # Iterate through each group
    for group in knowledge_data['group']:
        # Check if the group has elements
        if 'element' in group:
            # Extract the ID from each element
            for element in group['element']:
                if 'id' in element:
                    knowledge_ids.append(element['id'])
    
    return knowledge_ids

# Only run the following if this script is executed directly (not imported)
if __name__ == "__main__":
    # Get credentials from cache or prompt user
    username, password = get_credentials()
    onet_ws = OnetWebService(username, password)

    vinfo = onet_ws.call('about')
    check_for_error(vinfo)
    print("Connected to O*NET Web Services version " + str(vinfo['api_version']))
    print("")
    
    job_code = get_user_input('Job code for knowledge query (e.g., 17-2051.00)')
    knowledge_rslt = get_knowledge(onet_ws, job_code)
    if knowledge_rslt:
        print_knowledge_result(knowledge_rslt)
        knowledge_ids = extract_knowledge_ids(knowledge_rslt)
        print(f"\nExtracted Knowledge IDs: {knowledge_ids}")
    else:
        print("Failed to retrieve knowledge data.")