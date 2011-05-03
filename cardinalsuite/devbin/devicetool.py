#!/usr/bin/env python
""" Do various preparational tasks on device

Yeah, this is probably not the most modular approach

Usage:

devicetool.py command "argument string" (format of
argument string is tool specific), as is stdin handling

"""

import sys,logging, os

def c(cmd):
    os.system(cmd)

# maemo tools

def assert_file(fname, content):
    import textwrap
    if os.path.exists(fname):
        logging.info("File already exists:" + fname)
        return
        
    f = open(fname, "w")
    f.write(textwrap.dedent(content))
    f.close()

def prepare_repos_fremantle():
    assert_file("/etc/apt/sources.list.d/toolrepo.crd.list", """\
                # fremantle tools
                deb http://repository.maemo.org fremantle/tools free non-free
                # fremantle tools sources
                deb-src http://repository.maemo.org fremantle/tools free non-free                
                """)
    c('apt-get -q --yes --force-yes update')
    
def install_helpers_fremantle():
    c("apt-get -q --yes --force-yes install kernel-modules-debug maemo-debug-scripts strace ltrace "
      "sp-smaps-measure "
      )

_platform = None

def platform():
    global _platform
    if _platform is not None:
        return _platform
    if os.path.isfile("/etc/apt/sources.list.d/hildon-application-manager.list"):
        _platform = "maemo5"
    else:
        _platform = "meego"
        
    return _platform
        
    
def preparetools():
    p = platform()
    if p == "maemo5":
        prepare_repos_fremantle()
        
        install_helpers_fremantle()
    else:
        logging.warn("Don't know how to prepare tools for platform " + p)

def main():
    
    cmd = sys.argv[1]
    if cmd == "preparetools":
        preparetools()
    

if __name__ == '__main__':
    main()