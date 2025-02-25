import requests
import json
import io

# Name:    function
# Description: attach the python.stdout.log to jira if the pipeline is running on X86 and status of the test id is pass
# Param [in]:  jira credentials
# Param [out]: Nil
# Param [return]: Nil

def attachment_postlog(attachment_link):
    url = attachment_link
    headers={
        "X-Atlassian-Token": "no-check"
    }
    files={
        "file":("python.stdout.log",open("python.stdout.log","rb"))
    }

    response=requests.post(url,headers=headers,files=files,auth=("jenkins@uhnder.com","tlVTvkPcgqLWMCEXs4HlEB6C"))
    #print(response.text)