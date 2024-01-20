import io
import os
from setuptools import find_packages, setup


def read(*paths, **kwargs):
    content = ""
    with io.open(
        os.path.join(os.path.dirname(__file__), *paths),
        encoding=kwargs.get("encoding", "utf8"),
    ) as open_file:
        content = open_file.read().strip()
    return content


def read_requirements(path):
    return [
        line.strip()
        for line in read(path).split("\n")
        if not line.startswith(('"', "#", "-", "git+"))
    ]


setup(
    name="StudIP-cli",
    version=read("StudIP-cli", "0.1"),
    description="StudIP command line interface to emulate a JSON API",
    url="https://github.com/FrederikRichter/StudIP-cli",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="Frederik Richter",
    packages=find_packages(exclude=["tests", ".github"]),
    install_requires=read_requirements("requirements.txt"),
    entry_points={
        "console_scripts": ["studip-cli = studip-cli.__main__:main"]
    }
)

