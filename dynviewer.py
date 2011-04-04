#!/usr/bin/env python

from PyQt4 import QtCore, QtGui

import madre

import Ui_DynViewer
import os, re

class DynViewer(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_DynViewer.Ui_DynViewer()
        self.ui.setupUi(self)
        self.ses = madre.ses()
        self.ui.textBrowser.anchorClicked.connect(self.anchor_clicked)
        self.ui.textBrowser.setOpenLinks(False)
        self.pagestack = []
        self.currentpage = None
        self.ui.bBack.clicked.connect(self.go_back)
    def setHtml(self, html):
        self.ui.textBrowser.setHtml(html)
        
    def list_packages(self):
        out,err = self.ses.ex("dpkg -l")
        lines = out.splitlines()[5:]
        
        o = ["<table>"]
        for l in lines:            
            #cols = ['<td>%s</td>' % ent.strip() for ent in l.split(None,3)]
            cols = [ent.strip() for ent in l.split(None,3)]
            o.append('<tr><td><a href="pkg-%s">%s</a></td><td>%s</td></tr>' %
                    (cols[1],cols[1], cols[2]))
            
        o.append('</table>')
        
        self.setHtml("".join(o))

    def list_cores(self):
        coredir = '/home/user/cardinal/cores'
        all = self.ses.ls(coredir)
        print all
        o = ["<table>"]

        for n, attr in all:
            mo = re.match('^core-(.+).(\d+)$', n)
            if not mo:
                continue
            cf = mo.group(0)
            o.append('<tr><td><a href="core://%s/%s">%s</a></td></tr>\n' % (coredir, cf,
                os.path.basename(cf)))
            
        o.append("</table>")
        html = "<pre>" + "".join(o) + "</pre>"
        self.setHtml(html)
        print "set",html
        r = self.ses.ex_root('chown user %s' % (" ".join(coredir + "/" + e[0] for e in all),))
        print r
        
                
    def list_files(self, pkg):
        out, err = self.ses.ex("dpkg -L " + pkg)
        lines = out.splitlines()
        o = []
        for l in lines:
            l = l.strip()
            o.append('<a href="file://%s">%s</a>\n' % (l, l))
            
        self.setHtml("<pre>" + "".join(o) + "</pre>")
        
    def handle_file(self,fname):
        print "fetching",fname
        cloc = str(QtGui.QDesktopServices.storageLocation(QtGui.QDesktopServices.CacheLocation))
        trg = cloc + "/" + os.path.basename(fname)
        self.ses.get(fname, trg)
        os.system("gedit %s &" % (trg))
        
    def handle_core(self, cf):
        """ Handle core file """
        
        print "handle_core",cf
        proc = "top"
        
        mo = re.search('core-(.+)\.(\d+)$', cf)
        bin = mo.group(1)
        pid = mo.group(2)
        
        sdir = "/home/user/cardinal/state/p" + pid
        
        #all = self.ses.ls(sdir)        
        
        cmd = 'gdb -ex "set pagination 0" -ex "bt" --batch %s -c %s' % (bin, cf)
        out = self.ses.ex(cmd)
        print "opened stack", out
        self.setHtml("<pre>%s</pre>" % out[0])
        
    def anchor_clicked(self, url):
        u = str(url.toString())
        self.go_url(u)
        
    def go_back(self):
        print "ps",self.pagestack
        p = self.pagestack.pop()
        self.go_url(p)
        
    def go_url(self, u):
        print "go_url",u
        print "ps",self.pagestack
        self.pagestack.append(self.currentpage)
        self.currentpage = u
        if u.startswith('pkg-'):
            self.list_files(u[4:])
        if u.startswith('file://'):
            self.handle_file(u[7:])
        if u == 'packages':
            self.list_packages()
        if u.startswith('core:'):
            self.handle_core(u[5:])
        if u == 'cores':
            self.list_cores()
            
            
            
            
        
        
