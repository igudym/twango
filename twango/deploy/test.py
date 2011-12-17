from jinja2 import Environment, FileSystemLoader
import os.path as pth
import config
import pprint 
import deploy

path = pth.abspath(pth.join(pth.dirname(__file__), "templates"))

env = Environment(loader=FileSystemLoader(path))


template = env.get_template('test.conf')
print template.render(name='John Doe')

config.settings.pprint()

deploy.deploy()

