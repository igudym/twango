from fabric.api import run, env
from fabric.network import disconnect_all
from fabric.context_managers import settings

env.host_string = 'root@50.56.242.105'

def set_host_type():
    with settings(warn_only=True):
	    result = run('rpm -v')
    env.host_type = 'deb' if result.failed else 'rpm'

def install(packages):
    cmd = 'apt-get -y -q install ' if env.host_type == 'deb' else 'yum -y install '
    params = packages if type(packages) == str else ' '.join(packages)
    run(cmd + params)

def update():
    cmd = 'apt-get update ; apt-get -y -q upgrade' if env.host_type == 'deb' else 'yum -y update'
    run(cmd)

def init_host():
    update()
    install(['python-dev', 'python-virtualenv', 'python-pip'])
    run('pip install https://github.com/igudym/twango/tarball/master')

if __name__ == "__main__":
    try:
        set_host_type()
        init_host();
    finally:
        disconnect_all()

