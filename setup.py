import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="google_patent_scraper",
    version="1.0.8",
    author="Ryan Stevens",
    author_email="ryan.louis.stevens@gmail.com",
    description="A package to scrape patents from 'https://patents.google.com/'",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rls542/patent_scraper/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
