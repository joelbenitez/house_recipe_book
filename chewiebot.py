import calendar
from datetime import date, timedelta

import asana
import requests
from requests.structures import CaseInsensitiveDict

from config import asana_token, project_gid, slack_url_post

url = slack_url_post

headers = CaseInsensitiveDict()
headers["Content-Type"] = "application/json"


def get_asana_calendar():
    """Queries Asana for updated items and stores them in a dictionary"""
    Token = asana_token
    client = asana.Client.access_token(Token)

    result = client.tasks.get_tasks_for_project(
        project_gid,
        opt_fields=[
            "due_on",
            "name",
            "completed",
        ],
        opt_pretty=True,
    )

    MenuDict = {}

    for item in result:
        if item["completed"] is False:
            MenuDict[item["due_on"]] = item["name"]

    return MenuDict


def main():

    MenuList = get_asana_calendar()

    mydate = date.today()
    try:
        day = calendar.day_name[mydate.weekday() + 2]
    except IndexError:
        if calendar.day_name[mydate.weekday()] == "Saturday":
            day = "Monday"
        elif calendar.day_name[mydate.weekday()] == "Sunday":
            day = "Tuesday"
    targetDate = mydate + timedelta(days=2)

    # Post the day + 2 menu item in Slack in order to take the meat out of the freezer
    data = {}
    try:
        data["text"] = f"The item for {day} is: {MenuList[targetDate.isoformat()]}"
    except KeyError:
        data["text"] = f"There is no item in the calendar for {day}"


    # Posting to Slack
    requests.post(url, headers=headers, data=str(data))


if __name__ == "__main__":
    main()