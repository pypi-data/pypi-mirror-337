# qink - Real-time data processing framework

<img src="logo.png" alt="Qink Logo" >

A Cython-based data pipeline project.

## Development Setup

```
# Windows
set PYTHONPATH=.

# Linux/macOS
export PYTHONPATH=.
```

1. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Build the Cython modules:

```bash
python setup.py build_ext --inplace
```

## Testing

To run the tests:

```bash
pytest
```

This will run all tests and generate a coverage report. The coverage report will show which parts of the code are covered by tests.

To run tests with more detailed output:

```bash
pytest -v
```

To run a specific test file:

```bash
pytest tests/test_fib.py
```

To run tests in watch mode (automatically re-runs tests when files change):

```bash
ptw
```

You can also use additional options with watch mode:

```bash
ptw -- -v  # Verbose output
ptw -- -k "test_name"  # Run tests matching the given name
```

Copyright 2024 Quadible

This software is the property of Quadible and is protected under copyright law. Unauthorized copying, distribution, or use of this software, in whole or in part, without express permission from Quadible is strictly prohibited.
This repository and its contents are for authorized internal use only. External sharing or modification is not permitted unless written consent is obtained from Quadible.
For inquiries about permitted usage or licensing, contact [info@quadible.co.uk](mailto:info@quadible.co.uk).
