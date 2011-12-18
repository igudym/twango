from config import settings
from fabric.api import run, put, env
from fabric.network import disconnect_all
from fabric.context_managers import settings as fabset
from fabric.contrib.project import rsync_project
from fabric.contrib.files import upload_template
import os

VERBOSE = True

class KeywordError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def provision(node):
    if VERBOSE:
        print 'Provision: ', node
    cmd = prefix(node) + ('apt-get update ; apt-get -y -q upgrade' if env.host_type == 'deb' else 'yum -y update')
    run(cmd)

def process_packages(node, packages):
    if VERBOSE:
        print "Install packages: ", node, packages
    cmd = prefix(node) + ('apt-get -y -q install ' if env.host_type == 'deb' else 'yum -y install ')
    params = packages if type(packages) == str else ' '.join(packages)
    run(cmd + params)

def prefix(node):
    return 'sudo ' if settings.NODES[node]['sudo'] else ''

def create_user(node, user):
    if VERBOSE:
        print "Creating user: ", node, user
    if user:
        with fabset(warn_only=True):
            run(prefix(node) + 'useradd ' + user)

def create_group(node, group):
    if VERBOSE:
        print "Creating group: ", node, group
    if group:
        with fabset(warn_only=True):
            run(prefix(node) + 'groupadd ' + group)

def create_dir(node, path):
    run(prefix(node) + 'mkdir -p ' + path)

def process_project(node, proj):
    if VERBOSE:
        print "Project: ", node, proj
    project = settings.PROJECTS[proj]
    user = project['user']
    create_user(node, user)
    group = project['group']
    create_group(node, group)
    src = project['source']
    if not src:
        raise KeywordError('"source" attribute required')
    dst = project['destination']
    if not dst:
        raise KeywordError('"destination" attribute required')
    create_dir(node, dst)
    rsync_project(local_dir=src, remote_dir=dst)
    run(prefix(node) + ('chown -R %s:%s %s' % (user, group, dst)))
    

def process_modules(node, modules):
    if VERBOSE:
        print "Modules: ", node, modules
    run('pip install ' + ' '.join(modules))

def process_render(node, conf):
    if VERBOSE:
        print "Render: ", node, conf
    create_dir(node, os.path.dirname(conf['destination']))
    upload_template(conf['template'], conf['destination'], context={'name': 'John Doe'}, 
        use_jinja=True, template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "templates")),
        use_sudo = settings.NODES[node]['sudo'])
    

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
    process_packages(node, ['python-pip', 'rsync']) # need for 'module' and 'project' handlers
    process_entity(node, 'NODEDEF', defs)

def deploy(path):
    settings.load(os.path.join(path, 'settings.py'), os.path.join(path, 'nodes.py'))
    for node,defs in settings.NODEDEFS.iteritems():
        if not settings.NODES.has_key(node):
            if settings.OPTIONS['provision'] is not None:
                provision(node)
        env.host_string = '@'.join([settings.NODES[node]['user'], settings.NODES[node]['ip']])
        env.port = 22
        env.user = settings.NODES[node]['user']
        env.host = settings.NODES[node]['ip']
        deploy_node(node, defs)

