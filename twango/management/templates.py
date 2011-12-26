import shutil
import os 
import glob
import jinja2

def unprefix(filename):
    path, name = os.path.split(filename)
    return os.path.join(path, name[8:])

def startproject(dest):
    """
     
    """
    src = os.path.abspath(os.path.dirname(__file__)+"/../template/default/")
    print "copying src "+src+" to "+dest 
    shutil.copytree(src,dest)
    
    names = glob.glob(os.path.join(dest, '_jinja_.*'))
    for name in names:
        if name[-4:] != '.pyc':
            print 'Processing jinja template ', name
            tmpl = jinja2.Template(open(name).read())
            res = tmpl.render(project_name = dest, project_domain = dest+'.com')
            open(unprefix(name), 'w').write(res)
        os.remove(name)

