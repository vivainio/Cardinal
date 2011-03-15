<?xml version="1.0" encoding="utf-8"?>
<?xml-stylesheet ekr_test?>
<leo_file>
<leo_header file_format="2" tnodes="0" max_tnode_index="0" clone_windows="0"/>
<globals body_outline_ratio="0.5" body_secondary_ratio="0.5">
	<global_window_position top="50" left="50" height="500" width="700"/>
	<global_log_window_position top="0" left="0" height="0" width="0"/>
</globals>
<preferences/>
<find_panel_settings/>
<vnodes>
<v t="ville.20110202083633.2345"><vh>NewHeadline</vh></v>
<v t="ville.20110202083633.2346" a="E"><vh>@file cardinal.py</vh></v>
<v t="ville.20110203131933.2356" a="E"><vh>@path /home/ville/nqs/Maemo/4.6.2/madlib/m-cmds</vh>
<v t="ville.20110203131933.2358"><vh>@@edit remote</vh></v>
</v>
<v t="ville.20110203131933.2357" a="E"><vh>@path /home/ville/nqs/Maemo/4.6.2/madlib/ma-cmds</vh>
<v t="ville.20110203133009.2362"><vh>@edit create</vh></v>
<v t="ville.20110203133009.2364"><vh>@edit /home/ville/nqs/Maemo/4.6.2/madlib/ma-create-runtime.sh</vh></v>
</v>
<v t="ville.20110203133009.2363"><vh>copy key</vh></v>
<v t="ville.20110203133009.2368"><vh>@url paramiko</vh></v>
<v t="ville.20110203133009.2370"><vh>@url rsa auth</vh></v>
<v t="ville.20110203133009.2371"><vh>@url how to ssh using paramiko (good)</vh></v>
<v t="ville.20110202083633.2349"><vh>@file madre.py</vh></v>
<v t="ville.20110203133009.2372"><vh>grab ps</vh></v>
<v t="ville.20110203133009.2380"><vh>smaps</vh></v>
<v t="ville.20110304110027.2452"><vh>deploy keys</vh></v>
</vnodes>
<tnodes>
<t tx="ville.20110202083633.2345"></t>
<t tx="ville.20110203131933.2356"></t>
<t tx="ville.20110203131933.2357"></t>
<t tx="ville.20110203131933.2358">@nocolor
#!/bin/sh

# 180 remote -- command set to handle runtime

# This file is part of MADDE
#
# Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
#
# Contact: Riku Voipio &lt;riku.voipio@nokia.com&gt;
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public License
# version 2.1 as published by the Free Software Foundation.
#
# This library is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA
# 02110-1301 USA

. '/home/ville/nqs/Maemo/4.6.2/madlib/madlib.sh' || exit

progname=${MA_COMMAND:-`basename "$0"`}
user=$ml_remote_user
host=
runcommand=
frctty=
verbose=false opt_v=
sshopts='-oPasswordAuthentication=no -oStrictHostKeyChecking=no -oUserKnownHostsFile=/dev/null'

usage ()
{
	case ${1:-} in	0) ev=0 ;;
			*) exec 1&gt;&amp;2; ev=${1:-2} ;;
	esac

	echo
	echo "Usage: $progname [-r RUNTIME] poweron [-fg]| poweroff |"
	echo " send FILE | remove FILE | run [-t] PROGRAM | stop PROGRAM |"
	echo " debug PROGRAM (-c|-s) [ARGS] | mount LOCALDIR |"
	echo " install DEBIAN_PACKAGE | uninstall DEBIAN_PACKAGE | ping"
	echo
	echo " $progname starts and stops the QEMU runtime,"
	echo ' copies files to runtime and runs commands in runtime'
	echo
	echo '  poweron     start QEMU runtime. -fg runs the QEMU in foreground'
	echo '  poweroff    stop QEMU runtime'
	echo '  send        send FILE to runtime'
	echo '  remove      remove FILE from runtime'
	echo '  shell       run login shell on runtime'
	echo '  run         run PROGRAM on runtime. -t gives pseudo tty'
	echo '  stop        stop PROGRAM on runtime'
	echo '  debug       debug PROGRAM on runtime'
	echo '  mount       mount LOCALDIR to runtime'
	echo '  umount      unmount directory mounted by mount'
	echo '  install     install DEBIAN_PACKAGE on runtime'
	echo '  uninstall   uninstall DEBIAN_PACKAGE on runtime'
	echo '  ping        check if runtime is up and connectable'
	echo

	exit $ev
}

_quote_args ()
{
	args=
	for i in "$@"; do
		case $i in
			*'"'*) die "Cannot handle quotes in '$i'" ;;
			*\\*) die "Cannot handle backslashes in '$i'" ;;
		esac
		args="$args\"$i\" "
	done
}

_recmd ()
{
	case $1 in -u) shift; args="$*" ;; *) _quote_args "$@" ;; esac
	verbose warn ssh $frctty $sshopts -p $port $user@$host "$args"
	ssh $frctty $sshopts -p $port $user@$host "$args" || \
		 { warn ssh: exit $?; false; }
}

# set remote file base name
_set_rfbn ()
{
	rfbn=`basename "$1"`
	case $rfbn in *"'"*) die "'$1' contains ':s" ;; esac
}

remote_update ()
{
	remote_wrapper="$ml_madlib_dir/armel/remote-wrapper.sh"
	_recmd -u sh bin/remote-wrapper.sh self_update &lt; "$remote_wrapper"
}


poweron ()
{
	foreground=false
	case ${1:-} in -fg) foreground=true; shift ;; esac
	case ${qemu:-} in '')
		die "Not qemu runtime or qemu runtime configuration error" ;;
	esac
	# Check if ports needed for QEMU are free
	perl "$ml_madlib_dir/checkport.pl" $port $port2 $port3 || \
		{ warn "Cannot create new QEMU!";
		  die "Some of the ports ($port, $port2, $port3) needed for QEMU not available!"; }
	echo "Starting QEMU runtime $runtime"
	echo "This may take some time ..."
	cd "$ml_runtimes_dir/$runtime"
	streq "${QEMU_NOGRAPHIC:-}" 'yes' &amp;&amp; {
		testargs=-nographic
		# -nographic option does not work with -serial option
		qemu_args=`echo $qemu_args | sed 's/ -serial stdio\| -serial con://'`
	} || testargs=
	set_dgles2_backend # do temporary qemu workaround
	$foreground &amp;&amp; env $libpath "$qemu" $testargs $qemu_args ||
		{ env $libpath "$qemu" $testargs $qemu_args &gt;/dev/null 2&gt;&amp;1 &amp; }
}

poweroff ()
{
	echo "This may take some time ..."
	frctty=-t
	_recmd -u sh bin/remote-wrapper.sh $opt_v poweroff
}

sendfile ()
{
	test -f "$1" || die "Cannot find '$1'"
	sum=`"$ml_madbin_dir/md5sum" "$1"`
	case `file "$1"` in *executable*) x=+x ;; *) x= ;; esac
	_set_rfbn "$1"
	_recmd -u sh bin/remote-wrapper.sh $opt_v writefile $x "'$rfbn'" $sum &lt; "$1"
}

remove ()
{
	_set_rfbn "$1"
	_recmd -u sh bin/remote-wrapper.sh $opt_v removefile "'$rfbn'"
}

mount ()
{
	strne "${1:-}" '' || die "
	$progname mount needs local directory as an argument
	which to be mounted on remote filesystem. Enter '.' to
	mount current local directory.
"
	test -d "$1" || die "'$1': not a directory"
	# get "random" secrets
	eval `perl -e 'print "lsec=", rand, " rsec=", rand'`
	not_quiet echo Starting remote mount client
	_recmd -u sh bin/remote-wrapper.sh $opt_v mount $lsec $rsec \
		|| die 'Remote mount client start failed'
	not_quiet echo Starting local mount server
	"$ml_madlib_dir"/utfs-server -l $lsec -r $rsec -c $host:14168 "$1" &amp;
}

umount ()
{
	_recmd -u sh bin/remote-wrapper.sh $opt_v umount
}

run ()
{
	case ${1:-} in -t) frctty=-t; shift ;; esac
	#_quote_args "$@"
	#_recmd -u sh bin/remote-wrapper.sh run "$args"
	_recmd sh bin/remote-wrapper.sh $opt_v run "$@"
}

shell ()
{
	verbose warn ssh $sshopts -p $port $user@$host
	exec ssh $sshopts -p $port $user@$host
}

debug ()
{
	case ${1:-} in
		-s) shift
		    _recmd sh bin/remote-wrapper.sh $opt_v debug \
			gdbserver 0.0.0.0:13219 "$@"
		;;
		-c) shift
		    gdb=${MA_SESSION_DIR:-notset}/bin/gdb
		    test -x "$gdb" || die "Can not find gdb -- target not set?"
		    exec $gdb -ex "set sysroot $SYSROOT_DIR_NATIVE" \
			-ex "target remote $host:13219" "$@"
		;;
		'') die "
	Without options -c or -s debugging is done over ssh connection.

	With options -c and -s remote debugging is done with gdbserver - gdb
	pair:
		Run '$MA_COMMAND debug -s PROGRAM [ARGS]'
		on one terminal, and then
		run '$MA_COMMAND debug -c PROGRAM'
		on another to connect to the remote debugger.
	Note: gdb options are usable with '-c', but, unfortunately not
	when using this commmand to debug over ssh connection.
"		;;
		*) frctty=-t
		   _recmd sh bin/remote-wrapper.sh $opt_v debug gdb "$@"
		;;
	esac
}

stop ()
{
	_recmd -u killall "$1" '&amp;&amp;' sleep 1 '&amp;&amp;' killall -9 "$1" '2&gt;/dev/null'
}

install ()
{
	_set_rfbn "$1"
	_recmd sh -u bin/remote-wrapper.sh $opt_v install "'$rfbn'"
}

uninstall ()
{
	_set_rfbn "$1"
	_recmd sh -u bin/remote-wrapper.sh $opt_v uninstall "'$rfbn'"
}

get_runtime ()
{
	strne "${1:-}" '' &amp;&amp; runtime=$1 || runtime=`mad query runtime`

	_information="$ml_runtimes_dir"/$runtime/information
	if test -f "$_information" ; then
		case `sed 's;^[a-zA-Z0-9_]*=['"'"'a-zA-Z0-9_=:.,/ -]*;;' "$_information"` in
			 '') ;; *) die "Runtime '$runtime' information file has illegal characters" ;; esac
		. "$_information"
		host=$ip
		port=$sshport
		port2=${redirport2:-}
		port3=${redirport3:-}
	else
		case $runtime in
			'') die "No '-r &lt;runtime&gt;' option given nor default runtime set" ;;
			*) die "Runtime '$runtime' not found"
		esac
	fi
	unset _information
}

ping ()
{
	set x `_recmd -u sh bin/remote-wrapper.sh ping $runtime`
	case ${2:-} in 'pong') ;; *) die 'No connection to runtime' ;; esac
	case ${3:-} in '') set x x '&lt;unspesified&gt;' ;; esac
	echo 'pong' $3
}

runtime=
while
	case ${1:-} in
		-v) create_verbose; verbose=true; opt_v=-v ;;
		-r) optreqarg $1 ${2:-}; get_runtime $2; shift; true ;;
		'') usage ;;
		*) false ;;
	esac
do
	shift
done

strne "$runtime" '' || get_runtime

_cmd=$1; shift

verbose warn "runtime: '$runtime'"
$verbose || sshopts="-q $sshopts"

case $_cmd in
	poweron) poweron ${1:+"$@"} ;;
	poweroff) poweroff ;;
	shell) shell ;;
	ping) ping ;;
	debug) debug ${1:+"$@"} ;;
	mount) mount ${1:+"$@"} ;;
	umount) umount ;;
	_remote_update) remote_update ;;
	*) strne "${1:-}" '' || usage
	   # commands that do not have command-related usage message (but needs arg).
	   case $_cmd in
		send) sendfile ${1:+"$@"} ;;
		remove) remove ${1:+"$@"} ;;
		run) run ${1:+"$@"} ;;
		stop) stop ${1:+"$@"} ;;
		install) install ${1:+"$@"} ;;
		uninstall) uninstall ${1:+"$@"} ;;
		cmd) _recmd ${1:+"$@"} ;; # not documented!
		*) usage ;;
	   esac	;;
esac


# Local variables:
# mode: shell-script
# sh-basic-offset: 8
# tab-width: 8
# End:
# vi: set sw=8 ts=8
</t>
<t tx="ville.20110203133009.2363">           ssh -p $qemusshport $sshopts developer@$qemuip \
                '/bin/mkdir -p .ssh; /bin/cat &gt;.ssh/authorized_keys2' 2&gt;/dev/null &lt; "$IDFILEPUB" &amp;&amp; break
                
                
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@         WARNING: UNPROTECTED PRIVATE KEY FILE!          @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
Permissions 0644 for '/home/ville/ssh.nqs/id_rsa' are too open.
It is recommended that your private key files are NOT accessible by others.
This private key will be ignored.
                </t>
<t tx="ville.20110203133009.2368">http://jessenoller.com/2009/02/05/ssh-programming-with-paramiko-completely-different/</t>
<t tx="ville.20110203133009.2370">http://code.activestate.com/recipes/576810-copy-files-over-ssh-using-paramiko/</t>
<t tx="ville.20110203133009.2371">http://www.minvolai.com/blog/2009/09/how-to-ssh-in-python-using-paramiko/</t>
<t tx="ville.20110203133009.2372">import madre
reload(madre)

out = madre.run("ps -o pid -o rss -o vsz -o comm")

p2 = p.insertAsLastChild()
p2.b = out
c.redraw()</t>
<t tx="ville.20110203133009.2380">import madre

out = madre.run('sp_smaps_snapshot')

p2 = p.insertAsLastChild()
p2.b = out
c.redraw()

</t>
<t tx="ville.20110304110027.2452">import madre
reload(madre)
s = madre.ses()
s.copykey()</t>
</tnodes>
</leo_file>
