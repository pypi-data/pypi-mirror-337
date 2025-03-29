from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ghcopilot",
    version="0.1.0",
    description="GitHub Copilot API + CLI",
    author="CodeSoft",
    author_email="hello@mail.codesoft.is-a.dev",  # Added author email
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        "requests",
        "selenium",
        "rich",
        "inquirer"
    ],
    extras_require={
        "dev": [
            "pytest",
            "pytest-cov",
            "black",
            "flake8",
        ],
    },
    entry_points={
        'console_scripts': [
            'copilot=ghcopilot.cli:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)