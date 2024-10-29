from setuptools import setup, find_packages

setup(
	name='project1',
	version='1.0',
	author='Venkata Naga Satya Avinash, Gudipudi',
	author_email='gudipudiv@ufl.edu',
	packages=find_packages(exclude=('tests', 'docs', 'resources')),
	setup_requires=['pytest-runner'],
	tests_require=['pytest']	
)