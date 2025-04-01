#!/usr/bin/env python3
import os
import re
from setuptools import setup, find_packages

# Read version from __init__.py without importing the package
with open(os.path.join('treeignore', '__init__.py'), 'r') as f:
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", f.read(), re.M)
    if version_match:
        version = version_match.group(1)
    else:
        raise RuntimeError("Unable to find version string in treeignore/__init__.py")

if __name__ == "__main__":
    setup(
        version=version,
        packages=find_packages(),
    )
