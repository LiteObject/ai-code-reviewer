from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from datetime import datetime
from file_helper import create_file
import re
import os

llm = Ollama(
    # assuming you have Ollama installed and have llama3 model pulled with `ollama pull llama3 `
    model="llama3"
)

supported_extensions = [".py", ".ts", ".js", ".jsx"]

def get_code_review(filename, code) -> None:
    # prompt_template = PromptTemplate.from_template("Please review the following code, provide suggestions as bullet point list, and examples if needed in markdown format:\n---\n\n\"\"\"\n{code}\n\"\"\"")
    
    prompt_template = PromptTemplate.from_template("""
                                                   Carefully review following piece of code and give your recommendations. Your response should include:
                                                    - Code snippets or examples where relevant highlighting the changes.
                                                    - A complete revised version of the code if necessary.
                                                    - Format the response using markdown specification.
                                                    
                                                    {code}
                                                   
                                                    Code Review Template:
                                                   
                                                    ## Code Review Summary:
                                                    - This code snippet is written in...
                                                    - Provide a walk though of the code

                                                    ### Recommendation 1
                                                      Original Code:
                                                      ```
                                                      ```                                                
                                                      Revised Code:
                                                      ```
                                                      ```    
                                                      Provide a short explanation here. 
                                                                                                                                             
                                                    ### Recommendation 2
                                                      Original Code:
                                                      ```
                                                      ```                                                
                                                      Revised Code:
                                                      ```
                                                      ``` 
                                                      Provide a short explanation here.                              

                                                   """)
    escaped_code = code.replace('"', '\\"').replace('\n', '\\n')   
    prompt = prompt_template.invoke({"code": escaped_code})
    # print(prompt)
    review = llm.invoke(prompt)

    review_filename = f"reviews/REVIEW_{remove_file_ext(filename)}_by_{llm.model}.md"
    create_file(review_filename, review)

def remove_comments(code: str) -> str:
    # Remove single-line comments
    code = re.sub(r'#.*', '', code)
    
    # Remove multi-line comments
    code = re.sub(r'""".*?"""', '', code, flags=re.DOTALL)
    code = re.sub(r"'''.*?'''", '', code, flags=re.DOTALL)
    
    return code

def remove_file_ext(filename: str) -> str:
    extension = filename.rsplit('.', 1)[-1]
    filename_without_ext = filename.rsplit('.', 1)[0]
    return filename_without_ext

def review_code_files(folder_path: str, exclude_keywords=None) -> None:
    if exclude_keywords is None:
        exclude_keywords = []

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if any(file.endswith(ext) for ext in supported_extensions):
                file_path = os.path.join(root, file)
                
                # Check if the file path contains any of the exclude keywords
                if any(keyword in file_path for keyword in exclude_keywords):
                    # Skip the file if it contains an exclude keyword
                    continue

                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        code = f.read()
                        # Remove comments from the code
                        code = remove_comments(code)                                          

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