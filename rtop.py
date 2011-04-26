#!/usr/bin/env python



""" test for threadutil 'repeater' """

from PyQt4 import QtCore

import madre,sys

import threadutil

ses = madre.ses()

ses.connect()

from threadutil import Repeater

def main():
    app=QtCore.QCoreApplication(sys.argv)
    ch = ses.invoke_shell("ls")
    print ch
    #print `r.ex("ls")`
    
    ch.send('top\n')
    
    def f():
        print "call"
        return ch.recv(1000)
        
    rep = Repeater(f)
    
    def frag(r):
        print "frag",r
    
    rep.fragment.connect(frag)
    rep.start()
    
    app.exec_()                                            
    
main()            


