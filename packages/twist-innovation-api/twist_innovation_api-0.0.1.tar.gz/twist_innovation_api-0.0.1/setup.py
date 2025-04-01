from setuptools import setup, find_packages

setup(
    name="twist-innovation-api",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[
        # "requests"  # For REST API
    ],
    author="Sibrecht Goudsmedt",
    author_email="sibrecht.goudsmedt@twist-innovation.com",
    description="Python library to talk to the twist-innovation api",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/twist-innovation/twist-innovation-api",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)

