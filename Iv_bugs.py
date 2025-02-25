#!/usr/bin/env python

# Copyright (C) Uhnder, Inc. All rights reserved. Confidential and Proprietary - under NDA.



"""To look at the open regression bugs (those in PV state) and look at latest jenkins results and update the status accordingly."""



#==============================================================================================================================

#  To look at the open regression bugs (those in PV state) and look at latest jenkins results and update the status accordingly.

#The script identify the open Regression bugs, those in pending verification state and to look at the Jenkins results of the given 
#test-id and will automatically close the bugs, add comments, logs if the status of the given test id is Pass, 
#else the script will automatically move the status of bugs to “In Progress” and add a Fail comment.

#==============================================================================================================================

import requests
import json
import time
import io
import csv
import os
import re
import pass_comment
import jira_status_pdone
import jira_status_done
import add_label
from attach_log import attachment_postlog
import Test_ID 
import fail_comment
import glob
import jira_status_inprog
import Vers_log

# Name:    func
# Description:  Reads all the csv files
# Param [in]:  path of csv directory, all th csv files
# Param [out]: gives the csv file path in which it reads and execute the status
# Param [return]: jenkins result pass/fail, log link

def func(csv_file_name, test_id):
  csv_files = glob.glob(os.path.join("jenkins-regression-tests/Interns-codes/Regression_iv_bugs", "*.csv"))
  csv_files.sort()
  csv_files.reverse()
  #print(csv_files)

  data=[]
  #Getting the status of the test_id
  status = 'Fail'
  #print(csv_files)
  for csv_path in csv_files:
    with open(csv_path) as csvfile:
      print(csv_path)
      print("\n")
      reader = csv.reader(csvfile)
      for row in reader:
        data.append(row)
        if row == '<html>':
          continue

        else:
          for row in data:
            if len(row)>2:
              #print(len(row))
              if(row[3] == test_id):
                status = row[8]
                log = row[1]
                version_postupld_link= log.split("<")[1].split(">")[0]
                version_postupld_link=version_postupld_link.replace("a href=", '')
                version_postupld_link=version_postupld_link.replace("\"", '')
                print(version_postupld_link)
                print(status)
                return status,version_postupld_link


# Name:    function
# Description: fetches the pipeline link, issue id and and creates csv files for last 5 builds and update the state according to the result in csv 
# Param [in]:  jira credentials, jenkins credentials, jira query
# Param [out]: pipeline link,test id, issue id, pipeline last 5 builds url
# Param [return]: test id,issue id,url,attachment link, log link, status link

def function():
  url="https://uhnder.atlassian.net/rest/api/2/search"
  
  headers={
  "Accept":"application/json",
  "Content-Type":"application/json"
  }

  query = {
  'jql':'project = SWC AND issuetype = Bug AND status = "In Verification" AND labels = Regression'
  }

  #Getting the Bug_id, link of pipeline and test_case_id from bug description
  response=requests.get(url,headers=headers,params=query,auth=("jenkins@uhnder.com","tlVTvkPcgqLWMCEXs4HlEB6C"))
  data=response.json()
  issues=data["issues"]
  req_issue=[]
  for issue in range(len(issues)):
    if data["issues"][issue]["fields"]["customfield_11127"] != None and "http" in data["issues"][issue]["fields"]["customfield_11127"]:
      req_issue.append(issue)
  #print(req_issue)
  for issue in req_issue:
    #print(issue)
    fields=data["issues"][issue]["fields"]["customfield_11127"].split('\n')
    link=fields[0]
    bug_id=data["issues"][issue]["key"]  
    Testid_link= url.split("2")[0]+"3/issue/"+bug_id
    tcid = Test_ID.Test_id(Testid_link)
    print(bug_id)
    print("\n")
    print(link)
    print(tcid)
    print("\n")
    data_json = requests.get(link+"api/json?pretty=true", auth=('admin', 'admin')).json()
    #data_json_len = len(data_json["builds"])

    #Getting the last 5 builds of the pipeline and downloading the csv
    for build in range(5):
      artifacts=data_json["builds"][build]["url"]
      print(artifacts)
      try:
        urll=artifacts+"artifact/new_output.csv"
        with requests.get(urll, auth=('admin', 'admin')) as rq:
          with open(artifacts.split('/')[-2]+".csv", 'wb') as file:
            file.write(rq.content)
      except:
          pass
          print("\n")
    #Getting the Pass/Fail status of test_case_id by reading the csv
    status,version_postupld_link = func("jenkins-regression-tests/Interns-codes/Regression_iv_bugs",tcid)
    log_link= url.split("2")[0]+"3/issue/"+bug_id+"/comment"
    status_link = url.split("2")[0]+"3/issue/"+bug_id+"/transitions"
    #Updating the comment, status if the status is Fail and deleting the csv files
    if status == "Fail":
      print("Test_case is failed and status of issue is now moved to IN PROGRESS")
      fail_comment.function(log_link)
      jira_status_inprog.function(status_link)
      path = "jenkins-regression-tests/Interns-codes/Regression_iv_bugs/"
      for csvrmv in os.listdir(path):
        if csvrmv.endswith('.csv'):
          os.unlink(path + csvrmv)
    else: 
      #Updating the comment, status,label,adding the attachments if the status is Pass and deleting the csv files
      print("\n")
      log_json = requests.get(version_postupld_link+"/version_postupld.log",auth=('admin', 'admin')).text
      with open("version_postupld.log","w") as file:
        file.write(log_json)
      file.close()
      flag = 0
      with open(r'version_postupld.log', "r") as fp:
        lines = fp.readlines()
        for row in lines:
          if re.search("Error 404 Not Found",row):
            flag = 1 
            break
      fp.close()
      if flag == 1:
        os.remove("version_postupld.log")
        log_stdout = requests.get(version_postupld_link+"/python.stdout.log",auth=('admin', 'admin')).text
        with open("python.stdout.log","w") as file:
          file.write(log_stdout)
        file.close()
        attachment_link = url.split("2")[0]+"3/issue/"+bug_id+"/attachments"
        attachment_postlog(attachment_link)
      else:
        log_json = requests.get(version_postupld_link+"/version_postupld.log",auth=('admin', 'admin')).text
        with open("version_postupld.log","w") as file:
          file.write(log_json)
        file.close()
        attachment_link = url.split("2")[0]+"3/issue/"+bug_id+"/attachments"
        Vers_log.function(attachment_link)
      pass_comment.funct(log_link)
      attachment_link = url.split("2")[0]+"3/issue/"+bug_id+"/attachments"
      #attach_log.function(attachment_link)
      #print(attachment_link)
      #print(status_link)
      add_label.function(bug_id)
      jira_status_pdone.function(status_link)
      jira_status_done.functi(status_link)
      print("Tested and Logs are attached sucessfully in Jira attachments")
      print("Bug status is now moved to DONE")
      print("\n")
      path = "jenkins-regression-tests/Interns-codes/Regression_iv_bugs/"
      for csvrmv in os.listdir(path):
        if csvrmv.endswith('.csv'):
          os.unlink(path + csvrmv)
  return tcid,bug_id,url
tcid,bug_id,url=function()

