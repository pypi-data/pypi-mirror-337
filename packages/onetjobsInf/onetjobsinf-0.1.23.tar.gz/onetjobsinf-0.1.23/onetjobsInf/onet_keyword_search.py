# Source: git clone https://github.com/onetcenter/web-services-samples 
# Python3 code for interacting with the API. 
# This code is released into the public domain.

#!python3
from onetjobsInf.OnetWebService import OnetWebService
from onetjobsInf.onet_credentials import get_credentials, get_user_input, check_for_error


# Get credentials from cache or prompt user
username, password = get_credentials()
onet_ws = OnetWebService(username, password)

vinfo = onet_ws.call('about')
check_for_error(vinfo)
print("Connected to O*NET Web Services version " + str(vinfo['api_version']))
print("")

kwquery = get_user_input('Keyword search query')
kwresults = onet_ws.call('online/search',
                         ('keyword', kwquery),
                         ('end', 50))
check_for_error(kwresults)
if (not 'occupation' in kwresults) or (0 == len(kwresults['occupation'])):
    print("No relevant occupations were found.")
    print("")
else:
    print("Most relevant occupations for \"" + kwquery + "\":")
    for occ in kwresults['occupation']:
        print("  " + occ['code'] + " - " + occ['title'])
    print("")