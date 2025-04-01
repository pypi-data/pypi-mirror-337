from setuptools import setup, find_packages

# Read version from version.py (or you can hardcode it here)
version = "0.1.0"

setup(
    name="log2doc",  # Package name
    version=version,  # Set the version of your package
    description="A package to fetch and explain recent Linux/Windows terminal commands.",
    long_description=open("README.md").read(),  # Long description from your README file
    long_description_content_type="text/markdown",  # Format of the long description
    author="Savinay Pandey",
    author_email="savinaypandey123@gmail.com", 
    url="https://github.com/SaviPandey/log2doc",  # Update with your GitHub link
    packages=find_packages(),  # Automatically find all packages in the current directory
    install_requires=[  # Dependencies your package needs
        "google-genai",
        "python-dotenv",  # For managing environment variables
    ],
    classifiers=[  # Optional classifiers
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Minimum Python version supported
    entry_points={  # Entry point for the CLI command
        "console_scripts": [
            "log2doc=log2doc.explain:main",  # Correct entry point for CLI command
        ]
    },
)
