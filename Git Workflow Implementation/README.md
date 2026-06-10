# 🚀 Git Workflow Implementation 

![Git](https://img.shields.io/badge/Git-Version_Control-F05032?style=for-the-badge\&logo=git\&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-Ubuntu-E95420?style=for-the-badge\&logo=ubuntu\&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge\&logo=python\&logoColor=white)
![Workflow](https://img.shields.io/badge/Workflow-Feature_Branch-blue?style=for-the-badge)
![Status](https://img.shields.io/badge/Lab-Completed-success?style=for-the-badge)

---

# 📚 Git Workflow Implementation

This hands-on lab demonstrates a professional Git workflow used in real-world software development teams. You will learn how to create repositories, work with feature branches, perform merges, resolve conflicts, simulate pull requests, conduct code reviews, and maintain a clean repository history.

---

# 🎯 Learning Objectives

By the end of this lab, you will be able to:

* ✅ Initialize and configure a Git repository
* ✅ Implement a feature branch workflow
* ✅ Create and manage multiple branches
* ✅ Merge branches and resolve conflicts
* ✅ Simulate a pull request workflow
* ✅ Apply professional Git collaboration practices

---

# 📋 Prerequisites

* Basic Linux command line knowledge
* Understanding of file system navigation
* Familiarity with text editors (`nano`, `vim`, `vi`)
* Basic understanding of version control concepts
* Completed introductory Git tutorial or equivalent experience

---

# 🛠️ Environment Setup

## Install Git

```bash
# Update package manager
sudo apt update

# Install Git
sudo apt install git -y

# Verify installation
git --version
```

---

## Configure Git Identity

```bash
# Set your name and email
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Verify configuration
git config --global --list
```

---

# 🚀 Task 1: Initialize Repository and Create Feature Branches

---

## 🔹 Step 1: Create Project Structure

```bash
# Create project directory
mkdir ~/ecommerce-app
cd ~/ecommerce-app

# Initialize Git repository
git init

# Create initial project files
touch README.md
echo "# E-Commerce Application" > README.md
echo "A simple product catalog system" >> README.md
```

---

## 🔹 Step 2: Create Initial Commit

### Create Main Application File

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

Save as:

```text
app.py
```

### Commit Initial Files

```bash
git add README.md app.py
git commit -m "Initial commit: Add README and main application file"

git log --oneline
```

---

## 🔹 Step 3: Create Feature Branches

### 🌿 Product Search Feature Branch

```bash
git checkout -b feature/product-search
```

Create `search.py`

```python
#!/usr/bin/env python3
"""
Product Search Module
TODO: Implement search algorithms
"""

class ProductSearch:
    def __init__(self):
        self.products = []

    def search_by_name(self, query):
        """
        Search products by name

        Args:
            query: Search term

        Returns:
            List of matching products
        """
        # TODO: Implement search logic
        pass

    def search_by_category(self, category):
        """
        Search products by category

        Args:
            category: Product category

        Returns:
            List of products in category
        """
        # TODO: Implement category filter
        pass

if __name__ == "__main__":
    searcher = ProductSearch()
    print("Product Search Module Loaded")
```

Commit Search Feature

```bash
git add search.py
git commit -m "Add product search module with search methods"
```

---

### 🌿 Shopping Cart Feature Branch

```bash
git checkout main
git checkout -b feature/shopping-cart
```

Create `cart.py`

```python
#!/usr/bin/env python3
"""
Shopping Cart Module
TODO: Implement cart operations
"""

class ShoppingCart:
    def __init__(self):
        self.items = []
        self.total = 0.0

    def add_item(self, product_id, quantity, price):
        """
        Add item to cart

        Args:
            product_id: Unique product identifier
            quantity: Number of items
            price: Price per item
        """
        pass

    def remove_item(self, product_id):
        """
        Remove item from cart

        Args:
            product_id: Product to remove
        """
        pass

    def calculate_total(self):
        """Calculate cart total"""
        pass

if __name__ == "__main__":
    cart = ShoppingCart()
    print("Shopping Cart Module Loaded")
```

Commit Shopping Cart Feature

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

---

# 🔀 Task 2: Merge Branches and Resolve Conflicts

---

## 🔹 Step 1: Merge First Feature

```bash
git checkout main

git merge feature/product-search \
-m "Merge feature/product-search into main"

git log --oneline -n 3

ls -la
```

---

## 🔹 Step 2: Create Conflicting Changes

### Modify app.py on Main Branch

```python
#!/usr/bin/env python3
"""
E-Commerce Product Catalog
Main application entry point
"""

from search import ProductSearch

def main():
    print("E-Commerce Application v1.0")
    print("Product Catalog System")

    searcher = ProductSearch()
    print("Search module initialized")

if __name__ == "__main__":
    main()
```

Commit:

```bash
git add app.py
git commit -m "Integrate search module into main app"
```

---

### Modify app.py on Shopping Cart Branch

```bash
git checkout feature/shopping-cart
```

Replace `app.py`

```python
#!/usr/bin/env python3
"""
E-Commerce Product Catalog
Main application entry point
"""

from cart import ShoppingCart

def main():
    print("E-Commerce Application v1.0")
    print("Product Catalog System")

    cart = ShoppingCart()
    print("Shopping cart initialized")

if __name__ == "__main__":
    main()
```

Commit:

```bash
git add app.py
git commit -m "Integrate shopping cart into main app"
```

---

## 🔹 Step 3: Merge and Trigger Conflict

```bash
git checkout main

git merge feature/shopping-cart

git status

cat app.py
```

---

## 🔹 Step 4: Resolve Conflict

Replace with:

```python
#!/usr/bin/env python3
"""
E-Commerce Product Catalog
Main application entry point
"""

from search import ProductSearch
from cart import ShoppingCart

def main():
    print("E-Commerce Application v1.0")
    print("Product Catalog System")

    searcher = ProductSearch()
    print("Search module initialized")

    cart = ShoppingCart()
    print("Shopping cart initialized")

if __name__ == "__main__":
    main()
```

Complete Merge

```bash
git add app.py

git commit \
-m "Merge feature/shopping-cart with conflict resolution"

git log --oneline --graph -n 5
```

---

# 🔍 Task 3: Implement Pull Request Workflow

---

## 🔹 Step 1: Create Authentication Feature

```bash
git checkout -b feature/user-authentication
```

Create `auth.py`

```python
#!/usr/bin/env python3
"""
User Authentication Module
Simulates PR workflow
"""

class UserAuth:
    def __init__(self):
        self.users = {}

    def register_user(self, username, password):
        pass

    def login(self, username, password):
        pass

if __name__ == "__main__":
    auth = UserAuth()
    print("Authentication Module Loaded")
```

Commit:

```bash
git add auth.py

git commit -m "Add user authentication module"
```

---

## 🔹 Step 2: Simulate Code Review

Create `REVIEW_NOTES.md`

```markdown
# Code Review for feature/user-authentication

## Reviewer Comments:

- [ ] Add input validation for username
- [ ] Implement password strength requirements
- [ ] Add error handling for duplicate users
- [ ] Include unit tests

## Status: Changes Requested
```

Commit

```bash
git add REVIEW_NOTES.md

git commit -m "Add code review notes"
```

---

### Improved auth.py After Review

```python
#!/usr/bin/env python3
"""
User Authentication Module
Updated based on code review
"""

class UserAuth:
    def __init__(self):
        self.users = {}

    def validate_username(self, username):
        if len(username) < 3:
            return False, "Username must be at least 3 characters"
        return True, "Valid"

    def validate_password(self, password):
        if len(password) < 8:
            return False, "Password must be at least 8 characters"
        return True, "Valid"

    def register_user(self, username, password):

        valid, msg = self.validate_username(username)
        if not valid:
            return False, msg

        valid, msg = self.validate_password(password)
        if not valid:
            return False, msg

        if username in self.users:
            return False, "Username already exists"

        self.users[username] = password
        return True, "User registered successfully"

    def login(self, username, password):

        if username not in self.users:
            return False, "User not found"

        if self.users[username] == password:
            return True, "Login successful"

        return False, "Invalid password"

if __name__ == "__main__":
    auth = UserAuth()
    print("Authentication Module Loaded")
```

Commit Improvements

```bash
git add auth.py

git commit \
-m "Address code review feedback: Add validation and error handling"
```

---

## 🔹 Step 3: Approve and Merge

Update Review Notes

```markdown
# Code Review for feature/user-authentication

## Reviewer Comments:

- [x] Add input validation for username
- [x] Implement password strength requirements
- [x] Add error handling for duplicate users
- [ ] Include unit tests (deferred)

## Status: Approved for Merge
```

Commit

```bash
git add REVIEW_NOTES.md

git commit -m "Update review status: Approved"
```

Merge

```bash
git checkout main

git merge feature/user-authentication \
-m "Merge feature/user-authentication after code review"
```

---

## 🔹 Step 4: Clean Up Branches

```bash
git branch -a

git branch -d feature/product-search

git branch -d feature/shopping-cart

git branch -d feature/user-authentication

git branch
```

---

# ✅ Verification

## Verify Files

```bash
ls -la ~/ecommerce-app
```

Expected:

```text
README.md
app.py
search.py
cart.py
auth.py
REVIEW_NOTES.md
```

---

## Verify Git History

```bash
git log --oneline --all --graph

git branch -a

git log --merges --oneline
```

---

## Verify Main Application

```bash
cat app.py | grep -E "import|Initialize"
```

---

## Verify Validation Functions

```bash
cat auth.py | grep -E "def validate"
```

---

## Run Tests

```bash
python3 search.py

python3 cart.py

python3 auth.py

python3 app.py
```

---

# 🛠️ Troubleshooting

## Merge Conflict Markers

```text
<<<<<<< HEAD
Current branch changes
=======
Incoming branch changes
>>>>>>> branch-name
```

Abort merge

```bash
git merge --abort
```

---

## Reset Last Commit

Keep changes staged

```bash
git reset --soft HEAD~1
```

Keep changes unstaged

```bash
git reset HEAD~1
```

Discard changes

```bash
git reset --hard HEAD~1
```

---

## Force Delete Branch

```bash
git branch -D branch-name
```

Check merged branches

```bash
git branch --merged
```

---

## Current Branch

```bash
git branch --show-current

git branch -v
```

---

# 🏆 Key Takeaways

✅ Feature branches isolate development work

✅ Merge conflicts are normal and manageable

✅ Code reviews improve software quality

✅ Clean commit history improves maintenance

✅ Branch cleanup prevents repository clutter

✅ Professional Git workflows scale team collaboration

---

# 🎓 Conclusion

You have successfully implemented a complete professional Git workflow including repository initialization, feature branch development, merge conflict resolution, code review simulation, pull request workflow, and branch maintenance.

These skills are fundamental for collaborative software development using Git, GitHub, GitLab, Bitbucket, and enterprise DevOps platforms.

### 🚀 Next Steps

* Learn Git Rebase
* Learn Git Cherry-Pick
* Explore Git Hooks
* Work with Remote Repositories
* Practice GitHub Pull Requests
* Integrate Git into CI/CD Pipelines

**Happy Coding and Version Controlling! 🎉**
