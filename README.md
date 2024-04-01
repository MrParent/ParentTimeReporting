This tool is designed for users of Toggl or Optimize who prefer a streamlined process for time reporting in Maconomy and Jira.

To use it, specify your company and Maconomy prod in the settings. These details are used to construct the necessary URLs for logging time on tickets.
You also need to set up a few environment variables and a configuration file:
- For Jira, add your API key and username to your environment variables:
```
JIRA_API_KEY: value
JIRA_USER_NAME: value
```
- For faster Toggl access, add your API key to your environment variables:
```
TOGGL_API_KEY: value
```
- For Maconomy, create a config.json file in the same folder as the program. This file is used to map job numbers and handle long names in Maconomy. Format:
```json
{
  "defaults": {
    "spec3": "ROLE_YOU_HAVE"
  },
  "definitions": [
    {
      "local-job": "JOBNAME_IN_TOGGL_AS_CUSTOMER_1",
      "remote-job": "JOBNR_IN_MACONOMY_1",
      "spec3": "OTHER_ROLE_THAN_DEFAULT_1",
      "tasks": [
        {
          "local-task": "TASKNAME_IN_TOGGL_AS_PROJECT_1",
          "remote-task": "TASKNAME_IN_MACONOMY_1"
        },
        {
          "local-task": "TASKNAME_IN_TOGGL_AS_PROJECT_2",
          "remote-task": "TASKNAME_IN_MACONOMY_2"
        }
      ]
    },
	{
      "local-job": "JOBNAME_IN_TOGGL_AS_CUSTOMER_2",
      "remote-job": "JOBNR_IN_MACONOMY_2",
      "tasks": [
        {
          "local-task": "TASKNAME_IN_TOGGL_AS_PROJECT_2",
          "remote-task": "TASKNAME_IN_MACONOMY_2"
        }
      ]
    }
  ]
}
```
-For Optimize users, task descriptions should be formatted as: Client;Task;Description. Additionally, when prompted, select the OptTimes.txt file generated by Optimize.

Shout out to Guppan for his maconomy project, particularly in resolving issues related to time row pushing to Maconomy.
