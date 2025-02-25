import requests
import json
import io

# Name:    function
# Description: attach the pass comment to jira if the status of the test id is pass
# Param [in]:  log link, jira credentials
# Param [out]: Nil
# Param [return]: Nil

def funct(log_link):
  url=log_link
  headers={
    "Accept":"application/json",
    "Content-Type":"application/json"
  }
  data=json.dumps({
    
    "body": {
      "type": "doc",
      "version": 1,
      "content": [
        {
          "type": "paragraph",
          "content": [
            {
              "text": "Verified and logs are added in Attachments",
              "type": "text"
            }
          ]
        }
      ]
    }
  })

  response=requests.post(url,headers=headers,data=data,auth=("jenkins@uhnder.com","tlVTvkPcgqLWMCEXs4HlEB6C"))
  #print(response.text)