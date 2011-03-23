import sys
from PyQt4 import QtCore, QtGui

import madre

import Ui_ProcLauncher

import procexplorer
import threadutil
import proclist
from threadutil import RRunner

class ProcLauncher(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_ProcLauncher.Ui_ProcLauncher()
        self.ui.setupUi(self)
        self.ses = madre.ses()
        
        try:
            self.ses.connect()
        except:
            pass


        self.ui.bFindExec.clicked.connect(self.find_app)
        print "root"
        print self.ses.ex_root("pwd")
        tools = self.get_tools()
        for title, func in tools:
            b = QtGui.QPushButton(self.ui.centralwidget)
            b.setText(title)
            self.ui.verticalLayout.addWidget(b)
            b.clicked.connect(func)

        tools = self.get_device_tools()
        for title, func in tools:
            b = QtGui.QPushButton(self.ui.centralwidget)
            b.setText(title)
            self.ui.deviceOpLayout.addWidget(b)
            b.clicked.connect(func)
                    
        self.ui.inpProcName.setText("/usr/bin/widgetsgallery")
        self.add_actions()
        self.procs = []
        # explorer instances
        self.exps = []
        self.pl = None
        
        
    def add_actions(self):
        self.ui.actionSetup_device.triggered.connect(self.setup_device)

    def setup_device(self):
        print "setup"
        self.ses.copykey()
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
        
    def do_cmd(self, cmd, traces = []):
        def run():
            return self.ses.ex_full(cmd)
        r = RRunner(run)        
        self.start_explorer(r, traces)        

    def do_run(self):
        cmd = self.ui.inpProcName.text()
        print "run", cmd
        self.do_cmd(cmd)

    def do_strace(self):
        cmd = self.ui.inpProcName.text()
        cmd2 = "strace -t -o {SDIR}/strace %s" % (cmd,)
        print cmd2
        self.do_cmd(cmd2, ['strace'])

    def do_ltrace(self):
        cmd = self.ui.inpProcName.text()
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
        
        
    
    def get_tools(self):
        all = [
            ('run', self.do_run),
            ('strace', self.do_strace),
            ('ltrace', self.do_ltrace),
            ]
        return all
    def get_device_tools(self):
        all = [
            ('Processes', self.do_proclist),
            
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
