from setuptools import setup, find_packages

setup(
    name="nyt-digits-solver",          # must be unique on PyPI!
    version="0.1.2",
    author="Gabor Meszaros",
    description="Riddle solver algorithms for the NYT Digits game",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3.11',
)
