import requests
import json
import io

# Name:    functi
# Description: Change the state of the issue from pending done to done if the test id status is pass.
# Param [in]:  log link, jira credentials
# Param [out]: Nil
# Param [return]: Nil

def functi(status_link):
  url=status_link
  headers={
    "Accept":"application/json",
    "Content-Type":"application/json"
  }

  payload=json.dumps(
    {
    "transition": {
          "id": "101"
    }
  }
   )
  response=requests.post(url,headers=headers,data=payload,auth=("jenkins@uhnder.com","tlVTvkPcgqLWMCEXs4HlEB6C"))
  print(response.text)