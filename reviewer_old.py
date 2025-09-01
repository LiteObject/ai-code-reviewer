import os
import requests
import json
import re

def get_code_review(filename, code):
    url = "http://localhost:11434/api/generate"
    headers = {"Content-Type": "application/json"}
    escaped_code = code.replace('"', '\\"').replace('\n', '\\n')
    data = {
        "model": "llama3",
        "stream": False,
        "prompt": f"Please review the following code, provide suggestions as bullet point list, and examples if needed in markdown format:\n---\n\n\"\"\"\n{escaped_code}\n\"\"\""
    }
    # print(json.dumps(data))
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        try:
            response_json = response.json()
            if "response" in response_json:
                review = response_json["response"].strip()
                save_to_markdown(review, "REVIEW_" + filename + ".md")
                return review
            else:
                print("Error: 'response' key not found in the JSON response")
                return None
        except json.JSONDecodeError:
            print("Error parsing response JSON")
            return None
    else:
        print(f"Request failed with status code: {response.status_code}")
        print(f"Response content: {response.content}")
        return None


def remove_comments(code):
    # Remove single-line comments
    code = re.sub(r'#.*', '', code)
    
    # Remove multi-line comments
    code = re.sub(r'""".*?"""', '', code, flags=re.DOTALL)
    code = re.sub(r"'''.*?'''", '', code, flags=re.DOTALL)
    
    return code

def replace_double_quotes(code):
    # Replace double quotes with single quotes
    code = code.replace('"', "'")
    return code

def remove_extra_whitespace(code):
    # Remove multiple consecutive whitespace characters, including newlines and tabs
    code = re.sub(r'\s+', ' ', code)
    return code

def save_to_markdown(content, file_name):
    with open(file_name, "w") as file:
        file.write(content)
    print(f"Response saved as {file_name}")

def review_code_files(folder_path, exclude_keywords=None):
    if exclude_keywords is None:
        exclude_keywords = []

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".py"):  # Assuming Python files have .py extension
                file_path = os.path.join(root, file)
                
                # Check if the file path contains any of the exclude keywords
                if any(keyword in file_path for keyword in exclude_keywords):
                    continue  # Skip the file if it contains an exclude keyword

                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        code = f.read()
                        # Remove comments from the code
                        code = remove_comments(code)
                        # Replace double quotes with single quotes
                        #code = replace_double_quotes(code)
                        # Remove extra whitespace from the code
                        #code = remove_extra_whitespace(code)

                        # print(f"File Name: {file}")
                        # print(code + "\n\n\n")                        

                        review = get_code_review(file, code)                        
                        if review:
                            lines = review.split("\n")
                            for line in lines:
                                if ":" in line:
                                    line_number, suggestion = line.split(":", 1)
                                    print(f"File: {file}, Line: {line_number.strip()}, Suggestion: {suggestion.strip()}")
                except UnicodeDecodeError:
                    print(f"Skipping file: {file_path} (UnicodeDecodeError)")
                    continue

# Specify the folder path containing the code files
folder_path = "C:/Users/Owner/source/repos/LiteObject/py-tools"

# Call the function to review code files
review_code_files(folder_path)
exclude_keywords = ["venv", "Python311"]  # Specify the keywords to exclude files

review_code_files(folder_path, exclude_keywords)
