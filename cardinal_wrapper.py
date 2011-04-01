import os,sys,optparse,subprocess
import resource

def setdirs():
    global cdir
    cdir = "/home/user/cardinal"

def setenv():
    os.environ["DISPLAY"]=":0"
    if not os.path.isfile("/tmp/session_bus_address.user"):
        return
    
    for l in open("/tmp/session_bus_address.user"):
        if l.startswith('export'):
            parts = l[7:].split('=', 1)
            if len(parts) == 2:
                var, val = parts
                os.environ[var.strip()] = val.strip()

def setlimits():
    print "Setting resource limit in child (pid %d)" % os.getpid()
    resource.setrlimit(resource.RLIMIT_CORE, (-1, -1)) 

def launch(cmd):
    global cdir
    sdir = "%s/state/%d" % (cdir, os.getpid())
    os.makedirs(sdir)
    of = open(sdir + "/out","w")
    ef = open(sdir + "/err","w")
    cmd = cmd.replace("{SDIR}", sdir)
    
    p =  subprocess.Popen(cmd, shell=False, stdout = of, stderr=ef,
      preexec_fn=setlimits )
    open(sdir + "/pid","w").write("%s\n" % p.pid)
    print "cmd=%s\nstate=%s\npid=%s" % (cmd, sdir,p.pid)

setdirs()        
setenv()
launch(sys.argv[1])    
