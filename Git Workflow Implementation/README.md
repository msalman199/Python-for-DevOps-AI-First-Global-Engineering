# 🚀 Git Workflow Implementation 

<p align="center">

![Git](https://img.shields.io/badge/Git-Version_Control-F05032?style=for-the-badge\&logo=git\&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-Ubuntu-E95420?style=for-the-badge\&logo=ubuntu\&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge\&logo=python\&logoColor=white)
![GitHub Workflow](https://img.shields.io/badge/Workflow-Feature_Branch-blue?style=for-the-badge\&logo=github)
![Status](https://img.shields.io/badge/Lab-Completed-success?style=for-the-badge)

</p>

---

# 📚 Overview

This hands-on lab demonstrates a complete professional Git workflow used by software development teams. You will learn how to initialize repositories, create feature branches, manage parallel development, resolve merge conflicts, simulate pull request reviews, and maintain a clean Git history.

---

# 🎯 Learning Objectives

By completing this lab, you will be able to:

✅ Initialize and configure a Git repository

✅ Create and manage feature branches

✅ Work on multiple development streams simultaneously

✅ Merge branches and resolve conflicts

✅ Simulate Pull Request (PR) workflows

✅ Perform code review processes

✅ Maintain clean repository history

✅ Apply industry-standard Git collaboration practices

---

# 🛠️ Prerequisites

* Basic Linux command line knowledge
* Understanding of file system navigation
* Familiarity with text editors (`nano`, `vim`, `vi`)
* Basic understanding of version control concepts
* Completed introductory Git tutorial

---

# 💻 Environment Setup

## 📦 Install Git

```bash
sudo apt update
sudo apt install git -y
git --version
```

---

## 👤 Configure Git Identity

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

git config --global --list
```

---

# 🏗️ Task 1: Initialize Repository & Create Feature Branches

---

## 🔹 Step 1: Create Project Structure

```bash
mkdir ~/ecommerce-app
cd ~/ecommerce-app

git init

touch README.md

echo "# E-Commerce Application" > README.md
echo "A simple product catalog system" >> README.md
```

### 📌 Result

Repository initialized successfully.

---

## 🔹 Step 2: Create Initial Commit

### Create Main Application

```python
#!/usr/bin/env python3
"""
E-Commerce Product Catalog
Main application entry point
"""

def main():
    print("E-Commerce Application v1.0")
    print("Product Catalog System")

if __name__ == "__main__":
    main()
```

### Commit Changes

```bash
git add README.md app.py
git commit -m "Initial commit: Add README and main application file"
git log --oneline
```

### 📌 Result

Initial project version committed to repository.

---

## 🔹 Step 3: Create Feature Branches

### 🌿 Feature Branch: Product Search

```bash
git checkout -b feature/product-search
```

Create:

```python
search.py
```

Commit:

```bash
git add search.py
git commit -m "Add product search module with search methods"
```

---

### 🌿 Feature Branch: Shopping Cart

```bash
git checkout main
git checkout -b feature/shopping-cart
```

Create:

```python
cart.py
```

Commit:

```bash
git add cart.py
git commit -m "Add shopping cart module with cart operations"
```

---

## 🔹 Step 4: View Branch Structure

```bash
git branch -a

git log --all --graph --oneline --decorate
```

### 📌 Result

Visual representation of repository branches.

---

# 🔀 Task 2: Merge Branches & Resolve Conflicts

---

## 🔹 Step 1: Clean Merge

Switch to main branch:

```bash
git checkout main
```

Merge Product Search Feature:

```bash
git merge feature/product-search \
-m "Merge feature/product-search into main"
```

Verify:

```bash
git log --oneline -n 3
```

### 📌 Result

Search module integrated successfully.

---

## 🔹 Step 2: Create Merge Conflict

### Modify `app.py` on Main Branch

```python
from search import ProductSearch
```

Commit:

```bash
git add app.py
git commit -m "Integrate search module into main app"
```

---

### Modify `app.py` on Shopping Cart Branch

```python
from cart import ShoppingCart
```

Commit:

```bash
git add app.py
git commit -m "Integrate shopping cart into main app"
```

---

## 🔹 Step 3: Trigger Conflict

```bash
git checkout main
git merge feature/shopping-cart
```

Check conflict:

```bash
git status
cat app.py
```

### 📌 Result

Git reports merge conflict.

---

## 🔹 Step 4: Resolve Conflict

Update application:

```python
from search import ProductSearch
from cart import ShoppingCart
```

Stage and commit:

```bash
git add app.py

git commit -m \
"Merge feature/shopping-cart with conflict resolution"
```

Verify:

```bash
git log --oneline --graph -n 5
```

### 📌 Result

Conflict resolved successfully.

---

# 🔍 Task 3: Simulate Pull Request Workflow

---

## 🔹 Step 1: Create Authentication Feature Branch

```bash
git checkout -b feature/user-authentication
```

Create:

```python
auth.py
```

Commit:

```bash
git add auth.py
git commit -m "Add user authentication module"
```

### 📌 Result

Authentication feature created.

---

## 🔹 Step 2: Simulate Code Review

Create Review Notes:

```markdown
# Code Review

- [ ] Add username validation
- [ ] Implement password requirements
- [ ] Add duplicate user handling
- [ ] Include unit tests
```

Commit:

```bash
git add REVIEW_NOTES.md
git commit -m "Add code review notes"
```

---

### 📝 Address Review Feedback

Add:

* Username validation
* Password validation
* Duplicate user checks
* Better error handling

Commit:

```bash
git add auth.py

git commit -m \
"Address code review feedback: Add validation and error handling"
```

### 📌 Result

Feature improved after review process.

---

## 🔹 Step 3: Approve & Merge

Update review status:

```markdown
## Status: Approved for Merge
```

Commit:

```bash
git add REVIEW_NOTES.md
git commit -m "Update review status: Approved"
```

Merge:

```bash
git checkout main

git merge feature/user-authentication \
-m "Merge feature/user-authentication after code review"
```

### 📌 Result

Feature merged after successful review.

---

## 🔹 Step 4: Branch Cleanup

List branches:

```bash
git branch -a
```

Delete merged branches:

```bash
git branch -d feature/product-search

git branch -d feature/shopping-cart

git branch -d feature/user-authentication
```

Verify:

```bash
git branch
```

### 📌 Result

Repository remains clean and organized.

---

# ✅ Verification

---

## 📂 Verify Repository Structure

```bash
ls -la ~/ecommerce-app
```

Expected Files:

```text
README.md
app.py
search.py
cart.py
auth.py
REVIEW_NOTES.md
```

---

## 📜 Verify Git History

```bash
git log --oneline --all --graph
git branch -a
git log --merges --oneline
```

---

## 🔎 Verify Application Integration

```bash
cat app.py | grep -E "import|Initialize"
```

---

## 🔐 Verify Authentication Validation

```bash
cat auth.py | grep -E "def validate"
```

---

## 🧪 Test Modules

```bash
python3 search.py

python3 cart.py

python3 auth.py

python3 app.py
```

---

# 🛠️ Troubleshooting

---

## ⚠️ Merge Conflict Confusion

Conflict markers:

```text
<<<<<<< HEAD
Current branch changes
=======
Incoming branch changes
>>>>>>> branch-name
```

Abort merge:

```bash
git merge --abort
```

---

## ⚠️ Accidentally Committed Conflict Markers

```bash
git reset --soft HEAD~1
```

Fix files and recommit.

---

## ⚠️ Cannot Delete Branch

Check merged branches:

```bash
git branch --merged
```

Force delete:

```bash
git branch -D branch-name
```

---

## ⚠️ Lost Track of Current Branch

```bash
git branch --show-current

git branch -v
```

---

## ⚠️ Committed to Wrong Branch

```bash
git branch new-branch-name

git reset --hard HEAD~1

git checkout new-branch-name
```

---

## ⚠️ Undo Last Commit

Keep staged:

```bash
git reset --soft HEAD~1
```

Keep unstaged:

```bash
git reset HEAD~1
```

Discard completely:

```bash
git reset --hard HEAD~1
```

---

# 🏆 Lab Achievements

After completing this lab, you have successfully implemented:

✅ Repository initialization

✅ Git configuration management

✅ Feature branch workflows

✅ Parallel development strategy

✅ Merge operations

✅ Conflict resolution

✅ Pull Request simulation

✅ Code review lifecycle

✅ Branch cleanup process

✅ Professional Git collaboration practices

---

# 📈 Key Takeaways

### 🌿 Feature Branches

Isolate development work and reduce risk.

### 🔀 Merge Conflicts

Normal part of collaborative development and can be resolved safely.

### 👥 Code Reviews

Improve code quality and maintainability.

### 📝 Clean Commit History

Makes debugging and project maintenance easier.

### 🧹 Branch Management

Prevents repository clutter and confusion.

---

# 🚀 Next Steps

Continue building your Git expertise by learning:

* Interactive Rebase
* Git Cherry-Pick
* Git Stash
* Git Tags
* Git Hooks
* Remote Repositories
* GitHub Pull Requests
* GitLab Merge Requests
* CI/CD Integration
* Git Flow Workflow

---

# 🎓 Conclusion

This lab provided practical experience with modern Git workflows used in professional software development teams. The concepts learned here—branching strategies, merge conflict resolution, pull request reviews, and repository maintenance—form the foundation of collaborative software engineering.

Mastering these workflows prepares you to contribute effectively to real-world projects hosted on GitHub, GitLab, Bitbucket, and enterprise DevOps platforms.

---

### ⭐ Happy Coding & Version Controlling!

**Git Workflow Implementation Lab Complete 🎉**
