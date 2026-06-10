# 🚀 IDE Setup and Configuration 

<div align="center">

![VS Code](https://img.shields.io/badge/VS_Code-007ACC?style=for-the-badge\&logo=visualstudiocode\&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge\&logo=python\&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-Ubuntu-E95420?style=for-the-badge\&logo=ubuntu\&logoColor=white)
![Pylint](https://img.shields.io/badge/Pylint-Linting-yellow?style=for-the-badge)
![Black](https://img.shields.io/badge/Black-Formatter-black?style=for-the-badge)
![Pytest](https://img.shields.io/badge/Pytest-Testing-green?style=for-the-badge)

</div>

---

# 📚 Overview

This lab guides you through setting up a professional Python development environment using **Visual Studio Code**, **Python Virtual Environments**, **Debugging Tools**, and **Productivity Extensions**.

---

# 🎯 Learning Objectives

By completing this lab, you will:

* ✅ Install and configure VS Code
* ✅ Install essential Python extensions
* ✅ Create Python virtual environments
* ✅ Configure workspace settings
* ✅ Set up debugging configurations
* ✅ Improve Python development productivity

---

# 📋 Prerequisites

* Basic Linux command-line knowledge
* Understanding of Python fundamentals
* Familiarity with package management
* Basic understanding of file paths

---

# 🖥️ Environment Setup

You will use the bare-metal Linux machine provided by Al Nafi.

---

# 🛠️ Task 1: Install VS Code and Essential Extensions

## 🔹 Step 1: Install VS Code

```bash
# Update package list
sudo apt update

# Install dependencies
sudo apt install -y wget gpg apt-transport-https

# Add Microsoft GPG key and repository
wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg

sudo install -o root -g root -m 644 packages.microsoft.gpg \
/etc/apt/trusted.gpg.d/

sudo sh -c 'echo "deb [arch=amd64] https://packages.microsoft.com/repos/code stable main" > /etc/apt/sources.list.d/vscode.list'

# Install VS Code
sudo apt update
sudo apt install -y code

# Verify installation
code --version
```

### ✅ Expected Result

VS Code is successfully installed.

---

## 🔹 Step 2: Launch VS Code

```bash
code . &
```

> 💡 On headless servers use VS Code Server or X11 Forwarding.

---

## 🔹 Step 3: Install Python Extensions

```bash
# Python Extension
code --install-extension ms-python.python

# Pylance
code --install-extension ms-python.vscode-pylance

# Debugger
code --install-extension ms-python.debugpy

# Formatter
code --install-extension ms-python.black-formatter

# Jupyter Support
code --install-extension ms-toolsai.jupyter

# Verify
code --list-extensions
```

### 🎉 Installed Extensions

| Extension       | Purpose             |
| --------------- | ------------------- |
| Python          | Core Python Support |
| Pylance         | IntelliSense        |
| DebugPy         | Debugging           |
| Black Formatter | Code Formatting     |
| Jupyter         | Notebook Support    |

---

## 🔹 Step 4: Create Workspace Configuration

```bash
mkdir -p ~/python-workspace
cd ~/python-workspace

mkdir -p .vscode
```

Create `.vscode/settings.json`

```json
{
    "python.defaultInterpreterPath": "${workspaceFolder}/venv/bin/python",
    "python.formatting.provider": "black",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "editor.formatOnSave": true,
    "editor.rulers": [88],
    "files.autoSave": "afterDelay",
    "files.autoSaveDelay": 1000
}
```

---

# 🐍 Task 2: Setup Virtual Environment and Debugger

## 🔹 Step 1: Install Python Tools

```bash
sudo apt install -y python3 python3-pip python3-venv

python3 --version
pip3 --version
```

---

## 🔹 Step 2: Create Virtual Environment

```bash
cd ~/python-workspace

python3 -m venv venv

source venv/bin/activate

which python
```

### ✅ Expected Output

```text
/home/user/python-workspace/venv/bin/python
```

---

## 🔹 Step 3: Install Development Dependencies

```bash
pip install --upgrade pip

pip install pylint black pytest ipython

pip freeze > requirements.txt

pip list
```

---

## 🔹 Step 4: Create Sample Python Application

Create `app.py`

```python
def calculate_factorial(n: int) -> int:
    if n == 0 or n == 1:
        return 1

    result = 1

    for i in range(2, n + 1):
        result *= i

    return result


def process_numbers(numbers: list) -> dict:

    stats = {
        "sum": 0,
        "average": 0.0,
        "factorials": {}
    }

    return stats


def main():

    test_numbers = [3, 5, 7, 2]

    print("Testing factorial calculation:")

    for num in test_numbers:
        result = calculate_factorial(num)
        print(f"Factorial of {num} is {result}")

    print("\nProcessing numbers:")

    stats = process_numbers(test_numbers)

    print(f"Statistics: {stats}")


if __name__ == "__main__":
    main()
```

---

## 🔹 Step 5: Configure Debugger

Create `.vscode/launch.json`

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Current File",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
            "justMyCode": true
        },
        {
            "name": "Python: Debug App",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/app.py",
            "console": "integratedTerminal"
        }
    ]
}
```

---

## 🔹 Step 6: Test Debugging

```bash
python -m pdb app.py
```

### Useful PDB Commands

| Command | Description    |
| ------- | -------------- |
| l       | List Code      |
| n       | Next Line      |
| s       | Step Into      |
| c       | Continue       |
| b       | Set Breakpoint |
| p       | Print Variable |
| q       | Quit           |

---

## 🔹 Step 7: Create Debug Helper Script

Create `debug_helper.py`

```python
import pdb

def debug_function(func):

    def wrapper(*args, **kwargs):
        print(f"Debugging {func.__name__}")
        pdb.set_trace()
        return func(*args, **kwargs)

    return wrapper


def conditional_breakpoint(condition, message=""):
    pass


class DebugContext:

    def __init__(self, description):
        self.description = description

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
```

---

## 🔹 Step 8: Create Tasks Configuration

Create `.vscode/tasks.json`

```json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "Run Python File",
            "type": "shell",
            "command": "${workspaceFolder}/venv/bin/python",
            "args": ["${file}"]
        },
        {
            "label": "Run Tests",
            "type": "shell",
            "command": "${workspaceFolder}/venv/bin/pytest",
            "args": ["-v"]
        }
    ]
}
```

---

# ✅ Verification

## Verify VS Code

```bash
code --version

code --list-extensions | grep python
```

---

## Verify Virtual Environment

```bash
source venv/bin/activate

which python

pip list | grep -E "pylint|black|pytest"
```

---

## Test Application

```bash
python app.py
```

Expected:

```text
Testing factorial calculation:
Factorial of 3 is 6
Factorial of 5 is 120
Factorial of 7 is 5040
Factorial of 2 is 2

Processing numbers:
Statistics: {'sum': 0, 'average': 0.0, 'factorials': {}}
```

---

# 🛠️ Troubleshooting

## VS Code Installation Issues

```bash
curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > microsoft.gpg

sudo mv microsoft.gpg \
/etc/apt/trusted.gpg.d/microsoft.gpg

sudo apt clean
sudo apt update
```

---

## Virtual Environment Issues

```bash
python3 -m venv --clear venv

chmod +x venv/bin/activate
```

---

## Extension Issues

```bash
code --install-extension ms-python.python --force

ls ~/.vscode/extensions/
```

---

# 🎯 Challenge Tasks

* Complete `process_numbers()`
* Implement `conditional_breakpoint()`
* Implement `DebugContext`
* Create `test_app.py`
* Add VS Code snippets
* Run automated tests

---

# 🏆 Lab Achievements

✅ Installed VS Code

✅ Configured Python Extensions

✅ Created Virtual Environment

✅ Configured Debugger

✅ Created Workspace Settings

✅ Set Up Productivity Tasks

---

# 🎓 Conclusion

You have successfully built a professional Python development environment using VS Code, Virtual Environments, Debugging Tools, and Productivity Extensions. These skills are fundamental for modern Python development and provide a strong foundation for larger software engineering projects.

### 🚀 Next Steps

* Practice breakpoints and debugging
* Explore additional VS Code extensions
* Configure Git integration
* Build automated testing workflows
* Customize your Python development environment

**Happy Coding! 🐍✨**
