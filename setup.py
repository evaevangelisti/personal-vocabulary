from setuptools import setup, find_packages

setup(
    name="personal_vocabulary",
    version="0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "requests",
    ],
    entry_points={
        "console_scripts": [
            "personal_vocabulary=main:main",
        ],
    },
)