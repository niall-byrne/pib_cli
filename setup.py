from setuptools import find_packages, setup
import os

with open("README.md", "r") as fh:
  long_description = fh.read()

with open(os.path.join("assets", "requirements.txt")) as fh:
  assets = [line for line in fh.read().strip().split('\n') if line[0] != "#"]

packages = find_packages()
packages.remove('pib_cli.tests')

setup(
  name="pib_cli",
  version="0.0.1",
  author="Niall Byrne",
  author_email="niall@niallbyrne.ca",
  description="CLI for Python in a Box",
  entry_points='''
    [console_scripts]
    pib_cli=pib_cli.cli:cli
    dev=pib_cli.cli:cli
  ''',
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/niall-byrne/pib_cli",
  packages=packages,
  package_data={
    'pib_cli': [
      os.path.join("config", "config.yml"),
      os.path.join('bash', '.*'),
    ],
  },
  include_package_data=True,
  install_requires=assets,
  license="License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
    "Operating System :: OS Independent",
  ],
  python_requires='>=3.7.0,<3.8.0',
)
