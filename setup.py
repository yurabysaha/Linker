from distutils.core import setup
import py2exe

setup(windows=['ui/main.py'], requires=['selenium'])
