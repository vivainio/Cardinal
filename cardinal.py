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

garbage = []

import logging
log = logging.getLogger('crd')
def setup_logging():

    # Log everything, and send it to stderr.
    logging.basicConfig(level=logging.DEBUG)
    pm = logging.getLogger("paramiko.transport")
    pm.setLevel(logging.INFO)

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
        cols = 2
        for (i, (title, func)) in enumerate(tools):
            b = QtGui.QPushButton(self.ui.centralwidget)
            b.setText(title)
            self.ui.procLayout.addWidget(b,i/cols, i % cols)
            b.clicked.connect(func)

        tools = self.get_device_tools()
        for (i,(title, func)) in enumerate(tools):
            b = QtGui.QPushButton(self.ui.centralwidget)
            b.setText(title)
            self.ui.deviceLayout.addWidget(b, i/cols, i% cols)
            b.clicked.connect(func)
                    
        self.ui.inpProcName.setText("/bin/ls")
        self.add_actions()
        self.procs = []
        # explorer instances
        self.exps = []
        self.pl = None
        self.dv = None
        self.beamer = None
        cdir = cachedir()
        if not os.path.isdir(cdir):
            os.makedirs(cdir)

        
        
    def add_actions(self):
        self.ui.actionSetup_device.triggered.connect(self.setup_device)
        self.ui.actionCollect_cores.triggered.connect(self.setup_corepattern)

    def setup_device(self):
        print "setup"
        os.system('python devicesetup.py')
        #self.ses.copykey()
        #try:
        #    self.ses.connect()
        #except:
        #    pass
        
        #self.ses.setup_remote()

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
            st['launch_bin'] = str(self.ui.inpProcName.text())
            st['launch_args'] = str(self.ui.inpProcArgs.text())
            
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
        print "CMD",cmd
        def run():
            return self.ses.ex_full(cmd)
        r = RRunner(run)        
        e = self.start_explorer(r, traces)
        return e

    def do_run(self):
        cmd = self.get_cmd()
        print "run", cmd
        self.do_cmd(cmd)

    def add_generic_toggle(self, ex, enablepat = "strace -o {statedir}/strace -p {pid}",
                           disablepat = ""):
        
        
        def generic_toggle(state, s):
            print "Toggle",state,s
            
            pidof = state['pidof']
            d = {'pid': pidof,
                 'statedir' : state['state']}
            
            
            if s == 'enable':
                print "d",d
                cmd = enablepat.format(**d)
                o = self.ses.ex_raw(cmd)
                #print o[1].readline()
                
                garbage.append(o)
                
                #print "toggle res",o
            elif s == 'disable':
                if disablepat:
                    cmd = disablepat.format(**d)
                    o = self.ses.ex_raw(cmd)
                    #print o[1].readline()
                    
                    garbage.append(o)
                else:
                    logging.info("Disable not supported")
            
        
        ex.set_toggle_act("Start trace", "Stop trace", generic_toggle)
        
    def do_strace(self):        
        cmd = self.get_cmd()
        if self.is_deferred():
            exp = self.do_cmd(cmd)
            self.add_generic_toggle(exp, "strace -o {statedir}/strace -p {pid}",                                    
                                    "")
            return 
            
        cmd2 = "strace -t -o {SDIR}/strace %s" % (cmd,)
        print cmd2
        self.do_cmd(cmd2, ['strace'])

    def do_ltrace(self):
        cmd = self.get_cmd()
        if self.is_deferred():
            exp = self.do_cmd(cmd)
            self.add_generic_toggle(exp, "ltrace -t -C -o {statedir}/ltrace -p {pid}",                                    
                                    "")
            return 
        
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
        self.dv.go_url('packages')        
        
    
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
        startfile("%s/sp_smaps.html" % (self.msr_dir(),))        
        
        #print out
    
    def add_rtrace_postprocs(self,ex, deferred=False):
        def resolve_rtrace_leak(state):
            sdir = state['state']
            out = self.ses.ex("sp-rtrace-postproc -l -r -i %s/*.rtrace  > %s/rtrace_resolved.txt" % (
                sdir, sdir))
            print "Ret ",out

        def resolve_rtrace_all(state):
            sdir = state['state']
            out = self.ses.ex("sp-rtrace-postproc -r -i %s/*.rtrace > %s/rtrace_resolved.txt" % (
                sdir, sdir))
            print "Ret ",out
            
        ex.add_postproc("Resolve rtrace (leaks)", resolve_rtrace_leak)
        ex.add_postproc("Resolve rtrace (all)", resolve_rtrace_all)
        
        def rtrace_toggle(state, s):
            print "Toggle",state,s
            pidof = state['pidof']
            if s == 'enable':
                o = self.ses.ex_raw("sp-rtrace -t %d" % pidof)
                print o[1].readline()
                
                garbage.append(o)
                
                #print "toggle res",o
            elif s == 'disable':
                o = self.ses.ex('sp-rtrace -t %d' % pidof)
                garbage.append(o)
                print "disable res",o
            
        
        if deferred:
            
            ex.set_toggle_act("Start trace", "Stop trace", rtrace_toggle)
        else:
            ex.set_toggle_act("", "", None)


    def is_deferred(self):
        return self.ui.cbDefer.isChecked()
        
    def start_rtrace(self,module):
        cmd = self.get_cmd()
        #cmd2 = "strace -t -o {SDIR}/strace %s" % (cmd,)

        if self.is_deferred():
            sstr = ""
        else:
            sstr = "-s "
        cmd2 = "sp-rtrace %s-p %s -o {SDIR} -x %s" % (sstr, module, cmd)
        ex = self.do_cmd(cmd2)
        self.add_rtrace_postprocs(ex, not bool(sstr))
        
        
    def do_rtrace_mem(self):
        self.start_rtrace('memory')

    def do_rtrace_qobject(self):
        self.start_rtrace('qobject')

    def do_rtrace_file(self):
        self.start_rtrace('file')
        
    def do_examine_cores(self):        
        if not self.dv:
            self.dv = dynviewer.DynViewer()
        self.dv.show()
        self.dv.go_url('cores')
        
        print "examine"
        
    def do_beamer(self):
        import beamer
        if not self.beamer:
            self.beamer = beamer.Beamer()
            
        self.beamer.show()
        
    def do_shell(self):
        os.system('gnome-terminal --command="ssh -l root -i /home/ville/ssh.cardinal/id_rsa 192.168.2.15"')        
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
            ('Beamer', self.do_beamer),
            ('Shell (root)', self.do_shell),
            
        ]
        return all
    
    def find_app(self):
        s = str(self.ui.inpProcName.text())
        whi = self.ses.ex("which " + s)
        print "which: " , whi
        trie = whi[0].strip()
        self.ui.inpProcName.setText(trie)
        

if __name__ == "__main__":
    setup_logging()
    app = QtGui.QApplication(sys.argv)
    myapp = ProcLauncher()
    myapp.show()
    logging.debug("App started")
    sys.exit(app.exec_())
