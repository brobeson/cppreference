# Contributing

## Building the Documentation

### Set Up the Build Environment

1. Create a Python virtual environment.
   ```bash
   python3 -m venv .venv
   ```
1. Activate the virtual environment.
   ```bash
   source .venv/bin/activate
   ```
1. Install required packages.
   ```bash
   pip install -r requirements.txt
   ```

### Build the Documentation

Run sphinx-build.

```bash
sphinx-build docs/ build/
```
