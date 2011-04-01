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
                    
        self.ui.inpProcName.setText("/bin/ls")
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
        self.ui.actionCollect_cores.triggered.connect(self.setup_corepattern)

    def setup_device(self):
        print "setup"
        self.ses.copykey()
        try:
            self.ses.connect()
        except:
            pass
        
        self.ses.setup_remote()

    def setup_corepattern(self):
        print "core pattern"
        r = self.ses.ex_root('echo "/home/user/cardinal/cores/core-%e.%p" > /proc/sys/kernel/core_pattern')
        print r
        
    def parseState(self, s):
        lines = s.splitlines()
        d = {}
        for l in lines:
            pts = l.split("=",1)
            if len(pts) == 2:
                d[pts[0].strip()] = pts[1].strip()
            
        return d    
        

    def start_explorer(self, r, tabs):
        e = procexplorer.ProcExplorer()
        
        def setstate():
            st = self.parseState(r.res[0])
            hd = self.msr_dir() + "/" + st['pid']
            if not os.path.isdir(hd):
                os.makedirs(hd)
                
            st['hostdir'] = hd
            
            e.setState(st)
            e.setTabs(tabs)
    
        r.finished.connect(setstate)
        
        e.setRunner(r)
        self.exps.append(e)
        e.show()
        r.start()
        return e
        
    def get_cmd(self):
        cmd = str(self.ui.inpProcName.text() + " "+ self.ui.inpProcArgs.text()).strip()
        return cmd
        
    def do_cmd(self, cmd, traces = []):
        def run():
            return self.ses.ex_full(cmd)
        r = RRunner(run)        
        e = self.start_explorer(r, traces)
        return e

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
        
    def msr_dir(self):
        lab = str(self.ui.cbMeasurementLabel.currentText()).strip()
        if lab:
            lab = "/" + lab

        mdir = cachedir() + lab        
        if not os.path.isdir(mdir):
            os.makedirs(mdir)
        return mdir
            
        
    def smaps(self):
        out, err = self.ses.ex("sp_smaps_snapshot")
        f = self.msr_dir() + "/sp_smaps.cap"
        open(f,"w").write(out)
        print "Smaps dumped to",f
        cmd = "sp_smaps_analyze " + f
        print ">",cmd
        os.system(cmd)
        os.system("xdg-open %s/sp_smaps.html" % (self.msr_dir(),) )
        
        #print out
    
    def add_rtrace_postprocs(self,ex):
        def resolve_rtrace_leak(state):
            sdir = state['state']
            out = self.ses.ex("sp-rtrace-postproc -i %s/*.rtrace -l -r > %s/rtrace_resolved.txt" % (
                sdir, sdir))
            print "Ret ",out

        def resolve_rtrace_all(state):
            sdir = state['state']
            out = self.ses.ex("sp-rtrace-postproc -i %s/*.rtrace -r > %s/rtrace_resolved.txt" % (
                sdir, sdir))
            print "Ret ",out
            
        ex.add_postproc("Resolve rtrace (leaks)", resolve_rtrace_leak)
        ex.add_postproc("Resolve rtrace (all)", resolve_rtrace_all)

    def start_rtrace(self,module):
        cmd = self.get_cmd()
        #cmd2 = "strace -t -o {SDIR}/strace %s" % (cmd,)

        cmd2 = "sp-rtrace -s -p %s -o {SDIR} -x %s" % (module, cmd)
        ex = self.do_cmd(cmd2)
        self.add_rtrace_postprocs(ex)
        
        
    def do_rtrace_mem(self):
        self.start_rtrace('memory')

    def do_rtrace_qobject(self):
        self.start_rtrace('qobject')

    def do_rtrace_file(self):
        self.start_rtrace('file')
        
    def do_examine_cores(self):
        print "examine"
    def not_implemented(self):
        print "Not implemented"
        
    def get_tools(self):
        ni = self.not_implemented
        all = [
            ('run', self.do_run),
            ('strace', self.do_strace),
            ('ltrace', self.do_ltrace),
            ('sp-rtrace (mem)', self.do_rtrace_mem),
            ('sp-rtrace (QObject)', self.do_rtrace_qobject),
            ('sp-rtrace (file)', self.do_rtrace_file),
            ('Valgrind (mem)', self.do_valgrind),
            
            ]
        return all
    def get_device_tools(self):
        ni = self.not_implemented
        all = [
            ('Processes', self.do_proclist),
            ('Packages', self.do_pkglist),
            ('Syslog', self.do_syslog),
            ('sp-smaps', self.smaps),
            ('Examine cores', self.do_examine_cores),
            
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
