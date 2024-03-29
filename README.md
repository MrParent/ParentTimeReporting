This is for you whom do not like to spend time on reporting time in Maconomy and in Jira. You are also a user of Toggl or Optimize(old timer program).

For this to work, you will need to specify what company you have (to build the URL for pushing time logs on tickets) and you will need to specify the Maconomy prod (also to build the Maconomy URL for your company).
This can be done with the settings button in the program.

For Jira to work (because of advanced auth not implemented and convenience), you will have to add an API key and a username inside of your environment variables, like so:
```
JIRA_API_KEY: value
```
```
JIRA_USER_NAME: value
```
For toggl to be even faster (without login) then add an API key for that one too, like this:
```
TOGGL_API_KEY: value
```
For Maconomy to work, you will have to add a config.json file. This is due to long names in Maconomy, to map job numbers and because you don't want to clutter your timer program with too much stuff.
This config.json file, that you have to have in the same folder as the program, is specified like so:
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
If you use Optimize, you will have to write the description for a task in the form: Client;Task;Description
You also have to select the OptTimes.txt file that optimize generates when prompted for a file.

Special thanks to Guppan for making this possible and for solving a lot of the issues regarding pushing time rows to Maconomy.
