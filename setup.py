#@+leo-ver=4-thin

from distutils.core import setup

datapats = ['pics/*','devbin/*']
packages = ['cardinalsuite']

setup(
    name = 'cardinalsuite',
    version = "0.1",
    author = "Ville M. Vainio",
    author_email = 'vivainio@gmail.com',
    url = '',
    packages = packages,
    package_data = {'cardinalsuite' : datapats },
    description = "Maemo/MeeGo development/tracing frontend",
    long_description = """
Cardinal Suite is a development tool, an ssh-based "remote control" for an
expanding set of Linux devices (Maemo, MeeGo, Harmattan...).
    """,
    scripts = ['cardinal'],

    #entry_points = {
    #    'console_scripts': [
    #    ],

    #'gui_scripts' : [
    # 'leo = leo.core.runLeo:run'
    # ]
    #    }

)
#@-node:ville.20090213231648.1:@thin ~/leo-editor/setup.py
#@-leo
