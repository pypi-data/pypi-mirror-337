# setup.py
from setuptools import setup, find_packages

setup(
    name="printpgm",  # Replace with your package name
    version="0.3",
    packages=find_packages(),
    description="A simple package to print predefined texts",
    author="forgiveme",
    author_email="plshelpme.email@example.com",
    install_requires=["pyperclip>=1.8.0"]
)
