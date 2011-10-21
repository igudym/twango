"""
Methods for populating an initial project structure from a template app
"""
import os
import sys
import re

import shutil
from subprocess import call,check_call

strings = {}

strings['msg'] = """
*********************************
  Project {{project}}  created 
*********************************


Once installation is complete,
you should run ./bootstrap.sh in the newly created directory
to complete the setup of your environment.

This should be wrapped into this script, but something was amiss with 
subprocess / popen calling it.

"""

def startproject(target):
	"""
	starts a project from the default project template
	@todo: make this expandable to any template project
	
	@param target:  the path to the project directory.
	"""
	projpath = os.path.abspath(os.path.dirname(__file__)+"/../template/default/")
	shutil.copytree(projpath,target)
	
	print strings['msg'].replace('{{project}}',target)
	os.popen("cd "+os.path.abspath(target)+" && chmod 755 bootstrap.sh")