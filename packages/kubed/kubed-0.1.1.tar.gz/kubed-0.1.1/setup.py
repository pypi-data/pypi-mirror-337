from setuptools import setup, find_packages
import os

# Read the contents of README.md file
with open(os.path.join(os.path.dirname(__file__), "README.md"), "r") as f:
    long_description = f.read()

setup(
    name="kubed",
    version="0.1.1",
    description="CLI productivity tool with autocompletion for Docker, Terraform, Helm, and Kubernetes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Daley Arborough",
    author_email="info@daleyarborough.com",
    url="https://daleyarborough.com",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "kubed": ["completions/*.bash", "completions/*.zsh", "aliases/*.sh"],
    },
    entry_points={
        "console_scripts": [
            "kubed-setup=kubed.cli:setup_command",
            "kubed-completions-path=kubed.cli:completions_path_command",
            "kubed-aliases-path=kubed.cli:aliases_path_command",
        ],
    },
    python_requires=">=3.6",
    install_requires=[
        "click>=7.0",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Systems Administration",
    ],
) 