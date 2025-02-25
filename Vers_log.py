import requests
import json
import io

# Name:    function
# Description: attach the version_postupld.log to jira if the pipeine is running on hardware and status of the test id is pass
# Param [in]:  jira credentials
# Param [out]: Nil
# Param [return]: Nil

def function(attachment_link):
    url = attachment_link
    headers={
        "X-Atlassian-Token": "no-check"
    }
    files={
        "file":("version_postupld.log",open("version_postupld.log","rb"))
    }

    response=requests.post(url,headers=headers,files=files,auth=("jenkins@uhnder.com","tlVTvkPcgqLWMCEXs4HlEB6C"))
    #print(response.text)