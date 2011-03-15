import sys
from PyQt4 import QtCore, QtGui

import madre

import Ui_ProcLauncher

class RRunner(QtCore.QThread):
    def __init__(self, f, parent = None):

        QtCore.QThread.__init__(self, parent)
        self.f = f

    def run(self):
        self.res = self.f()


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

        self.ui.bLaRun.clicked.connect(self.do_run)
        self.ui.bLaStrace.clicked.connect(self.do_strace)
        self.ui.inpProcName.setText("/usr/bin/widgetsgallery")
        self.add_actions()
        self.procs = []
    def add_actions(self):
        self.ui.actionSetup_device.triggered.connect(self.setup_device)

    def setup_device(self):
        print "setup"
        self.ses.copykey()
        self.ses.setup_remote()

    def do_cmd(self, cmd):
        def run():
            return self.ses.ex_full(cmd)
        r = RRunner(run)
        r.start()
        self.procs.append(r)

    def do_run(self):
        cmd = self.ui.inpProcName.text()
        print "run", cmd
        self.do_cmd(cmd)

    def do_strace(self):
        cmd = self.ui.inpProcName.text()
        cmd2 = "strace -o {SDIR}/strace %s" % (cmd,)
        print cmd2
        self.do_cmd(cmd2)


    def do_find(self):
        pass


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = ProcLauncher()
    myapp.show()
    sys.exit(app.exec_())
