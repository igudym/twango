import ez_setup
ez_setup.use_setuptools()
from setuptools import setup, find_packages
setup(
    name = "django-brains",
    version = "0.1",
    packages = find_packages(),
    author = "Daniel Gray",
    author_email = "dan@technigami.com",
    description = "A package to help automate creation of new django apps and projects",
    url = "",
    include_package_data = True
)
