from setuptools import setup, find_packages     

setup(
    name="pnuske",
    version="0.7",
    packages=find_packages(),
    entry_points={
        "console_scripts": ["pnuske=pnuske:run"]
    },
)   