from setuptools import setup, find_packages
from os import path
working_dir = path.dirname(path.abspath(__file__))

with open(path.join(working_dir, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="easy_email_template",
    version="0.0.1",
    description="A package to help with email send functionality",
    author="davidb@rumianocheese.com",
    author_email="daveandtaybillingsley@gmail.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[],
)