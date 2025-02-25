import requests
from requests.auth import HTTPBasicAuth
import json

# Name:    Test_id
# Description: Fetches the test id from jira 
# Param [in]:  Testid_link, jira credentials
# Param [out]:  Nil
# Param [return]: test case id

def Test_id(Testid_link):
	url=Testid_link

	headers={
	"Accept":"application/json",
	"Content-Type":"application/json"
	}

	#Getting the Bug_id
	response=requests.get(url,headers=headers,auth=("jenkins@uhnder.com","tlVTvkPcgqLWMCEXs4HlEB6C"))
	Fields = response.json()
	testcaseid =(Fields['fields']['customfield_11333'])
	return testcaseid