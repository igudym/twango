from setuptools import setup, find_packages
setup(
    version = "0.1",
    name = "twango",
    packages = find_packages(),
    scripts = ['twango/twango-admin.py'],
	package_data = {
	        # If any package contains *.txt or *.rst files, include them:
			'twango/template/default/src/':['*'],
	    },
	exclude_package_data = { 'twango/template/default/src/':['*.pyc'] },
    author = "Daniel Gray",
    author_email = "dan@technigami.com",
    description = "A package to help automate creation of new django apps and projects",
    url = "",
    include_package_data = True
)
