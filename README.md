# Inventory_Management_LAB05
# Static Analysis Issues Fixed – Lab 5

| Issue | Type | Line | Description | Fix |
|------|------|------|------------|------|
| Mutable default argument | Bug | addItem() | logs=[] reused across calls | Changed to logs=None and initialized inside function |
| Broad exception | Code smell | except: | Hides real errors | Replaced with except KeyError |
| Insecure eval() | Security | eval() in main() | Executes arbitrary code | Removed the eval call |
| File opened without context manager | Resource leak | open() in load/save | File may not close properly | Used with open() context manager |
| Type errors on invalid input | Logic bug | passing wrong types | addItem(123, "ten") would break | Added input validation |
| KeyError crash | Bug | getQty(item) | Crash if item doesn't exist | Used stock_data.get(item, 0) |
| Unused import | Style | import logging | Not used, unnecessary import | Removed unused import |

# Lab 5 Reflection

## 1. Easiest vs Hardest Issues
- *Easiest:* Replacing open() with with open() and changing print formatting to f-strings.
- *Hardest:* Fixing the mutable default argument logs=[] because it requires an understanding of default argument behavior in Python.

## 2. False Positives
- Bandit flagged file writes; while writing text files isn't inherently risky here, it's still good practice to use with for safety. No problematic false positives impacted the lab.

## 3. Integrating Static Analysis in Workflow
- Run flake8 and pylint locally before commits.
- Add Bandit to CI (GitHub Actions) so security issues are checked on every push.
- Treat medium/high severity findings as blocking for production code.

## 4. Improvements Observed
- Reduced crashes from missing keys (used .get()).
- Avoided potential shared state bugs (removed mutable default).
- Removed eval() for security and used safer patterns.
- Improved readability and maintainability via consistent naming and f-strings.
