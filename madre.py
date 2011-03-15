#@+leo-ver=5-thin
#@+node:ville.20110202083633.2349: * @file madre.py

#@+others
#@+node:ville.20110203133009.2366: ** definitions
import os,subprocess

import paramiko
#@+node:ville.20110203133009.2369: ** paramiko misc
rsa_private_key = "/home/ville/ssh.nqs/id_rsa"

def agent_auth(transport, username):
    """
    Attempt to authenticate to the given transport using any of the private
    keys available from an SSH agent or from a local private RSA key file (assumes no pass phrase).
    """
    try:
        ki = paramiko.RSAKey.from_private_key_file(rsa_private_key)
    except Exception, e:
        print 'Failed loading' % (rsa_private_key, e)

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
        self.sshopts='-oStrictHostKeyChecking=no -oUserKnownHostsFile=/dev/null -i /home/ville/ssh.nqs/id_rsa'

        self.user = "user"
        self.host = "192.168.2.15"
        self.port = "22"
        self.IDFILE="~/ssh.nqs/id_rsa"
        self.IDFILEPUB=self.IDFILE + ".pub"


    def connect(self):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(
            paramiko.AutoAddPolicy())    

        self.ssh.connect(self.host, username = self.user, key_filename = rsa_private_key)
        self.ftp = self.ssh.open_sftp()


    def ex(self, c, inp=None ):
        stdin, stdout, stder = self.ssh.exec_command(c)
        if inp is not None:
            stdin.write(inp)
            stdin.close()

        return stdout.read(), stder.read()

    def ex_full(self, c, inp=None):
        cmd = 'python /home/user/cardinal/cardinal_wrapper.py "%s"' % (c.replace('"', r'\"'),)
        out = self.ex(cmd, inp)
        print "Out"
        print out
        
        
    def sshcmd(self, c, inp=None ):
        """ deprecated, ok for key transfer with pw prompt """

        cmd = "ssh %s -p %s %s@%s \"%s\"" % (self.sshopts, self.port, self.user, self.host, c)
        print ">",cmd
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
        os.chdir("/home/ville/ssh.nqs")

        os.system("ssh-keygen -f %s -P \"\" -t rsa" % self.IDFILE)

    def copykey(self):
        self.sshcmd("mkdir -p /home/user/.ssh; /bin/cat >/home/user/.ssh/authorized_keys2", open ("/home/ville/ssh.nqs/id_rsa.pub").read())

    def setup_remote(self):
        print "stub setup"
        self.ex("mkdir -p /home/user/cardinal/state")
        self.ftp.put("cardinal_wrapper.py", "/home/user/cardinal/cardinal_wrapper.py")
    
    def connect2(username, hostname, port):
        self.transport = t = paramiko.Transport((hostname, port))
        t.start_client()
        agent_auth(t, username)            

        return t

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
    out = `r.ex("ls")`
    r.setup_remote()

    print "got",out

if __name__ == "__main__":    
    main()    
#@-others
#@-leo