JIRA JENKINS RESTAPI Interface Regression Automation Scripts:

Overview:
This repository contains automation scripts for handling JIRA regression bugs based on Jenkins test results. The scripts automatically update bug statuses, attach logs, and add comments based on test pass/fail outcomes.

Functionality:-
Bug Status Updates:
Moves bugs from "In Verification" to "Done" if tests pass.
Moves bugs to "In Progress" if tests fail.

Log Attachments:
Attaches python.stdout.log if tests run on X86.
Attaches version_postupld.log if tests run on hardware.

Comments & Labels:
Adds comments for test pass or fail cases.
Labels issues with closed_by_jenkins upon success.

JIRA Integration:
Fetches bug details using JIRA API.
Reads Jenkins results and determines test outcomes.

Scripts Description:
Iv_bugs.py – Main script for analyzing regression bugs and updating JIRA based on Jenkins results.
add_label.py – Adds closed_by_jenkins label if the test passes.
attach_log.py – Attaches python.stdout.log to JIRA if pipeline runs on X86.
fail_comment.py – Adds a failure comment if the test fails.
jira_status_done.py – Marks an issue as "Done" if the test passes.
jira_status_pdone.py – Moves an issue to "Pending Done" status.
pass_comment.py – Adds a success comment if the test passes.
Test_ID.py – Fetches the test ID from JIRA.
Vers_log.py – Attaches version_postupld.log for hardware-based tests.

Prerequisites:
Python 3.x
requests and jira modules installed
Valid JIRA credentials and access permissions

Usage:
Run Iv_bugs.py to automatically analyze and update JIRA regression issues based on Jenkins results:
