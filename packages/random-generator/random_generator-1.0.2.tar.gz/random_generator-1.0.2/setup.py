from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='random_generator',
    version='1.0.2',
    description='Random generator',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Krzysztof Żyłka',
    author_email='krzysztofzylka@yahoo.com',
    install_requires=[],
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
