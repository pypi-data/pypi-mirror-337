from setuptools import setup, find_packages

setup(
    name='matmacore',
    version='0.1.10',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'matplotlib',
        'colormaps ',
        'networkx'
    ],
)
