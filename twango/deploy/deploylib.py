import sys, os
from fabric.api import run, put, env
from fabric.context_managers import settings as fabset
from fabric.context_managers import cd
from fabric.contrib.project import rsync_project
from fabric.contrib.files import exists, upload_template
from twango.deploy.config import settings
import imp

VERBOSE = True

def item(func):
    "Decorator for define property and verbosity"
    def wrapper(*args, **kwds):
        if VERBOSE:
            print ": ".join([args[0].__class__.__name__, func.__name__])
        return func(*args, **kwds)
    return property(wrapper)


def itemp(func):
    "Decorator for verbosity"
    def wrapper(*args, **kwds):
        if VERBOSE:
            print ": ".join([args[0].__class__.__name__, func.__name__]), args[1:], kwds
        return func(*args, **kwds)
    return wrapper


def provision(node):
    if VERBOSE:
        print 'Provision: ', node
    cmd = env.facts.sudo + ('apt-get update ; apt-get -y -q upgrade' if env.facts.packager == 'deb' else 'yum -y update')
    run(cmd)


class Facts(object):

    def __init__(self):
        self._packager = None
        self._sudo = None

    @property
    def packager(self):
        if self._packager is None:
            with fabset(warn_only=True):
                result = run('rpm -v')
            self._packager = 'deb' if result.failed else 'rpm'
        return self._packager
    
    @property
    def sudo(self):
        if self._sudo is None:
            self._sudo = ''
        return self._sudo

env.facts = Facts()
 
   
class Action(object):

    @itemp
    def create_user(self, user):
        if user:
            with fabset(warn_only=True):
                run(env.facts.sudo + 'useradd ' + user)
    @itemp
    def create_group(self, group):
        if group:
            with fabset(warn_only=True):
                run(env.facts.sudo + 'groupadd ' + group)

    @itemp
    def create_dir(self, path):
        run(env.facts.sudo + 'mkdir -p ' + path)

    @itemp
    def render(self, template, destination, context={}):
        action.create_dir(os.path.dirname(destination))
        path = os.path.join(os.path.dirname(sys.modules['twango'].__file__), 'deploy', 'templates')
        upload_template(template, destination, context, use_jinja=True,
            template_dir = path, use_sudo = env.facts.sudo)

action = Action()


class Package(object):

    @itemp
    def install(self, *packages):
        cmd = ('apt-get -y -q install ' if env.facts.packager == 'deb' else 'yum -y install ')
        params = packages if type(packages) == str else ' '.join(packages)
        run(env.facts.sudo + cmd + params)

package = Package()


class Module(object):

    @itemp
    def install(self, *modules):
        run('pip install ' + ' '.join(modules))

module = Module()


class Service(object):

    @item
    def nginx(self):
        package.install('nginx', 'libpcre3', 'libpcre3-dev', 'libssl-dev')
        version = '1.0.11'
        if not exists('nginx-%s.tar.gz' % version, env.facts.sudo):
            run('wget -c http://nginx.org/download/nginx-%s.tar.gz' % version)
            run('tar -xzf nginx-%s.tar.gz' % version)
        if not exists('nginx-%s' % version + '/Makefile'):
            with cd('nginx-%s' % version):
                run('''./configure --conf-path=/etc/nginx/nginx.conf \
                    --error-log-path=/var/log/nginx/error.log \
                    --pid-path=/var/run/nginx.pid \
                    --lock-path=/var/lock/nginx.lock \
                    --http-log-path=/var/log/nginx/access.log \
                    --http-client-body-temp-path=/var/lib/nginx/body \
                    --http-proxy-temp-path=/var/lib/nginx/proxy \
                    --http-fastcgi-temp-path=/var/lib/nginx/fastcgi \
                    --with-http_stub_status_module \
                    --with-http_flv_module \
                    --with-http_ssl_module \
                    --sbin-path=/usr/sbin \
                ''')
                run('make')
                run(env.facts.sudo + 'make install')

    @item
    def uwsgi(self):
        package.install('python-dev', 'libxml2-dev')
        module.install('uwsgi')
        action.render('uwsgi.conf', '/etc/init/uwsgi.conf')
        with fabset(warn_only=True):
            run(env.facts.sudo + 'service uwsgi start')

service = Service()


class defProject(object):
    def deploy(self, source=None, destination=None, user=None, group=None):
        action.create_user(user)
        action.create_group(group)
        if not source:
            raise KeywordError('"source" attribute required')
        if not destination:
            raise KeywordError('"destination" attribute required')
        action.create_dir(destination)
        rsync_project(local_dir=source, remote_dir=destination)
        run(env.facts.sudo + ('chown -R %s:%s %s' % (user, group, destination)))


def deploy_nodes(nodelist):
    for node, roles in nodelist.iteritems():
        if not settings.NODES.has_key(node):
            if settings.OPTIONS['provision'] is not None:
                provision(node)
        env.host_string = '@'.join([settings.NODES[node]['user'], settings.NODES[node]['host']])
        env.port = 22
        env.user = settings.NODES[node]['user']
        env.host = settings.NODES[node]['host']
        env.facts = Facts()
        for role in roles:
            role()


def deploy(path):
    settings.load(os.path.join(path, 'options.py'), os.path.join(path, 'nodes.py'))
    mod = imp.load_source('init', os.path.join(path, 'deploy.py'))
    thismodule = sys.modules[__name__]
    for symbol in dir(mod):
        setattr(thismodule, symbol, getattr(mod, symbol))
    env.settings = settings
    deploy_nodes(nodes)

