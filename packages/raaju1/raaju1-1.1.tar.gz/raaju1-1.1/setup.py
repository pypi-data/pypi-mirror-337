from setuptools import setup, find_packages

setup(
    name="raaju1",
    version="1.1",
    packages=find_packages(),
    install_requires=[], 
    entry_points={
        "console_scripts": [
            "raaju1 = raaju1:roomate",
        ],
    }
)