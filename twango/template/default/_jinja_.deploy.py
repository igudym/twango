from twango.deploy.deploylib import *

class Project(defProject):

    @item
    def {{ project_name }}(self):
        destination = '/home/web/{{ project_name }}'
        self.deploy(
            source = 'src',
            destination = destination,
            user = 'web',
            group = 'web',
        )
        put('bootstrap.sh', destination, env.facts.sudo)
        put('requirements.txt', destination, env.facts.sudo)
        with cd(destination):
            run('source bootstrap.sh')

project = Project()

class Role():

    @item
    def web(self):
        service.nginx
        service.uwsgi
        project.{{ project_name }}
        action.render('backends.conf', '/etc/nginx/conf.d/backends.conf')
        action.render('site.conf', '/etc/nginx/sites-available/{{ project_name }}.conf', 
            {'project_directory': '/home/web/{{ project_name }}',
             'project_domain': '{{ project_domain }}',
            }
        )
        with fabset(warn_only=True):
            run(env.facts.sudo + 
                'ln -s /etc/nginx/sites-available/{{ project_name }}.conf ' + 
                '/etc/nginx/sites-enabled/{{ project_name }}.conf')
            run(env.facts.sudo + 'rm -f /etc/nginx/sites-enabled/default')
        run(env.facts.sudo + 'service nginx restart')        

        
role = Role()

nodes = {
    '{{ project_domain }}': [ lambda: role.web ] 
}

