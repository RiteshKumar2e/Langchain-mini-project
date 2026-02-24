# Git and Version Control

## What is Git?

Git is a distributed version control system (VCS) that tracks changes in source code during software development. It was created by Linus Torvalds in 2005 for Linux kernel development.

Git enables multiple developers to work together on the same project efficiently while maintaining a complete history of all changes.

## Core Concepts

### Repository (Repo)

A repository is a directory that Git tracks. It contains:
- All project files
- `.git/` directory with the version history

### Commits

A commit is a snapshot of the repository at a point in time:
- Has a unique SHA-1 hash identifier
- Contains author, date, message, and parent commit reference
- Immutable once created

### Branches

Branches are lightweight pointers to specific commits:
- `main` / `master`: The primary branch
- Feature branches: For developing new features
- Hotfix branches: For urgent bug fixes

### HEAD

HEAD is a special pointer indicating the current checkout position.

## Essential Git Commands

### Setup
```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

### Creating and Cloning
```bash
git init                    # Initialize new repo
git clone <url>             # Clone existing repo
```

### Staging and Committing
```bash
git status                  # Check status
git add <file>              # Stage a file
git add .                   # Stage all changes
git commit -m "message"     # Commit staged changes
git commit -am "message"    # Stage and commit tracked files
```

### Branching
```bash
git branch                  # List branches
git branch <name>           # Create branch
git checkout <name>         # Switch branch
git checkout -b <name>      # Create and switch
git merge <name>            # Merge branch
git branch -d <name>        # Delete branch
```

### Remote Operations
```bash
git remote add origin <url> # Add remote
git push origin main        # Push to remote
git pull origin main        # Pull from remote
git fetch                   # Download without merging
```

### Inspection
```bash
git log                     # View commit history
git log --oneline           # Compact log
git diff                    # View unstaged changes
git diff --staged           # View staged changes
git show <commit>           # Show commit details
```

### Undoing Changes
```bash
git restore <file>          # Discard working directory changes
git reset HEAD <file>       # Unstage a file
git revert <commit>         # Create a commit that undoes changes
git reset --hard <commit>   # Reset to a commit (destructive)
```

## Git Workflows

### Feature Branch Workflow
1. Create a feature branch from `main`
2. Develop the feature with multiple commits
3. Open a Pull Request / Merge Request
4. Code review
5. Merge into `main`

### Gitflow Workflow
- `main`: Production-ready code
- `develop`: Integration branch
- `feature/*`: New features
- `release/*`: Release preparation
- `hotfix/*`: Urgent patches

### Trunk-Based Development
- Commit directly to `main` (or short-lived branches)
- Use feature flags for incomplete features
- Continuous integration and deployment

## GitHub / GitLab / Bitbucket

### Pull Requests
- Propose changes to be merged
- Enable code review
- Discuss and iterate on changes

### Issues
- Track bugs, features, and tasks
- Can be linked to commits and pull requests

### Actions / CI/CD
- Automated workflows on events (push, PR, etc.)
- Run tests, linting, deployment

## .gitignore

Specifies files Git should not track:
```
# Python
__pycache__/
*.pyc
.env
venv/

# Node
node_modules/
.env.local
dist/
```

## Advanced Git

### Rebasing
```bash
git rebase main             # Reapply commits on top of main
git rebase -i HEAD~3        # Interactive rebase last 3 commits
```

### Stashing
```bash
git stash                   # Temporarily store changes
git stash pop               # Restore stashed changes
git stash list              # List stashes
```

### Cherry-pick
```bash
git cherry-pick <commit>    # Apply a specific commit
```

### Tags
```bash
git tag v1.0.0              # Lightweight tag
git tag -a v1.0.0 -m "..."  # Annotated tag
git push origin --tags      # Push tags
```
