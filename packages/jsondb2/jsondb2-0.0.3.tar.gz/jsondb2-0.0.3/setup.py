from setuptools import setup, find_packages

setup(
    name="jsondb2",
    version="0.0.3",
    packages=find_packages(),
    description="Use json file as database",
    long_description=open("README.md", "r", encoding="utf-16").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/sinofarmonovzfkrvjl/JsonDB",
    classifiers=[
        "Programming Language :: Python :: 3",
    ]
)
