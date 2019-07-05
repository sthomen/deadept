from setuptools import setup,find_packages

setup(
	name = 'deadept',
	version = '1.2',
	packages = find_packages(),

	entry_points = {
		'console_scripts': [
			'deadept = deadept.scripts.deadept:decode',
			'deadeptdump = deadept.scripts.deadept:dump'
		]
	},

	author = 'Staffan Thomen',
	author_email = 'staffan@thomen.fi',
	description = ('Program to remove Adobe Adept DRM from epub files'),

	url = 'https://mercurial.shangtai.net/deadept',

	license = 'BSD',

	classifiers = [
		'Development Status :: 4 - Beta',
		'Programming Languge :: Python :: 3'
	])
