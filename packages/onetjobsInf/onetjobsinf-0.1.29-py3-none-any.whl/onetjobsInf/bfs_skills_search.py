# Source: git clone https://github.com/onetcenter/web-services-samples 
# Python3 code for interacting with the API. 
# This code is released into the public domain.

#!python3
import sys
import os 


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'onetjobsInf')))
from OnetWebService import OnetWebService
from onet_credentials import get_credentials, get_user_input, check_for_error


def print_skills_result(skills_data):
    """
    Format and print skills data in a readable way
    
    Args:
        skills_data (dict): The skills data from the API response
    """
    print(f"\nSkills for Occupation: {skills_data.get('code', 'Unknown')}")
    print("=" * 50)
    
    if 'group' not in skills_data or not skills_data['group']:
        print("No skills data available for this occupation.")
        return
    
    for group in skills_data['group']:
        # Print the skill group title
        group_title = group.get('title', {})
        print(f"\n{group_title.get('id', '')} - {group_title.get('name', 'Unknown Group')}")
        print("-" * 50)
        
        # Print each skill element in the group
        if 'element' in group:
            for idx, element in enumerate(group['element'], 1):
                print(f"  {idx}. {element.get('id', '')} - {element.get('name', 'Unknown Skill')}")
        else:
            print("  No specific skills listed in this group.")

def extract_skill_ids(skills_data):
    """
    Extract all skill IDs from the skills data structure.
    
    Args:
        skills_data (dict): The skills data from the API response
        
    Returns:
        list: A list of all skill IDs found in the data
    """
    skill_ids = []
    
    # Check if there's skill group data
    if 'group' not in skills_data or not skills_data['group']:
        return skill_ids
    
    # Iterate through each group
    for group in skills_data['group']:
        # Check if the group has elements
        if 'element' in group:
            # Extract the ID from each element
            for element in group['element']:
                if 'id' in element:
                    skill_ids.append(element['id'])
    
    return skill_ids

def get_skills(onet_service, job_code):
    """
    Get skills for a specific job code using the O*NET Web Service.
    
    Args:
        onet_service: An initialized OnetWebService instance
        job_code (str): The O*NET job code (e.g., '17-2051.00')
        
    Returns:
        dict: Skills data for the specified job code
    """
    skills_rslt = onet_service.call(f'mnm/careers/{job_code}/skills')
    if check_for_error(skills_rslt):
        return None
    return skills_rslt

# Only run the following if this script is executed directly (not imported)
if __name__ == "__main__":
    # Get credentials from cache or prompt user
    username, password = get_credentials()
    onet_ws = OnetWebService(username, password)

    vinfo = onet_ws.call('about')
    check_for_error(vinfo)
    print("Connected to O*NET Web Services version " + str(vinfo['api_version']))
    print("")
    
    job_code = get_user_input('Job code for skills query (e.g., 17-2051.00)')
    skills_rslt = get_skills(onet_ws, job_code)
    if skills_rslt:
        print_skills_result(skills_rslt)
    else:
        print("Failed to retrieve skills data.")