from twango.deploy.deploy import *

class Project(defProject):

    @item
    def myp(self):
        destination = '/home/web/myp'
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
        project.myp
        action.render('backends.conf', '/etc/nginx/conf.d/backends.conf')
        action.render('site.conf', '/etc/nginx/sites-available/myp.conf', 
            {'project_directory': '/home/web/myp', 'project_domain': '.twango-example.com'})
        with fabset(warn_only=True):
            run(env.facts.sudo + 
                'ln -s /etc/nginx/sites-available/myp.conf /etc/nginx/sites-enabled/myp.conf')
            run(env.facts.sudo + 'rm -f /etc/nginx/sites-enabled/default')
        run(env.facts.sudo + 'service nginx restart')        

        
role = Role()

nodes = {
    'twango-example.com': [ lambda: role.web ] 
}

