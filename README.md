This is for you whom do not like to spend time on reporting time in Maconomy and in Jira. You are also a user of Toggl or another timer program (that might be supported in the future).

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
    "spec3": "ROLEYOUHAVE"
  },
  "definitions": [
    {
      "local-job": "JOBNAMEYOUWANTTOSPECIFYINTOGGLASCUSTOMER1",
      "remote-job": "JOBNRINMACONOMY1",
      "spec3": "OTHERROLETHANDEFAULT",
      "tasks": [
        {
          "local-task": "TASKNAMEYOUWANTTOSPECINTOGGLASPROJECT1",
          "remote-task": "TASKNAMEINMACONOMY1"
        },
        {
          "local-task": "TASKNAMEYOUWANTTOSPECINTOGGLASPROJECT2",
          "remote-task": "TASKNAMEINMACONOMY2"
        }
      ]
    },
	{
      "local-job": "JOBNAMEYOUWANTTOSPECIFYINTOGGLASCUSTOMER2",
      "remote-job": "JOBNRINMACONOMY2",
      "tasks": [
        {
          "local-task": "TASKNAMEYOUWANTTOSPECINTOGGLASPROJECT2",
          "remote-task": "TASKNAMEINMACONOMY2"
        }
      ]
    }
  ]
}
```
Special thanks to Guppan for making this possible and for solving a lot of the issues regarding pushing time rows to Maconomy.
