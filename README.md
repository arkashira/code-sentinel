# Code Sentinel Context-Aware Remediation Engine
As a platform engineer, you want remediation suggestions for detected adversarial code, so you can fix issues without introducing new bugs.
## Features
* Remediation suggestions for HIGH severity findings
* Fix suggestions preserve original resource intent
* Suggestions are validated against Terraform plan compatibility
## Usage
1. Run `python -m pytest` to execute the tests
2. Run `python src/remediation_engine.py` to execute the remediation engine
