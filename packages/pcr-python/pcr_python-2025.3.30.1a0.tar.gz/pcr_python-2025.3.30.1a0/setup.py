from setuptools import setup, find_packages

setup(
    name='pcr_python',
    version='2025.03.30.1-alpha',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[],
)