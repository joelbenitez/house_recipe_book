#!/usr/bin/env python3
import calendar
import json
import random
from datetime import date, timedelta
from itertools import islice
from pprint import pprint
import psycopg2

import asana
import pymongo
import requests
from requests.structures import CaseInsensitiveDict

from config import (
    asana_token,
    mongo_db_host,
    project_gid,
    slack_url_post,
    workspace_gid,
)
from mongo_db_actions import get_collection, get_db, read_collection

url = slack_url_post

headers = CaseInsensitiveDict()
headers["Content-Type"] = "application/json"


def AddItemToMenu(workspace_gid, menuitem, due_date, project_gid):
    """Adds menu items to Asana calendar"""
    client = asana.Client.access_token(asana_token)
    result = client.tasks.create_in_workspace(
        workspace_gid,
        {
            "name": menuitem,
            "due_on": due_date,
            "projects": [project_gid],
        },
    )

    pprint(json.dumps(result, indent=4))


if __name__ == "__main__":

    ###Grabbing menu items from PostgreSQL
    connection = psycopg2.connect(
        user="db_admin_user",
        password="db_admin_password",
        host="localhost",
        port="5432",
        database="blog",
    )
    cursor = connection.cursor()
    postgreSQL_select_Query = "select * from blog_post"

    cursor.execute(postgreSQL_select_Query)
    recipe_records = cursor.fetchall()
    full_menu = [row[1] for row in recipe_records]

    cursor.close()
    connection.close()

    #Grabbing a random sample
    suggestions = random.sample(full_menu, 12)

    start_date = date.today() + timedelta(days=1)

    # list of length in which we have to split
    length_to_split = [2, 2, 2, 2, 2, 2]
    Input = iter(suggestions)
    Output = [list(islice(Input, elem)) for elem in length_to_split]

    for item in Output:
        for i in item:
            if calendar.day_name[start_date.weekday()] == "Thursday":
                AddItemToMenu(workspace_gid, "Takeout", str(start_date), project_gid)
                start_date = start_date + timedelta(days=1)
            elif calendar.day_name[start_date.weekday()] == "Friday":
                AddItemToMenu(workspace_gid, "Surf-and-turf", str(start_date), project_gid)
                start_date = start_date + timedelta(days=1)
            else:
                AddItemToMenu(workspace_gid, i, str(start_date), project_gid)
        start_date = start_date + timedelta(days=1)

    # Posting to Slack
    data = {}
    data["text"] = "Suggestions for the menu have been posted in Asana"
    resp = requests.post(url, headers=headers, data=str(data))