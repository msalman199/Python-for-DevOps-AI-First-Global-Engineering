# 🔐 Role-Based Access Control (RBAC) Simulator

> *"Security is not about giving everyone access—it's about giving the right people the right access at the right time."*

---

![Python](https://img.shields.io/badge/Python-3.6+-blue?style=for-the-badge&logo=python)
![Security](https://img.shields.io/badge/Security-RBAC-red?style=for-the-badge&logo=securityscorecard)
![Access%20Control](https://img.shields.io/badge/Access-Control-green?style=for-the-badge)
![Linux](https://img.shields.io/badge/Linux-Compatible-yellow?style=for-the-badge&logo=linux)
![Authorization](https://img.shields.io/badge/Authorization-Management-purple?style=for-the-badge)

---

# 📖 Overview

The **Role-Based Access Control (RBAC) Simulator** demonstrates how modern authorization systems manage access to protected resources through users, roles, and permissions.

This project helps learners understand:

- 👤 Users
- 🎭 Roles
- 🔑 Permissions
- 📂 Resources
- 🛡️ Access Decisions

The simulator follows the same RBAC concepts used by:

- AWS IAM
- Azure RBAC
- Google Cloud IAM
- Linux Access Controls
- Enterprise Applications
- Database Security Systems

---

# 🎯 Learning Objectives

By completing this lab, you will:

✅ Understand RBAC architecture

✅ Learn how users inherit permissions from roles

✅ Implement access control decisions

✅ Create reusable authorization logic

✅ Simulate real-world permission systems

---

# 🛠️ Prerequisites

- Basic Linux command line knowledge
- Python fundamentals
- Understanding of file permissions
- Python 3.6+ installed

---

# ⚙️ Environment Setup

## Step 1: Verify Python Installation

```bash
python3 --version
```

Expected:

```text
Python 3.6+
```

---

## Step 2: Create Lab Directory

```bash
mkdir ~/rbac-lab
cd ~/rbac-lab
```

---

## Step 3: Create Project Structure

```bash
touch rbac_simulator.py
touch test_rbac.py
```

---

# 🏗️ RBAC Architecture

RBAC contains four major components:

| Component | Description |
|------------|-------------|
| 👤 User | Individual requesting access |
| 🎭 Role | Collection of permissions |
| 🔑 Permission | Action allowed on a resource |
| 📂 Resource | Protected object |

---

# 📁 Project Structure

```text
rbac-lab/
│
├── rbac_simulator.py
├── test_rbac.py
│
└── custom_test.py
```

---

# 🚀 Task 1: Build the RBAC Simulator

---

# 🔑 Permission Class

The Permission class represents an action allowed on a resource.

### Example Permissions

```text
read:document
write:document
delete:document
```

Add to `rbac_simulator.py`

```python
class Permission:
    """
    Represents a single permission in the RBAC system.
    A permission defines an action that can be performed on a resource.
    """

    def __init__(self, action, resource):
        self.action = action
        self.resource = resource

    def __str__(self):
        return f"{self.action}:{self.resource}"

    def __eq__(self, other):
        """Check if two permissions are equal."""
        return (
            self.action == other.action and
            self.resource == other.resource
        )

    def __hash__(self):
        return hash((self.action, self.resource))
```

---

# 🎭 Role Class

Roles group multiple permissions together.

Examples:

- Admin
- Editor
- Viewer

```python
class Role:
    """
    Represents a role in the RBAC system.
    """

    def __init__(self, name):
        self.name = name
        self.permissions = set()

    def add_permission(self, permission):
        self.permissions.add(permission)

    def has_permission(self, permission):
        return permission in self.permissions

    def __str__(self):
        return f"Role: {self.name} ({len(self.permissions)} permissions)"
```

---

# 👤 User Class

Users receive permissions through assigned roles.

```python
class User:
    """
    Represents a user in the RBAC system.
    """

    def __init__(self, username):
        self.username = username
        self.roles = set()

    def assign_role(self, role):
        self.roles.add(role)

    def has_permission(self, permission):

        for role in self.roles:
            if role.has_permission(permission):
                return True

        return False

    def __str__(self):
        return f"User: {self.username} (Roles: {[r.name for r in self.roles]})"
```

---

# 🛡️ RBAC System Class

Main authorization engine.

```python
class RBACSystem:
    """
    Main RBAC system.
    """

    def __init__(self):
        self.users = {}
        self.roles = {}

    def create_role(self, role_name):

        role = Role(role_name)
        self.roles[role_name] = role

        return role

    def create_user(self, username):

        user = User(username)
        self.users[username] = user

        return user

    def check_access(self, username, action, resource):

        user = self.users.get(username)

        if not user:
            return False

        permission = Permission(action, resource)

        return user.has_permission(permission)

    def display_system_state(self):

        print("\n=== RBAC System State ===")

        print(f"\nRoles ({len(self.roles)}):")

        for role in self.roles.values():

            print(f"  - {role}")

            for perm in role.permissions:
                print(f"    * {perm}")

        print(f"\nUsers ({len(self.users)}):")

        for user in self.users.values():
            print(f"  - {user}")
```

---

# 🧪 Task 2: Test the RBAC Simulator

Create `test_rbac.py`

```python
#!/usr/bin/env python3

from rbac_simulator import RBACSystem, Permission

def main():

    rbac = RBACSystem()

    print("=== Setting up RBAC System ===\n")

    # Roles
    admin = rbac.create_role("admin")
    editor = rbac.create_role("editor")
    viewer = rbac.create_role("viewer")

    # Admin Permissions
    admin.add_permission(Permission("read", "document"))
    admin.add_permission(Permission("write", "document"))
    admin.add_permission(Permission("delete", "document"))

    # Editor Permissions
    editor.add_permission(Permission("read", "document"))
    editor.add_permission(Permission("write", "document"))

    # Viewer Permissions
    viewer.add_permission(Permission("read", "document"))

    # Users
    alice = rbac.create_user("alice")
    bob = rbac.create_user("bob")
    charlie = rbac.create_user("charlie")

    # Assign Roles
    alice.assign_role(admin)
    bob.assign_role(editor)
    charlie.assign_role(viewer)

    rbac.display_system_state()

    print("\n=== Testing Access Control ===\n")

    test_cases = [
        ('alice', 'delete', 'document', True),
        ('bob', 'write', 'document', True),
        ('bob', 'delete', 'document', False),
        ('charlie', 'read', 'document', True),
        ('charlie', 'write', 'document', False),
    ]

    for username, action, resource, expected in test_cases:

        result = rbac.check_access(username, action, resource)

        status = "GRANTED" if result else "DENIED"
        check = "✓" if result == expected else "✗"

        print(
            f"{check} {username} -> {action}:{resource} = {status}"
        )

if __name__ == "__main__":
    main()
```

---

# ▶️ Run the Simulator

```bash
python3 test_rbac.py
```

---

# ✅ Expected Output

```text
=== RBAC System State ===

Roles (3):

  - Role: admin (3 permissions)
    * read:document
    * write:document
    * delete:document

  - Role: editor (2 permissions)
    * read:document
    * write:document

  - Role: viewer (1 permissions)
    * read:document

Users (3):

  - User: alice (Roles: ['admin'])
  - User: bob (Roles: ['editor'])
  - User: charlie (Roles: ['viewer'])

=== Testing Access Control ===

✓ alice -> delete:document = GRANTED
✓ bob -> write:document = GRANTED
✓ bob -> delete:document = DENIED
✓ charlie -> read:document = GRANTED
✓ charlie -> write:document = DENIED
```

---

# 🔍 Verification

## Test 1: Verify Basic Functionality

```bash
python3 -c "
from rbac_simulator import RBACSystem, Permission

rbac = RBACSystem()

admin = rbac.create_role('admin')
admin.add_permission(Permission('read', 'file'))

user = rbac.create_user('testuser')
user.assign_role(admin)

print(
'Access granted!'
if rbac.check_access('testuser','read','file')
else 'Access denied!'
)
"
```

Expected:

```text
Access granted!
```

---

## Test 2: Custom Scenario

Create `custom_test.py`

```python
from rbac_simulator import RBACSystem, Permission

rbac = RBACSystem()

manager = rbac.create_role('manager')

manager.add_permission(
    Permission('read', 'reports')
)

manager.add_permission(
    Permission('write', 'reports')
)

user = rbac.create_user('john')

user.assign_role(manager)

print(
rbac.check_access(
'john',
'read',
'reports'
)
)

print(
rbac.check_access(
'john',
'delete',
'reports'
)
)
```

Run:

```bash
python3 custom_test.py
```

---

## Test 3: Multiple Roles Per User

```python
developer = rbac.create_role('developer')

developer.add_permission(
    Permission('read', 'code')
)

developer.add_permission(
    Permission('write', 'code')
)

user.assign_role(developer)

print(
rbac.check_access(
'john',
'write',
'code'
)
)
```

---

# 🧠 RBAC Flow Diagram

```text
            ┌─────────┐
            │  User   │
            └────┬────┘
                 │
                 ▼
          ┌─────────────┐
          │    Role     │
          └────┬────────┘
               │
               ▼
        ┌───────────────┐
        │ Permissions   │
        └──────┬────────┘
               │
               ▼
         Access Granted
```

---

# 🚨 Troubleshooting

## Permission Not Found

Verify action and resource strings match exactly.

```python
Permission("read", "document")
```

---

## Access Always Denied

Check:

- Permission added to role
- Role assigned to user
- Exact permission names used

---

## Import Errors

Ensure files exist in the same directory:

```bash
ls
```

Expected:

```text
rbac_simulator.py
test_rbac.py
```

---

## Set Operations Failing

Verify both methods exist:

```python
def __eq__(self, other):
```

```python
def __hash__(self):
```

---

# 📊 Real-World Applications

RBAC is used extensively in:

| Platform | Usage |
|-----------|--------|
| ☁️ AWS IAM | Cloud permissions |
| ☁️ Azure RBAC | Resource authorization |
| ☁️ Google Cloud IAM | Access control |
| 🐧 Linux | User/group permissions |
| 🗄️ Databases | Privilege management |
| 🏢 Enterprise Apps | User authorization |

---

# 🎓 Key Takeaways

✅ Users inherit permissions from roles

✅ Roles simplify authorization management

✅ One user can have multiple roles

✅ RBAC scales better than assigning permissions individually

✅ RBAC is the foundation of modern access control systems

---

# 🚀 Next Steps

Enhance the simulator by adding:

- 🔗 Role inheritance
- ⏰ Time-based access control
- 📍 Location-based permissions
- 📝 Audit logging
- 🌐 REST API integration
- 🖥️ Command-line management interface

---

# 🏁 Conclusion

Congratulations! 🎉

You successfully built a complete **Role-Based Access Control (RBAC) Simulator** capable of:

- Creating users and roles
- Managing permissions
- Making authorization decisions
- Supporting multiple roles per user
- Simulating enterprise-grade access control workflows

These same concepts power modern security systems used across operating systems, cloud platforms, databases, and enterprise applications worldwide.

**Secure systems start with proper access control—and RBAC is one of the most widely adopted models in cybersecurity.**
