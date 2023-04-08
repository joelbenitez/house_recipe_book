# 🧐 Project summary

A band-aid held project for managing the house menu system and grocery list. You can configure multiple actions based on your needs. 

* Send emails when the menu is built
* Send Slack messages n-days in advance for taking meat out of the freezer
* Many things I tried and forgot they existed


# 👨‍💻 Tech stack

Here's a brief high-level overview of the tech stack the project uses:

* Django as web framework
* PostgreSQL as database 
* Asana's REST API to manage the menu schedule and grocery list
* GMail as SMTP server
* Slack webhooks for posting messages

# ✍️ Contributing

Interested in contributing? Please do, anything is welcome as this is not maintained at all

# 🌟 How-Tos

Django will need you to set environment variables to manage it all in `settings.py`. Examples:

* `DJANGO_SECRET`
* `POSTGRESQL_USER`
* `POSTGRESQL_PASS`
* Host and port for the database connection
* `EMAIL_USER`
* `EMAIL_PASS`