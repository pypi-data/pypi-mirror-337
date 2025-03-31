from setuptools import setup, find_packages
import re

# Extract version from __init__.py
with open('dotenvy_py/__init__.py', 'r') as f:
    version_match = re.search(r'^__version__ = ["\']([^"\']*)["\']', f.read(), re.M)
    if version_match:
        version = version_match.group(1)
    else:
        raise RuntimeError("Couldn't find version string")

# Use README_PYPI.md for PyPI description if available, otherwise use README.md
try:
    with open('README_PYPI.md', 'r') as f:
        long_description = f.read()
        readme_source = "README_PYPI.md"
except FileNotFoundError:
    with open('README.md', 'r') as f:
        long_description = f.read()
        readme_source = "README.md"

print(f"Using {readme_source} for package long description")

setup(
    name="dotenvy-py",
    version=version,
    author="NeutrobeatBoxing",
    author_email="dev@neutroboxing.com",
    description="A Python port of Rust's dotenvy with first-occurrence-wins behavior",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/neutroboxing/dotenvy-py",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    keywords="dotenv, environment, config, env, dotenvy, rust",
) 