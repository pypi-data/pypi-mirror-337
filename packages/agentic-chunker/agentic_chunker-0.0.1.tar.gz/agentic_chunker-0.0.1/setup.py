from setuptools import setup, find_packages

setup(
    name='agentic_chunker',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'openai>=1.24.1'
    ],
)