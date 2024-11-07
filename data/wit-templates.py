# pip install -r requirements.txt
import requests
import os
import base64

# Replace with your Azure DevOps organization, project, and personal access token
organization = 'microsoftdigitallearning'
project = 'Courseware'
team = 'Courseware Team'
# take from Github Secrets, need to be renewed every 7 days
personal_access_token = os.getenv('ADO_PAT')

# variable to keep all work item templates with following fields: name, template_url, course_indentifier
work_item_templates = []

# Encode the PAT in base64
encoded_pat = base64.b64encode(f':{personal_access_token}'.encode()).decode()

# Azure DevOps REST API URL for work item templates
url = f'https://{organization}.visualstudio.com/{project}/{team}/_apis/wit/templates?api-version=6.0'

# Set up the headers with the encoded PAT
headers = {
    'Authorization': f'Basic {encoded_pat}',
    'Content-Type': 'application/json'
}

# Make the request to the Azure DevOps REST API
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    templates = response.json()['value']
    for template in templates:
        # if "workItemTypeName" is "SE Bug"
        if template['workItemTypeName'] == "SE Bug":
            print(f"Template Name: {template['name']}")
            # print(f"Template URL: {template['url']}")
            # get the identifier on the URL (between /courseware and /_apis)
            identifier = template['url'].split('/Courseware/')[1].split('/_apis')[0]
            template_link = "https://microsoftdigitallearning.visualstudio.com/Courseware/_workitems/create/SE%20Bug?templateId=" + identifier
            print(f"Template Link: {template_link}")
            # Do a request to the "url" and get field "Custom.CourseIdentifier" under fields
            response = requests.get(template['url'], headers=headers)
            if response.status_code == 200:
                fields = response.json().get('fields', {})
                course_identifier = fields.get('Custom.CourseIdentifier', 'N/A')
                print(f"Course Identifier: {course_identifier}")
                course_identifier = course_identifier.replace(" ", "%20")
                work_item_templates.append({
                    'name': template['name'],
                    'template_url': template_link,
                    'course_identifier': course_identifier
                })

            else:
                print(f"Failed to get fields : {response.status_code}")
                print(response.json())
else:
    print(f"Failed to get templates : {response.status_code}")
    print(response.json())

# Print the work item templates
print(work_item_templates)
 
