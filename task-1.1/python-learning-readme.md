# Python Learning Project

## Environment Setup

### Python Installation
- Installed Python 3.8.7
- Verified installation using `python --version`

### Virtual Environment
1. Created virtual environment named "cf-python-base"
```bash
python -m venv cf-python-base
```

2. Created second virtual environment "cf-python-copy" for requirements testing
```bash
python -m venv cf-python-copy
```

### Development Environment
- Installed Visual Studio Code as the primary code editor
- Created initial script `add.py` for basic number addition

## Project Structure

```
├── Exercise 1.1/
│   ├── add.py
│   └── requirements.txt
├── README.md
```

## Scripts

### add.py
A simple Python script that:
- Takes two numbers as user input
- Adds them together
- Displays the result

Example usage:
```python
Enter first number: 5
Enter second number: 3
Result: 8
```

## Package Management

### Installed Packages
- IPython shell for enhanced Python REPL experience
- Additional dependencies as listed in requirements.txt

### Requirements File
- Generated using `pip freeze > requirements.txt`
- Successfully tested package installation in secondary environment using:
```bash
pip install -r requirements.txt
```

## Development Tools

### IPython Shell
- Installed and configured IPython for enhanced development experience
- Features include:
  - Syntax highlighting
  - Auto-indentation
  - Auto-completion

## Version Control

### GitHub Repository
- Created dedicated repository for course work
- Organized with separate folders for each exercise
- All exercise deliverables stored in respective folders

## Getting Started

1. Clone the repository
```bash
git clone [repository-url]
```

2. Create and activate virtual environment
```bash
python -m venv cf-python-base
source cf-python-base/bin/activate  # On Unix/macOS
cf-python-base\Scripts\activate     # On Windows
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Run the sample script
```bash
python add.py
```

## Maintenance

This repository will be continuously updated throughout the course with new exercises and projects. Each exercise will be stored in its own dedicated folder for clear organization.

