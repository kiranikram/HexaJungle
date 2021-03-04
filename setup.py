from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()


setup(
    name='HexaJungle',
    version='0.0.01',
    description='MARL Simulator for Mixed-Motive Communication',
    author='Kiran Ikram, Michael Garcia Ortiz',
    author_email='kiran.ikram@city.ac.uk',
    packages=[package for package in find_packages()
                if package.startswith('HexaJungle')],
    include_package_data=True,
    install_requires=requirements
)