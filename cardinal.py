import sys,os
from PyQt4 import QtCore, QtGui

import madre

import Ui_ProcLauncher

import procexplorer
import threadutil
import proclist
import dynviewer
import traceviewer

from threadutil import RRunner
from cardinalutil import *

class ProcLauncher(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_ProcLauncher.Ui_ProcLauncher()
        self.ui.setupUi(self)
        self.ses = madre.ses()
        
        #self.ses.connect()
        try:
            self.ses.connect()
        except:
            pass


        self.ui.bFindExec.clicked.connect(self.find_app)
        #print "root"
        #print self.ses.ex_root("pwd")
        tools = self.get_tools()
        for title, func in tools:
            b = QtGui.QPushButton(self.ui.centralwidget)
            b.setText(title)
            self.ui.procLayout.addWidget(b)
            b.clicked.connect(func)

        tools = self.get_device_tools()
        for title, func in tools:
            b = QtGui.QPushButton(self.ui.centralwidget)
            b.setText(title)
            self.ui.deviceLayout.addWidget(b)
            b.clicked.connect(func)
                    
        self.ui.inpProcName.setText("/usr/bin/widgetsgallery")
        self.add_actions()
        self.procs = []
        # explorer instances
        self.exps = []
        self.pl = None
        self.dv = None
        cdir = cachedir()
        if not os.path.isdir(cdir):
            os.makedirs(cdir)

        
        
    def add_actions(self):
        self.ui.actionSetup_device.triggered.connect(self.setup_device)

    def setup_device(self):
        print "setup"
        self.ses.copykey()
        try:
            self.ses.connect()
        except:
            pass
        
        self.ses.setup_remote()

    def start_explorer(self, r, tabs):
        e = procexplorer.ProcExplorer()
        
        def setstate():
            e.setState(r.res)
            e.setTabs(tabs)
    
        r.finished.connect(setstate)
        
        e.setRunner(r)
        self.exps.append(e)
        e.show()
        r.start()
        
    def get_cmd(self):
        cmd = str(self.ui.inpProcName.text() + " "+ self.ui.inpProcArgs.text()).strip()
        return cmd
        
    def do_cmd(self, cmd, traces = []):
        def run():
            return self.ses.ex_full(cmd)
        r = RRunner(run)        
        self.start_explorer(r, traces)        

    def do_run(self):
        cmd = self.get_cmd()
        print "run", cmd
        self.do_cmd(cmd)

    def do_strace(self):
        cmd = self.get_cmd()
        cmd2 = "strace -t -o {SDIR}/strace %s" % (cmd,)
        print cmd2
        self.do_cmd(cmd2, ['strace'])

    def do_ltrace(self):
        cmd = self.get_cmd()
        cmd2 = "ltrace -t -C -o {SDIR}/ltrace %s" % (cmd,)
        print cmd2
        self.do_cmd(cmd2, ['ltrace'])
    
    def do_find(self):
        pass

    def do_proclist(self):
        print "process list"
        if not self.pl:
            self.pl = proclist.ProcList()
        
        self.pl.refresh()
        self.pl.show()
        
        
    def do_pkglist(self):
        if not self.dv:
            self.dv = dynviewer.DynViewer()
        self.dv.show()
        self.dv.list_packages()
        
    
    def do_syslog(self):
        tv = self.vsyslog = traceviewer.TraceViewer()
        tv.start_tracking("/var/log/syslog")
        tv.show()
        
    def do_valgrind(self):
        cmd = self.get_cmd()
        cmd2 = 'valgrind --tool=memcheck ' + cmd
        self.do_cmd(cmd2)
        
    def smaps(self):
        out, err = self.ses.ex("sp_smaps_snapshot")
        f = cachedir() + "/sp_smaps.txt"
        open(f,"w").write(out)
        print "Smaps dumped to",f
        #print out
    
    def do_rtrace_mem(self):
        cmd = self.get_cmd()
        #cmd2 = "strace -t -o {SDIR}/strace %s" % (cmd,)

        cmd2 = "sp-rtrace -s -p memory -P '-l -c' -o {SDIR} -x %s" % (cmd,)
        self.do_cmd(cmd2)
        
        
    def not_implemented(self):
        print "Not implemented"
        
    def get_tools(self):
        ni = self.not_implemented
        all = [
            ('run', self.do_run),
            ('strace', self.do_strace),
            ('ltrace', self.do_ltrace),
            ('sp-rtrace (mem)', self.do_rtrace_mem),
            ('sp-rtrace (QObject)', ni),
            ('Valgrind (mem)', self.do_valgrind),

            
            ]
        return all
    def get_device_tools(self):
        ni = self.not_implemented
        all = [
            ('Processes', self.do_proclist),
            ('Packages', self.do_pkglist),
            ('Syslog', self.do_syslog),
            ('sp-smaps', self.smaps)            
            
        ]
        return all
    
    def find_app(self):
        s = str(self.ui.inpProcName.text())
        whi = self.ses.ex("which " + s)
        print "which: " , whi
        trie = whi[0].strip()
        self.ui.inpProcName.setText(trie)
        

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = ProcLauncher()
    myapp.show()
    sys.exit(app.exec_())
