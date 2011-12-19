import sys
VERBOSE = True

def action(func):
"Decorator for define property and verbosity"
    def wrapper(*args, **kwds):
        if VERBOSE:
            print ": ".join([args[0].__class__.__name__, func.__name__])
        return func(*args, **kwds)
    return property(wrapper)

def actionp(func):
"Decorator for verbosity"
    def wrapper(*args, **kwds):
        if VERBOSE:
            print ": ".join([args[0].__class__.__name__, func.__name__])
        return func(*args, **kwds)
    return wrapper

class Package(object):
    def install(self, *packages):
        if VERBOSE:
            print 'Install packages: ', ' '. join(packages)
#        cmd = prefix(node) + ('apt-get -y -q install ' if env.host_type == 'deb' else 'yum -y install ')
#        params = packages if type(packages) == str else ' '.join(packages)
#        run(cmd + params)
package = Package()

class Module(object):
    def install(self, *modules):
        if VERBOSE:
            print 'Install modules: ', ' '. join(modules)
        run('pip install ' + ' '.join(modules))

module = Module()

class Service(object):
    @action
    def nginx(self):
        package.install('nginx')
        run('wget -c http://nginx.org/download/nginx-1.0.11.tar.gz');
        run('tar -xzf nginx-1.0.11.tar.gz')
        with env.cd('nginx-1.0.11':
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
            run('make install')

    @action
    def uwsgi(self):
        module.install('uwsgi')

service = Service()


class Project(object):
    def _deploy(source=None, destination=None, user=None, group=None)
        create_user(node, user)
        create_group(node, group)
        if not source:
            raise KeywordError('"source" attribute required')
        if not destination:
            raise KeywordError('"destination" attribute required')
        create_dir(destination)
        rsync_project(local_dir=source, remote_dir=destination)
        run(prefix(node) + ('chown -R %s:%s %s' % (user, group, destination)))

    @action
    def myp(self):
        _deploy(
            source: 'src',
            destination: '/home/web/myp',
            user: 'web',
            group: 'web',
        )

project = Project()

class Role():
    @action
    def web(self):
        package.install('python', 'python-virtualenv')
        service.nginx
        service.uwsgi
        project.myp

role = Role()

role.web

