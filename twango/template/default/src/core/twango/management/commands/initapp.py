import os

from django.core.management.base import copy_helper, CommandError, LabelCommand
from django.utils.importlib import import_module
from django.conf import settings

def copy_helper(style, app_or_project, name, directory, other_name=''):
    """
    Copies either a Django application layout template or a Django project
    layout template into the specified directory.

    """
    # style -- A color style object (see django.core.management.color).
    # app_or_project -- The string 'app' or 'project'.
    # name -- The name of the application or project.
    # directory -- The directory to which the layout template should be copied.
    # other_name -- When copying an application layout, this should be the name
    #               of the project.
    import re
    import shutil
    other = {'project': 'app', 'app': 'project'}[app_or_project]
    if not re.search(r'^[_a-zA-Z]\w*$', name): # If it's not a valid directory name.
        # Provide a smart error message, depending on the error.
        if not re.search(r'^[_a-zA-Z]', name):
            message = 'make sure the name begins with a letter or underscore'
        else:
            message = 'use only numbers, letters and underscores'
        raise CommandError("%r is not a valid %s name. Please %s." % (name, app_or_project, message))
    top_dir = os.path.join(directory, name)
    try:
        os.mkdir(top_dir)
    except OSError, e:
        raise CommandError(e)

    # Determine where the app or project templates are. Use
    # django.__path__[0] because we don't know into which directory
    # django has been installed.
    template_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)+'/../'), 'conf', '%s_template' % app_or_project)
    print template_dir
    for d, subdirs, files in os.walk(template_dir):
        relative_dir = d[len(template_dir)+1:].replace('%s_name' % app_or_project, name)
        if relative_dir:
            os.mkdir(os.path.join(top_dir, relative_dir))
        for subdir in subdirs[:]:
            if subdir.startswith('.'):
                subdirs.remove(subdir)
        for f in files:
            if not f.endswith('.py'):
                # Ignore .pyc, .pyo, .py.class etc, as they cause various
                # breakages.
                continue
            path_old = os.path.join(d, f)
            path_new = os.path.join(top_dir, relative_dir, f.replace('%s_name' % app_or_project, name))
            fp_old = open(path_old, 'r')
            fp_new = open(path_new, 'w')
            fp_new.write(fp_old.read().replace('{{ %s_name }}' % app_or_project, name).replace('{{ %s_name }}' % other, other_name))
            fp_old.close()
            fp_new.close()
            try:
                shutil.copymode(path_old, path_new)
                _make_writeable(path_new)
            except OSError:
                sys.stderr.write(style.NOTICE("Notice: Couldn't set permission bits on %s. You're probably using an uncommon filesystem setup. No problem.\n" % path_new))

def _make_writeable(filename):
    """
    Make sure that the file is writeable. Useful if our source is
    read-only.

    """
    import stat
    import sys
    if sys.platform.startswith('java'):
        # On Jython there is no os.access()
        return
    if not os.access(filename, os.W_OK):
        st = os.stat(filename)
        new_permissions = stat.S_IMODE(st.st_mode) | stat.S_IWUSR
        os.chmod(filename, new_permissions)


def update_configuration(package,app_name):
    """
    This takes in a template settings file, and generates a new settings file from that template
    """
    f = open(settings.PROJECT_DIR+"/urls.py","a")
    f.write("urlpatterns = urlpatterns + patterns('',(url(r'^"+app_name+"/'"+",include('src.apps"+".".join(package)+"."+app_name+".urls'))),) \n")
    f.close()
    try: 
        f = open(settings.PROJECT_DIR+"/settings/25-added_apps.py","a")
    except:
        f = open(settings.PROJECT_DIR+"/settings/25-added_apps.py","w")
        
    f.write("""
INSTALLED_APPS += (
    'apps"""+".".join(package)+"."+app_name+"""',
    ) \n""")

class Command(LabelCommand):
    help = "Creates a Django app directory structure for the given app name in the current directory."
    args = "[appname]"
    label = 'application name'

    requires_model_validation = False
    # Can't import settings during this command, because they haven't
    # necessarily been created.
    can_import_settings = False

    def handle_label(self, app_name, directory=None, **options):
        package = app_name.split('.')
        app_name = package.pop()
         
        if directory is None:
            directory = os.getcwd() + '/apps/'
            
            for pdir in package:
                directory += pdir + '/'
                if not os.path.exists(directory):
                    os.mkdir(directory)
                    init = open(directory+'__init__.py', 'w')
                    init.close()
                
            print directory

        # Determine the project_name by using the basename of directory,
        # which should be the full path of the project directory (or the
        # current directory if no directory was passed).
        project_name = os.path.basename(directory)
        if app_name == project_name:
            raise CommandError("You cannot create an app with the same name"
                               " (%r) as your project." % app_name)

        # Check that the app_name cannot be imported.
        try:
            import_module(app_name)
        except ImportError:
            pass
        else:
            raise CommandError("%r conflicts with the name of an existing Python module and cannot be used as an app name. Please try another name." % app_name)

        copy_helper(self.style, 'app', app_name, directory, project_name)
        update_configuration(package,app_name)

class ProjectCommand(Command):
    help = ("Creates a Django app directory structure for the given app name"
            " in this project's directory.")

    def __init__(self, project_directory):
        super(ProjectCommand, self).__init__()
        self.project_directory = project_directory

    def handle_label(self, app_name, **options):
        super(ProjectCommand, self).handle_label(app_name, self.project_directory, **options)

