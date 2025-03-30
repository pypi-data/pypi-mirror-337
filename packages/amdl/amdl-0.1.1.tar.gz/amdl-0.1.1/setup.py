from setuptools import setup, find_packages

setup(
    name="amdl",
    version="0.1.1",
    author="Zarby",
    author_email="ZarbyTheOne@proton.me",
    description="This allows you to load modules in an elegant way.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/zZarby/amdl",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
