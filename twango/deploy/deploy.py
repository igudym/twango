from config import settings
from fabric.api import run, env
from fabric.network import disconnect_all
from fabric.context_managers import settings as fabset

VERBOSE = True

class KeywordError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def provision(node):
    if VERBOSE:
        print 'Provision: ', node
    cmd = 'apt-get update ; apt-get -y -q upgrade' if env.host_type == 'deb' else 'yum -y update'
    run(cmd)

def process_packages(node, packages):
    if VERBOSE:
        print "Install packages: ", node, packages
    cmd = 'apt-get -y -q install ' if env.host_type == 'deb' else 'yum -y install '
    params = packages if type(packages) == str else ' '.join(packages)
    run(cmd + params)

def process_project(node, project):
    if VERBOSE:
        print "Project: ", node, project

def process_modules(node, modules):
    if VERBOSE:
        print "Modules: ", node, modules
    run('pip install ' + ' '.join(modules))

def process_render(node, conf):
    if VERBOSE:
        print "Render: ", node, conf

def process_entity(node, entity, defs):
    print node, entity, defs
    for key, value in defs.iteritems():
        if key == 'roles':
            if entity != 'NODEDEF':
                raise KeywordError(key)
            for role in value:
                process_entity(node, 'ROLE', settings.ROLES[role])
        elif key == 'packages':
            process_packages(node, value)
        elif key == 'services':
            for service in value:
                process_entity(node, 'SERVICE', settings.SERVICES[service])
        elif key == 'projects':
            for project in value:
                process_project(node, project)
        elif key == 'modules':
            process_modules(node, value)
        elif key == 'render':
            for conf in value:
                process_render(node, conf)
        else:
            raise KeywordError(key)
            
def set_host_type():
    with fabset(warn_only=True):
        result = run('rpm -v')
    env.host_type = 'deb' if result.failed else 'rpm'

def deploy_node(node, defs):
    set_host_type()
    process_packages(node, 'python-pip') # need for 'module' handler
    process_entity(node, 'NODEDEF', defs)

def deploy():
    for node,defs in settings.NODEDEFS.iteritems():
        if not settings.NODES.has_key(node):
            if settings.OPTIONS['provision'] is not None:
                provision(node)
        env.host_string = '@'.join([settings.NODES[node]['user'], settings.NODES[node]['ip']])
        deploy_node(node, defs)

