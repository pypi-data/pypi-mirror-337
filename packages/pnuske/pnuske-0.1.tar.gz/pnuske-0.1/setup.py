from setuptools import setup, find_packages     

setup(
    name="pnuske",
    version="0.1",
    packages=find_packages(),
    entry_points={
        "console_scripts": ["pnuske=pnuske.main:run"]
    },
)   