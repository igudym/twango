
OPTIONS = { 
    'provision': 'rackspace',
}

PROVIDERS = {
    'rackspace': {
        'login': 'igudym',
        'key': '342343423423423',
    }
}

SERVICES = {
    'uwsgi': { 
        'packages': ['python-dev', 'libxml2-dev'],
        'modules': ['uwsgi'],
        'render': [
            {
                'template': 'uwsgi.conf', 
                'destination': '/etc/uwsgi/uwsgi.conf',
                'mode': '600',
                'user': 'root',
                'group': 'root',
            }
        ],
    },
    'nginx': {
        'packages': ['nginx'],
        'render': [
            {
                'template': 'nginx.conf', 
                'destination': '/etc/nginx/nginx.conf',
                'mode': '600',
                'user': 'root',
                'group': 'root',
            }
        ],
    }
}

PROJECTS = {
    'myp': {
        'source': 'src',
        'destination': '/home/myp',
        'user': 'web',
        'group': 'web',
    }
}

ROLES = {
    'web': { 
        'packages': ['python', 'python-virtualenv', 'python-pip'],
        'services': ['uwsgi', 'nginx'],
        'projects': [ 'myp' ],
    }
}

NODEDEFS = {
    'twango-example.com': { 'roles': ['web'], }
}

