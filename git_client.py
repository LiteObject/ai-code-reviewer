import requests

def get_pull_request_data(token: str, owner: str, repo: str, pull_number: int) -> str:
    # Set up the request headers with the access token
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    # Make the API request to get pull request details
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pull_number}"
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Get the pull request data from the response
        pr_data = response.json()

        # Extract the pull request title
        # pr_title = pr_data['title']

        # print(f'Pull Request Title: {pr_title}')
    else:
        print(f"Error: {response.status_code} - {response.text}")

    return pr_data

def get_pull_request_changes(token: str, owner: str, repo: str, pull_number: int) -> str:
    
   # GET /repos/{owner}/{repo}/pulls/{pull_number}/files    
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }

    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pull_number}/files"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return None

    data = response.json()    

    return data

def get_commit_messages(token: str, owner: str, repo: str, pull_number: int) -> list[str]:
        
    # https://docs.github.com/en/rest/pulls/pulls?apiVersion=2022-11-28#list-commits-on-a-pull-request
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pull_number}/commits"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }
    response = requests.get(url, headers=headers)
    commits = response.json()

    commit_messages = []
    for commit in commits:
        # print(commit)
        commit_messages.append(commit["commit"]["message"])

    return commit_messages

def get_commits_for_day(token: str, owner: str, repo: str, day: str, page_size: int) -> list[str]:

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }

    page_size = page_size or 50;

    url = f"https://api.github.com/repos/{owner}/{repo}/commits?since={day}&per_page={page_size}"
    response = requests.get(url, headers=headers)

    # Handle rate limiting
    if response.status_code == 403:
        raise ValueError("GitHub API rate limit exceeded")

    commits = response.json()


    # Extract the commits
    commits = [commit["commit"] for commit in commits]

    # Return the commits
    return commits

def get_file_changes_for_day(token: str, owner: str, repo: str, day: str, page_size: int):

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }

    page_size = page_size or 100;

    url = f"https://api.github.com/repos/{owner}/{repo}/commits?since={day}&per_page={page_size}"
    response = requests.get(url, headers=headers)

    # Handle rate limiting
    if response.status_code == 403:
        raise ValueError("GitHub API rate limit exceeded")
    
    commits = response.json()
    print(commits)

    file_changes = []
    for commit in commits:
        for file in commit['files']:
            print(file, "\n\n")
            if file['status'] == 'A' or file['status'] == 'M' or file['status'] == 'D':
                file_changes.append({
                    'filename': file['filename'],
                    'sha': file['sha'],
                    'change_type': file['status'],
                    'old_sha': file['old_sha'] if file['status'] == 'M' else None,
                    'new_sha': file['new_sha'] if file['status'] == 'M' else None
                })

    return file_changes

def convert_github_pr_url_to_api(url):

  # Check if the URL is valid and has the expected format
  if not url.startswith("https://github.com/") or "/pull/" not in url:
    return None

  # Split the URL into parts
  parts = url.split("/")

  # Extract owner, repo, and pull number
  owner = parts[3]
  repo = parts[4]
  pull_number = parts[6]

  # Construct the API URL
  api_url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pull_number}"

  return api_url
