from setuptools import find_packages, setup

PROJECT_NAME = 'MY_PROJECT'

with open("README.md", "r") as fh:
  long_description = fh.read()

packages = find_packages()
packages.remove('pib_cli.tests')

setup(
    name="%s_pib_cli" % PROJECT_NAME,
    version="0.0.1",
    author="Niall Byrne",
    author_email="niall@niallbyrne.ca",
    description="CLI for Python in a Box",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/niall-byrne/pib_cli",
    packages=packages,
    install_requires=[],
    license="License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7.0,<3.8.0',
)
