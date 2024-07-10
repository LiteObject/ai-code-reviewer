import requests
import git_client as git
import file_helper as file_helper
import reviewer as reviewer
import datetime
from pprint import pprint
import os
from dotenv import load_dotenv
load_dotenv()

if __name__ == "__main__":    

    if not os.getenv('GITHUB_TOKEN'):
        os.environ['GITHUB_TOKEN'] = input("Enter your Github token: ")
    else:
        token = os.environ.get("GITHUB_TOKEN")

    # if not token:
    #     raise ValueError("GITHUB_TOKEN environment variable is not set")

    owner = "LiteObject"
    repo = "react-testing-with-cypress"
    pull_number = 8

    ## Specify the keywords to exclude files
    exclude_keywords = ["venv", "Python311", "node_modules"] 

    try:       
        # pr_data = git.get_pull_request_data(token, owner, repo, pull_number)        
                
        ## Specify the folder path containing the code files
        folder_path = "C:/tmp"
        reviewer.review_files(folder_path, exclude_keywords)

        # while True:
        #     choice = input("Enter 'f' to review a single file or 'd' to review all files in a folder: ")
            
        #     if choice.lower() == 'f':
        #         file_path = input("Enter the file path: ")
        #         if os.path.exists(file_path) and os.path.isfile(file_path):
        #             reviewer.review_file(file_path)
        #             break
        #         else:
        #             print("Invalid file path. Please try again.")
            
        #     elif choice.lower() == 'd':
        #         folder_path = input("Enter the folder path: ")
        #         if os.path.exists(folder_path) and os.path.isdir(folder_path):
        #             reviewer.review_files(folder_path, exclude_keywords)
        #             break
        #         else:
        #             print("Invalid folder path. Please try again.")
            
        #     else:
        #         print("Invalid choice. Please try again.")
        

        # pr_changes = git.get_pull_request_changes(token, owner, repo, pull_number)
        # reviewer.get_code_review("react-testing-with-cypress_pr_6", pr_changes)
    except Exception as e:
        print(f"Error: {e}")