```text
NOTE: crtl+shift+V to preview markdown file
NOTE: ctrl+K V to view and preview markdown
```

# Week 1 – Engineering Learning Lab

## Theme
**Professional Engineering Development Environment**

### Primary Goal
Create an environment where you can learn, build, test, document, and version-control future projects.

---

# Technical Accomplishments

## 1. GitHub Setup Complete

### Repository Created

```text
engineering-learning-lab
```
### Success Criteria

- GitHub account configured
- SSH key configured
- Can clone repository
- Can push changes
- Can pull changes
- Can create branches

### Commands to Understand

```bash
git clone
git add
git commit
git push
git pull
git checkout
git branch
```

---

## 2. VS Code Setup Complete

### Install

- VS Code
- Python Extension
- GitHub Extension
- Docker Extension
- Markdown Extension

### Success Criteria

Can:

- Open project folders
- Run Python
- Debug Python
- Use integrated terminal
- Commit changes from VS Code

---

## 3. Python Environment Working

### Create

```text
01-development-environment/python-test/
```

### Example Script

```python
print("Engineering Learning Lab")
```

### Success Criteria

Run successfully:

```bash
python test.py
```

### Install NumPy

```bash
pip install numpy
```

### Verification Script

```python
import numpy as np

print(np.__version__)
```

---

## 4. Learn Basic Linux Commands

### Commands

```bash
pwd
ls
cd
mkdir
rm
cp
mv
cat
grep
find
```

### Success Criteria

Without looking up commands, you can:

- Navigate folders
- Create files
- Delete files
- Copy files
- Move files
- Search for files

---

## 5. Create First Engineering Script

### Option A – Unit Converter

```python
feet = 1000
meters = feet * 0.3048

print(meters)
```

### Option B – Aircraft Turn Radius Calculator

```python
import math

speed = 50
bank = 30

radius = speed**2 / (9.81 * math.tan(math.radians(bank)))

print(radius)
```

### Success Criteria

At least one engineering-related Python program exists in GitHub.

---

# Documentation Accomplishments

## Create README

### Purpose Statement

Example:

> This repository contains my engineering development journey focused on systems engineering, software development, cloud technologies, controls, GNC, autonomy, AI, and aerospace architecture.

### Include High-Level Roadmap

```text
Development Tools
Software Foundations
Cloud Foundations
Systems Engineering
Controls
GNC
Autonomy
AI for Autonomy
Advanced Projects
```

---

# Engineering Habits

## Daily Git Commits

Make commits even for small improvements.

### Examples

```text
Added Linux notes
Updated README
Completed Python exercise
Configured VS Code
```

---

## Start an Engineering Notebook

### Create

```text
notes/
```

### Example Files

```text
linux-notes.md
git-notes.md
python-notes.md
```

### Document

- Commands learned
- Lessons learned
- Mistakes encountered
- Questions to research later

---

# Portfolio Deliverables

By the end of Week 1, you should be able to show:

### Repository

```text
engineering-learning-lab
```

### Documentation

- Organized README
- Linux notes
- Git notes
- Python notes

### Code

- At least one engineering-related Python script

### Version Control

- Multiple commits demonstrating progress

---

# Week 1 Definition of Success

You can confidently:

- Create and organize repositories
- Write and run Python programs
- Use Git for version control
- Navigate a Linux terminal
- Use VS Code effectively
- Document technical work in Markdown

---

# Stretch Goals (Excellent Outcome)

If time allows:

- Configure SSH authentication for GitHub
- Learn Git branching workflow
- Create a Python virtual environment
- Install and test Docker
- Explore GitHub Issues and Projects
- Create a long-term roadmap for Weeks 2–40

---

# Why Week 1 Matters

Week 1 is not about advanced controls, autonomy, or AI.

It is about building the professional engineering environment and workflow that every future project will rely on.

A strong foundation in Git, Python, Linux, documentation, and development tools will accelerate learning across:

- Systems Engineering
- MBSE
- Controls
- GNC
- Robotics
- Autonomy
- Cloud Computing
- Aerospace Software Development

The goal is simple:

> Build an environment where future learning becomes faster, easier, and more professional.
