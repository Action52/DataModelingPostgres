from setuptools import setup

setup(
    name="dmp",
    version="0.1",
    author="alfredo.leon",
    description="This is the first project for Udacity's Data Engineering Nanodegree.",
    install_requires=[
        "pandas",
        "jupyter",
        "psycopg2-binary",
        "tqdm"
    ]
)