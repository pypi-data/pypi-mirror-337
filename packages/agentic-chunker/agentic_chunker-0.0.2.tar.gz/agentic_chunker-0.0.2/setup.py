from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name='agentic_chunker',
    version='0.0.2',
    packages=find_packages(),
    install_requires=[
        'openai>=1.24.1'
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Gurram Siddarth Reddy',
)