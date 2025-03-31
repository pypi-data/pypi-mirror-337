from setuptools import setup, find_packages

setup(
    name="prarthana_package",
    version="0.1",
    author="Prarthana",
    author_email="your_email@example.com",
    description="A simple package with math and string utilities",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/GKPrarthana/prarthana_package",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
