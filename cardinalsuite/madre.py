#@+leo-ver=5-thin
#@+node:ville.20110202083633.2349: * @file madre.py

#@+others
#@+node:ville.20110203133009.2366: ** definitions
import os,subprocess

import paramiko

import logging
log = logging.getLogger('madre')
#@+node:ville.20110203133009.2369: ** paramiko misc

def rsa_key_dir():
    return os.path.expanduser("~/ssh.cardinal")

def rsa_private_key():    
    key = rsa_key_dir() + "/id_rsa"
    return key

crdroot = '/home/user/cardinal'
   

def agent_auth(transport, username):
    """
    Attempt to authenticate to the given transport using any of the private
    keys available from an SSH agent or from a local private RSA key file (assumes no pass phrase).
    """
    try:
        ki = paramiko.RSAKey.from_private_key_file(rsa_private_key())
    except Exception, e:
        print 'Failed loading' % (rsa_private_key(), e)

    agent = paramiko.Agent()
    agent_keys = agent.get_keys() + (ki,)
    if len(agent_keys) == 0:
        return

    for key in agent_keys:
        print 'Trying ssh-agent key %s' % key.get_fingerprint().encode('hex'),
        try:
            transport.auth_publickey(username, key)
            print '... success!'
            return
        except paramiko.SSHException, e:
            print '... failed!', e

#@+node:ville.20110203133009.2365: ** class RemoteSes
class RemoteSes:
    #@+others
    #@+node:ville.20110202083633.2350: *3* impl
    #sshopts='-oPasswordAuthentication=no -oStrictHostKeyChecking=no -oUserKnownHostsFile=/dev/null -i /home/ville/ssh.nqs/id_rsa'

    def __init__(self):
        self.sshopts='-oStrictHostKeyChecking=no -oUserKnownHostsFile=/dev/null -i %s' % rsa_private_key()

        self.user = "user"
        self.host = "192.168.2.15"
        self.port = "22"
        self.IDFILE=rsa_private_key()
        self.IDFILEPUB=self.IDFILE + ".pub"
    
    def rootdir(self):
        return '/home/%s/cardinal' % self.user        

    def connect(self):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(
            paramiko.AutoAddPolicy())    

        self.ssh.connect(self.host, username = self.user, key_filename = rsa_private_key())
        self.ftp = self.ssh.open_sftp()
        self.rootssh = paramiko.SSHClient()
        self.rootssh.set_missing_host_key_policy(
            paramiko.AutoAddPolicy())    

        self.rootssh.connect(self.host, username = 'root', key_filename = rsa_private_key())


    def ex_root(self,c, inp=None):
        log.debug("ex_root: " + c)
        stdin, stdout, stder = self.rootssh.exec_command(c)
        if inp is not None:
            stdin.write(inp)
            stdin.close()

        return stdout.read(), stder.read()
        
    def ex(self, c, inp=None ):
        log.debug("ex: " + c)
        stdin, stdout, stder = self.ssh.exec_command(c)
        if inp is not None:
            stdin.write(inp)
            stdin.close()

        return stdout.read(), stder.read()

    def ex_raw(self, c, inp = None):
        log.debug("ex_raw: " + c)
        stdin, stdout, stder = self.ssh.exec_command(c)
        if inp is not None:
            stdin.write(inp)
            stdin.close()

        return stdout, stder
        
        
    def invoke_shell(self):
        ch = self.ssh.invoke_shell(width = 500)
        return ch

    def ex_full(self, c, inp=None):
        cmd = 'python %s/bin/cardinal_wrapper.py "%s"' % (self.rootdir(), c.replace('"', r'\"'),)
        out = self.ex_raw(cmd, inp)        
        return out
    
        
    def sshcmd(self, c, inp=None ):
        """ deprecated, ok for key transfer with pw prompt """

        # always use root here, needed for setup
        cmd = "ssh %s -p %s %s@%s \"%s\"" % (self.sshopts, self.port, 'root', self.host, c)
        log.debug("ex: " + cmd)
        out = None
        if inp is None:
            os.system(cmd)

        else:

            p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, close_fds=True)        

            p.stdin.write(inp)
            p.stdin.close()        
            os.waitpid(p.pid,0)[1]
            
        return out        



    """
    def _recmd ()
    {
    	case $1 in -u) shift; args="$*" ;; *) _quote_args "$@" ;; esac
    	verbose warn ssh $frctty $sshopts -p $port $user@$host "$args"
    	ssh $frctty $sshopts -p $port $user@$host "$args" || \
    		 { warn ssh: exit $?; false; }
    }
    """

    def gen_keys(self):
        #os.chdir("/home/ville/ssh.nqs")
        if not os.path.isdir(rsa_key_dir()):
            os.makedirs(rsa_key_dir())
        os.chdir(rsa_key_dir())

        os.system("ssh-keygen -f %s -P \"\" -t rsa" % self.IDFILE)
        os.system("ssh-add %s" % (self.IDFILE,))

    def copykey(self):
        userhome = '/home/%s' % self.user
        cmd = "mkdir -p %s/.ssh /root/.ssh; tee %s/.ssh/authorized_keys2 /root/.ssh/authorized_keys2" % (
            userhome, userhome
            )
        #print cmd
        self.sshcmd(cmd, open (rsa_key_dir() + "/id_rsa.pub").read())
        self.sshcmd("passwd -u " + self.user)
        
    def setup_remote(self):
        print "stub setup"
        self.ex("mkdir -p %s/state %s/bin" % (self.rootdir(), self.rootdir()))
                
        pth = os.path.dirname(__file__) + "/devbin"
        all = os.listdir(pth)
    
        for e in all:
            print "Deploying",e
            self.ftp.put(pth + "/"+ e, self.rootdir() + "/bin/" + e)
        self.ex_root("chown -R %s %s"  % (self.user, self.rootdir()))
    
    def connect2(username, hostname, port):
        self.transport = t = paramiko.Transport((hostname, port))
        t.start_client()
        agent_auth(t, username)            

        return t

    def ping(self):
        ret = os.system("ping -w 5 -c 1 %s" % self.host)
        print "ping ret",ret
        
    def get(self, pth, target):
        log.debug("get: %s => %s" % (pth, target))
        
        self.ftp.get(pth, target)
    def put(self, localpth, target):
        log.debug("put: %s => %s" % (localpth, target))

        self.ftp.put(localpth, target)
    
    def ls(self, d):
        r = [ (a.filename, a) for a in self.ftp.listdir_attr(d)]
        return r
    
    def pkg_install(self, packages):
        
        deb_files = [p for p in packages if p.endswith('.deb')]
        
        if deb_files:
            c = "dpkg -i --force-all " + " ".join(deb_files)
            log.debug(c)
    
            print ">",c
            stdin, stdout, stder = self.rootssh.exec_command(c)
            return stdout, stder
        
        rpm_files = [p for p in packages if p.endswith('.rpm')]
        if rpm_files:
            c = "rpm --replacepkgs -Uvh " + " ".join(rpm_files)
        
            log.debug(c)
                
            stdin, stdout, stder = self.rootssh.exec_command(c)
            return stdout, stder
    
    
        
    #gen_keys()
    #copykey()

    #@-others
#@+node:ville.20110203133009.2377: ** run
_instance = None

def ses():
    global _instance
    if _instance is None:
        _instance = RemoteSes()
    return _instance    

def run(c):
    return ses().ex(c)

#@+node:ville.20110203133009.2367: ** test run
def main():
    r = ses()
    r.connect()
    print "connected"
    out = `r.ex("ls")`
    #print out
    ch = r.invoke_shell("ls")
    print ch
    #print `r.ex("ls")`
    
    ch.send('top\n')
    while 1:
        re = ch.recv(1000)
        print re
    
    #r.setup_remote()

    #print "got",out

if __name__ == "__main__":    
    main()    
#@-others
#@-leo
