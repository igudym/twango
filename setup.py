from setuptools import setup, find_packages
setup(
    version = "0.1",
    name = "twango",
    packages = find_packages(),
    scripts = ['twango/twango-admin.py'],
	package_data = {
	        # If any package contains *.txt or *.rst files, include them:
	        '': ['*.sh','*.txt', '*.html','*.js','*.css','*.png','*.jpg','*.pdf'],
			'twango/template/default/src/media':['*'],
			'twango/template/default/src/settings':['*'],
			'twango/template/default/src/templates':['*'],
	    },
    author = "Daniel Gray",
    author_email = "dan@technigami.com",
    description = "A package to help automate creation of new django apps and projects",
    url = "",
    include_package_data = True
)
