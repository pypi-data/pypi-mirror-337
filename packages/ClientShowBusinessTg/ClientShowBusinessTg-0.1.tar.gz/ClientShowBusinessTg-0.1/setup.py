import setuptools
with open('README.md', 'r', encoding='utf-8') as fh:
	long_description = fh.read()

setuptools.setup(
	name='ClientShowBusinessTg',
	version='0.1',
	author='showbusiness',
	author_email='fefrwerfre53@tutamail.com',
	description='async upload archive',
	long_description=long_description,
	long_description_content_type='text/markdown',
	packages=['ClientShowBusinessTg'],
	include_package_data=True,
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.11',
)