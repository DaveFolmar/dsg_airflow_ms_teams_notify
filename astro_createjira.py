from atlassian import Jira
import argparse, json, sys
import requests
import dave_config
import json

#DSG- Jira Service Management Sandbox URL
url = 'https://dcsgcloud-sandbox-871.atlassian.net/rest/api/3/issue'
print("URL: " + url)

# Define a file name where you want to store the output
output_file = "output.txt"


message = 'Message'
jobname = 'FolmarTest'
nodename = 'rhel-cs-p-XYXX'
completion_code = '099'
scheduling_date = '09/23/23'
cm_time = '09:00'
cm_application = 'TSD'
cm_applicationGroup = 'YYY'
cm_group = 'Tech-CommandCenter'


print("Job Name: " + jobname)
print("Nodename: " + nodename)
print("Completion Code: " + completion_code)
print("Scheduling Date: " + scheduling_date)
print("Time: " + cm_time)
print("Control-M Applicaton: " + cm_application)
print("Control-M Appliction Group: " + cm_applicationGroup)

jira_project_key = 'TSD'
print("Jira Project Key: " + jira_project_key)
jira_impact = 'Significant / Large'
print("Jira Impact: " + 'Significant / Large')
jira_urgency = 'Medium'
print("jira Urgency: " + 'Medium')
jira_assignee = '63f2c6e940328c12e4eb37ae'
print("Jira_assignee: " + '63f2c6e940328c12e4eb37ae')

# Handle the optional --message and --group arguments outside of argparse
cm_message = message

if message is not None:
    summary = (message + " Folmar App job " + jobname + " on node " + nodename + " return code " + completion_code)

else:
    summary = (" Control-M job " + jobname + " on node " + nodename + " return code " + completion_code)

cm_group = "Tech-CommandCenter"  # Default value for --group
if cm_group:
    if cm_group.startswith('Tech-'):
        cm_group = cm_group
    else:
        print("Group must start with 'Tech-'")
        sys.exit(1)

description = "Control-M Task Failure\nJob Name: " + jobname + "\nHostname: " + nodename + "\nApplication Group: " + cm_application + "\nSub Application: " + cm_applicationGroup + "\nCompletion Code: " + completion_code+ "\nOrder Date: " + scheduling_date + "\nRun Date: " + cm_time + "\n"

# Redirect output to the file
with open(output_file, "w") as output:
    # Print the variables to the file
    print("cm_message:", cm_message, file=output)
    print("Description: ", description, file=output)
    print("Summary: ", summary, file=output)

# Create the ticket
payload = json.dumps({
  "fields": {
    "project": {
      "key": "TSD"
    },
    "issuetype":{
      "id":"10040"
    },
    "summary": summary,
    "priority": {
      "name: ":"Low",
      "id": "4",   # Low = 4, Medium=3, High=2
    },
    "customfield_10099": {
      "value":"Low",
      "id":"10270"  #Urgency: Low - 10270
    },
    "customfield_10097": {
      "value": "Minor",
      "id": "10256"  #Impact
    },
    # Assignee Group-set for DSGCloud - Good
    "customfield_10077": {
      "name": cm_group
     # "groupId":"8fcd9351-1736-4d2c-b9f1-0d22a70424a0"
    },
    # Source updated for DSGCloud - ok
    "customfield_10140": {
      "value": "Control-M",
      "id": "10455"
    },
    "reporter": {
      "id": "712020:2d789736-5bc9-468b-a972-e8e850eddf5c"
    },
    "assignee": {
      "id": "712020:2d789736-5bc9-468b-a972-e8e850eddf5c"
    },
    "description": {
      "type": "doc",
      "version": 1,
      "content": [
        {
          "type": "paragraph",
          "content": [
            {
              "type": "text",
              "text": description
            }
          ]
        }
      ]
    }
  }
})

print(payload)
headers = {
  'Authorization': 'Basic c3J2LWN0cmxtamlyYUBkY3NnLmNvbTpBVEFUVDN4RmZHRjBra2hGdVhPV2prTkpiTUhhSTFZM0JISkhNVnc3WGVyT1JrWmo0LUxtc01MandVNmFOam9kSEN4YmZqOUJQQlduN0JhM0NzRVZHNTQyVEVueWNvQVFQTEZLZzlxUkpUX0RnQXllb0x6anM3QmVQbUZiZE1FeXR5OHR1MUJ1RWpFUm1GRzVrRThaYWliQi1aazhRWGRHdE5KUDU4MEZGTVBqbHRDMUdHY012ejQ9M0IyNEJCNzU=',
  'Content-Type': 'application/json',
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)

