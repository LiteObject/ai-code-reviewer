import requests
import git_client as git
import file_helper as file_helper
import datetime
import os
from pprint import pprint
from dotenv import load_dotenv
load_dotenv()

token = os.environ.get("GITHUB_TOKEN")
owner = "LiteObject"
repo = "react-testing-with-cypress"
pull_number = 8

# pr_data = git.get_pull_request_data(token, owner, repo, pull_number)
# pprint(pr_data)

pr_changes = git.get_pull_request_changes(token, owner, repo, pull_number)
pprint(pr_changes)