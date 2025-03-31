from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="raaju1",
    version="1.2.2",
    packages=find_packages(),
    install_requires=[], 
    entry_points={
        "console_scripts": [
            "raaju1 = raaju1:roomate",
        ],
    },
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Raaj",
    
    
)