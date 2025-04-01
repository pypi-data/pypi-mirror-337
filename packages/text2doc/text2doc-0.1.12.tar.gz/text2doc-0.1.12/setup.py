from setuptools import setup, find_packages

setup(
    name="text2doc",
    version="0.1.12",  # Hard-coded clean version
    description="Convert text to formatted documents",
    author="text2doc Team",
    author_email="info@text2doc.com",
    url="https://github.com/text2doc/python",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)