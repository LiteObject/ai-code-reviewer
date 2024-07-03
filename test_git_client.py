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
repo = "changelog-with-ai"
pull_number = 6

pr_data = git.get_pull_request_data(token, owner, repo, pull_number)
pprint(pr_data)