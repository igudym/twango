import shutil
import os 

def startproject(dest):
    src = os.path.abspath(os.path.dirname(__file__)+"/../template/default/")
    shutil.copytree(src,dest)
