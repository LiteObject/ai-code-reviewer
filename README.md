# AI Code Reviewer

An intelligent code review tool that leverages AI models to analyze code files and provide detailed feedback, suggestions, and improvements. The tool integrates with GitHub APIs to review pull requests and can analyze local code files.

## Features

- **AI-Powered Code Reviews**: Uses Ollama with Llama3 model for intelligent code analysis
- **Multiple Language Support**: Supports Python, TypeScript, JavaScript, and JSX files
- **GitHub Integration**: Can analyze GitHub pull requests and commits
- **Batch Processing**: Review entire directories with exclude filters
- **Markdown Reports**: Generates detailed review reports in markdown format
- **Customizable Prompts**: Structured prompt templates for consistent review quality

## Prerequisites

- Python 3.11+
- [Ollama](https://ollama.ai/) installed and running locally
- Llama3 model pulled in Ollama (`ollama pull llama3`)
- GitHub Personal Access Token (for GitHub integration)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/LiteObject/ai-code-reviewer.git
cd ai-code-reviewer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
# Create .env file
echo "GITHUB_TOKEN=your_github_token_here" > .env
```

4. Ensure Ollama is running:
```bash
ollama serve
```

## Usage

### Review Local Files

```python
from reviewer import review_file, review_files

# Review a single file
review_file("path/to/your/file.py")

# Review all files in a directory
exclude_keywords = ["venv", "node_modules", "__pycache__"]
review_files("path/to/directory", exclude_keywords)
```

### GitHub Integration

```python
import git_client as git

# Get pull request data
pr_data = git.get_pull_request_data(token, owner, repo, pull_number)

# Get pull request changes
pr_changes = git.get_pull_request_changes(token, owner, repo, pull_number)
```

### Run the Main Application

```bash
python app.py
```

## Project Structure

```
ai-code-reviewer/
├── app.py                 # Main application entry point
├── reviewer.py            # Core review logic using LangChain
├── git_client.py          # GitHub API integration
├── file_helper.py         # File operations utilities
├── test_git_client.py     # Manual testing script
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (create this)
├── reviews/              # Generated review reports
│   ├── REVIEW_*_BY_llama3.md
└── test_files/           # Sample files for testing
    ├── bad_code_examples.py
    └── delete_folders.py
```

## Configuration

### Supported File Extensions
- `.py` (Python)
- `.ts` (TypeScript)
- `.js` (JavaScript)
- `.jsx` (React JSX)

### Exclude Keywords
Configure which directories/files to skip during batch processing:
```python
exclude_keywords = ["venv", "Python311", "node_modules", "__pycache__"]
```

### Ollama Configuration
The tool uses Ollama running on `http://localhost:11434` with the `llama3` model. You can modify these settings in `reviewer.py`:

```python
llm = Ollama(
    base_url='http://localhost:11434',
    model="llama3"
)
```

## Review Output

Reviews are saved in the `reviews/` directory with the format:
```
REVIEW_{filename}_BY_{model}.md
```

Each review includes:
- Code analysis summary
- Specific recommendations with before/after code examples
- Complete revised code when necessary
- Markdown formatting for easy reading

## API Functions

### Core Review Functions
- `review_file(file_path)` - Review a single file
- `review_files(folder_path, exclude_keywords)` - Review multiple files
- `get_code_review(filename, code)` - Generate AI review for code

### GitHub Integration
- `get_pull_request_data(token, owner, repo, pull_number)`
- `get_pull_request_changes(token, owner, repo, pull_number)`
- `get_commit_messages(token, owner, repo, pull_number)`

### File Operations
- `create_file(filename, content)` - Create new file
- `append_to_file(filename, content)` - Append to existing file

## Dependencies

Key dependencies include:
- `langchain` - AI model integration
- `requests` - HTTP requests for GitHub API
- `python-dotenv` - Environment variable management
- `pydantic` - Data validation

See `requirements.txt` for complete list.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source. Please check the repository for license details.
