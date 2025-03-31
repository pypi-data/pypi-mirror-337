from setuptools import setup, find_packages

setup(
    name='hopkins_ep_timesheet_utils',
    version='0.1',
    packages=find_packages(exclude=['tests*']),
    license='MIT',
    description='Loading shared utilities for Hopkins project',
    long_description=open('README.md').read(),
    install_requires=[],
    url='https://github.com/mathewdenison/shared_utils',
    author='Mathew Denison',
    author_email='mathewdenison@gmail.com'
)
