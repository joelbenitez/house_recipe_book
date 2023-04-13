from datetime import date, timedelta

import asana
import pymongo
import requests
from requests.structures import CaseInsensitiveDict
import psycopg2

from ChewieBot import get_asana_calendar
from config import asana_token, grocery_project_gid, mongo_db_host, slack_url_post
from mongo_db_actions import get_collection, get_db, get_one_item


def get_sections():
    """Queries Asana for updated items and stores them in a dictionary"""
    client = asana.Client.access_token(asana_token)

    result = client.sections.get_sections_for_project(
        grocery_project_gid, {"param": "value", "param": "value"}, opt_pretty=True
    )

    for item in result:
        if item["name"] == "Wegmans":
            wegmans_gid = item["gid"]
    return wegmans_gid


def get_items_for_section(wegmans_gid):
    """Queries Asana for updated items and stores them in a dictionary"""
    client = asana.Client.access_token(asana_token)
    section_gid = wegmans_gid

    result = client.tasks.get_tasks_for_section(
        section_gid,
        opt_fields=[
            "name",
            "completed",
        ],
        opt_pretty=True,
    )

    for item in result:
        if item["completed"] is False:
            print(item)


def create_task(task_name, wegmans_gid):
    """Queries Asana for updated items and stores them in a dictionary"""
    client = asana.Client.access_token(asana_token)

    workspace_gid = "wegmans_gid"
    section_gid = wegmans_gid

    client.tasks.create_in_workspace(
        workspace_gid,
        {
            "name": task_name,
            "memberships": [
                {
                    "project": grocery_project_gid,
                    "section": section_gid,
                }
            ],
        },
    )


def get_menu_items_week():
    # This will run on a Saturday so it will get menu items from Sat - Fri
    MenuList = get_asana_calendar()

    mydate = date.today()
    weekly_menu = []
    for i in range(0, 7):
        targetDate = mydate + timedelta(days=i)
        try:
            if MenuList[targetDate.isoformat()] == "Takeout" or MenuList[targetDate.isoformat()] == "Surf-and-turf":
                pass
            else:
                weekly_menu.append(MenuList[targetDate.isoformat()])
        except KeyError as e:
            print(f"Nothing in the menu for {e}")

    return weekly_menu


def main():
    weekly_menu = get_menu_items_week()

    master_ingredient_list = []

    connection = psycopg2.connect(
        user="db_admin_user",
        password="db_admin_password",
        host="localhost",
        port="5432",
        database="blog",
    )
    cursor = connection.cursor()

    for menu_item in weekly_menu:
        postgreSQL_select_Query = (
            f"select * from blog_recipe where title = '{menu_item}' "
        )

        cursor.execute(postgreSQL_select_Query)
        recipe_records = cursor.fetchall()

        for row in recipe_records:
            master_ingredient_list += row[2].split(",")

    cursor.close()
    connection.close()

    wegmans_gid = get_sections()

    for item in sorted(master_ingredient_list):
        create_task(item, wegmans_gid=wegmans_gid)


if __name__ == "__main__":
    main()
    # Posting to Slack
    url = slack_url_post

    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"

    data = {}
    data["text"] = "Grocery list items have been posted in Asana"
    resp = requests.post(url, headers=headers, data=str(data))