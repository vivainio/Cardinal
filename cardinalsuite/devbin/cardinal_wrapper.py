import os,sys,optparse,subprocess,shlex
import resource

def setdirs():
    global cdir
    cdir = os.path.expanduser("~/cardinal")
    subdirs = ['cores', 'inbox', 'outbox']
    for sd in subdirs:
        d = cdir + "/" + sd
        if not os.path.isdir(d):
            os.makedirs(d)
            
    

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
    fakepid = os.getpid()
    sdir = "%s/state/s%d" % (cdir, fakepid)
    if os.path.isdir(sdir):
        os.rm
    os.makedirs(sdir)
    of = open(sdir + "/out","w")
    ef = open(sdir + "/err","w")
    cmd = cmd.replace("{SDIR}", sdir)
    args = shlex.split(cmd)
    # state line for host end
    print "cmd=%s|||state=%s|||pid=%s" % (cmd, sdir, fakepid)
    p =  subprocess.Popen(args, shell=False, stdout = of, stderr=ef,
      preexec_fn=setlimits )
    pid = str(p.pid)
    open(sdir + "/.pid","w").write("%s\n" % pid)
    open(sdir + "/.meta", "w").write("cmd=%s\nbin=%s\n" % (cmd, cmd.split(None,1)[0]))
    
    sldir = "%s/state/p%s" % (cdir, pid)
    os.symlink(sdir, sldir)

setdirs()        
setenv()
launch(sys.argv[1])    
