from jira import JIRA

# Name:    function
# Description: adds the "closed_by_jenkins" label is the status of the test id is pass.
# Param [in]:  jira credentials
# Param [out]: Nil
# Param [return]: Nil

def function(bug_id):
    jira_connection = JIRA(
        basic_auth=('jenkins@uhnder.com', 'tlVTvkPcgqLWMCEXs4HlEB6C'),
        server="https://uhnder.atlassian.net"
    )

    issue = jira_connection.issue(bug_id)
    print("closed_by_jenkins label is added sucessfully")
    issue.fields.labels.append(u'closed_by_jenkins')
    issue.update(fields={"labels": issue.fields.labels})
