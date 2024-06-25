from setuptools import setup, find_packages

setup(
    name="personal-vocabulary",
    version="1.0.0",
    author="Eva",
    packages=find_packages(),
    install_requires=[
        "appdirs",
        "beautifulsoup4",
        "requests",
        "sortedcontainers",
    ],
    entry_points={
        "console_scripts": [
            "personal-vocabulary=personal_vocabulary.main:main",
        ],
    },
)