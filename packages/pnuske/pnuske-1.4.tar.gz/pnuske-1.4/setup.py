from setuptools import setup, find_packages     

setup(
    name="pnuske",
    version="1.4",
    packages=find_packages(),
    entry_points={
        "console_scripts": ["pnuske=pnuske:run"]
    },
)   