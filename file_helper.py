def create_file(filename: str, content: str) -> None:   
    with open(filename, "w", encoding="utf-8") as file:
        file.write(content)

    print(f"\"{filename}\" file created successfully!")

def append_to_file(filename: str, new_content: str):
    existing_content = ""

    # Check if the file exists
    try:
        with open(filename, "r") as file:
            existing_content = file.read()
    except FileNotFoundError:
        pass

    # Write the new changelog content along with the existing content
    with open(filename, "w", encoding="utf-8") as file:
        file.write(new_content)
        file.write(existing_content)