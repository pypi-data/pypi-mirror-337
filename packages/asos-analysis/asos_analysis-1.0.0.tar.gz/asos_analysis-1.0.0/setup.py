from setuptools import setup, find_packages

# Read the contents of your README.md file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="asos_analysis",  # Name of your library
    version="1.0.0",  # Initial version
    description="A Python tool for sorting and analyzing ASOS weather data",  # Brief description
    long_description=long_description,  # Detailed description (from README.md)
    long_description_content_type="text/markdown",  # Specify that the long description is in Markdown
    author="Saurav",  # Your name
    author_email="your_email@example.com",  # Your email
    url="https://github.com/sauravshuvo/asos_analysis",  # GitHub repository URL
    packages=find_packages(),  # Automatically detect packages
    install_requires=[
        "pandas>=1.3.0",
        "openpyxl>=3.0.9",
    ],  # Dependencies
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # License
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",  # Minimum Python version
)
