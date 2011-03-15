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
<v t="ville.20110202083633.2346" a="E"><vh>@auto cardinal.py</vh></v>
<v t="ville.20110203131933.2356" a="E"><vh>@path /home/ville/nqs/Maemo/4.6.2/madlib/m-cmds</vh>
<v t="ville.20110203131933.2358"><vh>@@edit remote</vh></v>
</v>
<v t="ville.20110203131933.2357" a="E"><vh>@path /home/ville/nqs/Maemo/4.6.2/madlib/ma-cmds</vh>
<v t="ville.20110203133009.2362"><vh>@@edit create</vh></v>
<v t="ville.20110203133009.2364"><vh>@@edit /home/ville/nqs/Maemo/4.6.2/madlib/ma-create-runtime.sh</vh></v>
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
<t tx="ville.20110203133009.2362">@nocolor
#!/bin/sh

# 150 create -- create target cross-compilation environment or runtime

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

#set -x

progname=${MA_COMMAND:-`basename "$0"`}

usage ()
{
	case ${1:-} in	0) ev=0 ;;
			*) exec 1&gt;&amp;2; ev=${1:-2} ;;
	esac
	echo
	echo "Usage: $progname [-q] TARGET [-s] [-r] [-f] [-tc TOOLCHAIN -sr SYSROOT -rt RUNTIME -qt QTTOOLS]"
	echo "       $progname [-q] RUNTIME [-e] [-a ADDRESS ]"
	echo
	echo ' Options:'
	echo
	echo '    -q   quiet operation'
	echo '    -s   set as default (target only)'
	echo '    -r   create matching runtime (target only)'
	echo '    -e   extract only (runtime only) (DANGEROUS!)'
	echo '    -f   attempt to fetch missing toolchain/sysroot/runtime'
	echo '    -tc TOOLCHAIN'
	echo '         either complete path to toolchain archive or just archive'
	echo '         name without extension'
	echo '    -sr SYSROOT'
	echo '         either complete path to sysroot archive or just archive'
	echo '         name without extension'
	echo '    -rt RUNTIME'
	echo '         runtime to be bound to this target'
	echo '    -qt QTTOOLS'
	echo '         either complete path to Qt tools archive or just archive'
	echo '         name without extension'
	echo '    -a ADDRESS'
	echo '         IP address or hostname of the device used as a remote target'
	echo '         This option is mandatory if the runtime is a device'
	echo
	echo ' In case of user-given toolchain and sysroot, target name'
	echo ' must begin with '"'my'".
	echo
	echo ' There are two types of runtimes - devices and QEMU runtimes.'
	echo ' In case of QEMU runtime only preconfigured runtime names are used.'
	echo ' Use command '"'mad list runtimes'"' to see available QEMU runtime names.'
	echo
	exit $ev
}

qflag= vflag=-v
case ${1:-} in -q) create_quiet; qflag=-q vflag=; shift ;; esac

name=
sysroot= toolchain= qttools=
address= runtime=
ffetch=false
extractonly=false
nodefault=true noruntime=true
while case ${1:-} in
	-s)	nodefault=false ;;
	-r)	noruntime=false ;;
	-f)	ffetch=true ;;
	-e)	extractonly=true ;;
	-tc)	optreqarg $1 ${2:-}; toolchain=$2 ; shift ;;
	-sr)	optreqarg $1 ${2:-}; sysroot=$2 ; shift ;;
	-a)	optreqarg $1 ${2:-}; address=$2 ; shift ;;
	-rt)	optreqarg $1 ${2:-}; runtime=$2 ; shift ;;
	-qt)	optreqarg $1 ${2:-}; qttools=$2 ; shift ;;
	'')	false ;;
	*)	streq "$name" '' || die "$progname: '$1': unknown option."
		name=$1 ;;
     esac
do
	shift
done

case $name in
	'')	warn "No target/runtime name defined"; usage ;;
	*' '*)	die "Target/runtime name '$1' contains spaces" ;;
esac

case `echo $name | tr -d 'a-zA-Z0-9_.,+-'` in
	'') ;;
	*) die "Target/runtime name '$1' has illegal characters" ;;
esac


# can not have both target and runtime options
test  x != "x$sysroot$toolchain" -a x != "x$address" &amp;&amp; usage

q_type= q_sysroot= q_toolchain=
q_ccxopts='arch-spesific-default' # mkgccspecs.sh checks gcc if not given...
q_qttools= q_arch= q_os=
q_runtime= q_image= q_qemu= q_args=
eval `perl -e "use Madde::Query; query '$name'" 2&gt;/dev/null`

runtime_for_target ()
{
	strne "${1:-}" '' || die "No runtime name defined. Can not create one"
	$extractonly &amp;&amp; flags="$qflag -e" || flags=$qflag
	sh "$0" $flags $1
}

cnf=true own=false
case $q_type in
	target)
		case $sysroot$toolchain in '') ;;
			*) die "Preconfigured target '$name' does not accept sysroot/toolchain option"
		esac

		# If target is already created and user wants create runtime, skip target
		# creation, because it fails when target exist
		if test -d "$ml_targets_dir/$name" -a "$noruntime" = false
		then
			echo "Target already created, continue to create runtime"
		else
			"$ml_madlib_dir/ma-create-target.sh" $cnf $name "$q_sysroot" "$q_toolchain" "$q_ccxopts" "$q_runtime" "$q_qttools" "$q_arch" "$q_os" $ffetch
		fi

		$nodefault || mad set $vflag $name
		$noruntime || runtime_for_target $q_runtime
		exit 0 ;;
	runtime)
		case $address in '') ;;
			*) die "QEMU runtime '$name' does not accept address option"
		esac
		exec "$ml_madlib_dir/ma-create-runtime.sh" $cnf $name "$q_image" "$q_qemu" "$q_args" "$address" $ffetch $extractonly ;;
	'') ;;
	*) die "Unknown item type '$q_type' for '$name'" ;;
esac

# Not found from configuration.
case $sysroot$toolchain in '') ;;
	*) "$ml_madlib_dir/ma-create-target.sh" $own $name "$sysroot" "$toolchain" "$q_ccxopts" "$runtime" "$qttools" "" "" $ffetch
	   $nodefault || mad set $vflag $name
	   $noruntime || runtime_for_target $runtime
	   exit 0 ;;
esac

case $address in '') ;;
	*) exec "$ml_madlib_dir/ma-create-runtime.sh" $own $name no-image no-qemu no-args "$address" $ffetch $extractonly;;
esac

die "No predefined target/runtime '$name' found".


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
<t tx="ville.20110203133009.2364">@language shell
#!/bin/sh

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
. '/home/ville/nqs/Maemo/4.6.2/madlib/ma-create-lib.sh' || exit

progname=${MA_COMMAND:-`basename "$0"`}
IDFILE=$HOME/.ssh/id_rsa
IDFILEPUB=${IDFILE}.pub
sshopts='-q -oPasswordAuthentication=no -oStrictHostKeyChecking=no -oUserKnownHostsFile=/dev/null'
initabletsshopts='-q -oStrictHostKeyChecking=no -oUserKnownHostsFile=/dev/null'
defsshport=22
qemusshport=6666
redirport2=13219
redirport3=14168
qemuip=127.0.0.1
scriptname=`basename "$0"`

cnf=$1 runtime=$2 image=$3 qemu=$4 args=$5
address=$6 ffetch=$7 extractonly=$8

test $qemu = "no-qemu" || {
	# Mac OS Leopard uses different qemu than newer one(s).
	case $ml_os in darwin)
		case `host_uname -s -r` in Darwin' '9*)
			qemu=`echo "$qemu" | sed 's/darwin/darwin_9/'`
		esac ;;
	esac
	# Remove suffix (tar.gz) from the end of $qemu
	tar_basename "$qemu" # sets $_bn
	qemubn=$_bn
	qemu_dir=$ml_tools_dir/$qemubn

	case $ml_os in
		linux)	qemu_bin_dir='/bin'
			qemulibpath="LD_LIBRARY_PATH=$qemu_dir/lib";;
		darwin) qemu_bin_dir='/bin'
			qemulibpath=DYLD_LIBRARY_PATH="$qemu_dir/lib" ;;
		*)	qemu_bin_dir= qemulibpath= ;;
	esac
	qemu_bin_dir_native=`echo $ml_tools_dir_native/$qemubn$qemu_bin_dir|tr '\\\\' /`
	qemu_bin_dir=$qemu_dir$qemu_bin_dir
	# add mad tcp redir extensions
	args="$args -net nic -net user,hostfwd=tcp:$qemuip:$qemusshport-:$defsshport,hostfwd=tcp:$qemuip:$redirport2-:$redirport2,hostfwd=tcp:$qemuip:$redirport3-:$redirport3"

}

gen_ssh_keys ()
{
	if test ! -f "$IDFILEPUB"; then
		echo "Generating ssh keys, this may take some time ..."
		test -d "$HOME/.ssh" || { mkdir "$HOME/.ssh"; chmod 700 "$HOME/.ssh"; }
		ssh-keygen -f "$IDFILE" -P "" -t rsa
		if test $? -ne 0; then
			die "Generating ssh keys failed"
		fi
		echo "Keys generated successfully"
	fi
}

configure_runtime ()
{
	ssh -p $1 $2 developer@$3 &gt;/dev/null 2&gt;&amp;1 '
		rm -f bin/remote-wrapper.sh bin/utfs-client'

	scp -P $1 $2 -oConnectTimeout=600 "$ml_madlib_dir/armel/remote-wrapper.sh" \
		"$ml_madlib_dir/armel/utfs-client" developer@$3:bin &gt;/dev/null 2&gt;&amp;1 \
		|| die 'Copying setup files to runtime failed'

	ssh -p $1 $2 developer@$3 &gt;/dev/null 2&gt;&amp;1 '
		chmod 755 bin/utfs-client
		bin/devrootsh grep -q ^root:: /etc/passwd &amp;&amp; bin/devrootsh usermod -p "*" root
		bin/devrootsh grep -q ^developer:: /etc/passwd &amp;&amp; bin/devrootsh usermod -p "*" developer
		true' || die 'Configuring runtime failed'
}

qemu_trap ()
{
	rv=$?
	trap '' 0 HUP INT TERM
	heavy_rmdir "$ml_tools_dir/$qemu.wip"
	exit $rv
}

runtime_trap ()
{
	rv=$?
	trap '' 0 HUP INT TERM
	heavy_rmdir "$ml_runtimes_dir/$runtime.wip"
	exit $rv
}

running_qemu_trap ()
{
	rv=$?
	trap '' 0 HUP INT TERM
	cd "$ml_runtimes_dir"
	heavy_rmdir "$ml_runtimes_dir/$runtime.wip" || true
	qemupid=`ps ax | grep $qemu |awk '/grep|'$scriptname'/ {next} {print $1}'`
	streq "$qemupid" '' || kill -9 $qemupid || true
	heavy_rmdir "$ml_runtimes_dir/$runtime"
	exit $rv
}

create_qemu_info_file ()
{
	set_dgles2_backend # do temporary qemu workaround

	{ echo "qemu='$qemu_bin_dir/$qemubn'"
	  echo "qemu_path_native='$qemu_bin_dir_native/$qemubn'"
	  echo "libpath='$qemulibpath'"
	  echo "qemu_args='$args'"
	  echo "ip='$qemuip'"
	  echo "sshport='$qemusshport'"
	  echo "redirport2='$redirport2'"
	  echo "redirport3='$redirport3'"
	  echo "tcpportmap='$qemusshport:22 $redirport2:$redirport2 $redirport3:$redirport3'"
	} &gt; "$ml_runtimes_dir/$runtime/information"
}

create_qemu_runtime ()
{
	test ! -d "$ml_runtimes_dir/$runtime" || {
		$extractonly || die_with_premature_msg '' $runtime "QEMU runtime '$runtime' already exists."
		# Regenerate infromation file if the runtime directory exists and 'extractonly'
		# option is set
		create_qemu_info_file
		return
	}
	# cache_check_fetch modifies $image, sets $image_ar
	cache_check_fetch '' image $ffetch

	# cache_check_fetch modifies $qemu, sets $qemu_ar
	cache_check_fetch "$ml_tools_dir" qemu $ffetch
	#extract  qemu to tools/&lt;qemu&gt; directory
	test -d "$ml_tools_dir" || mkdir "$ml_tools_dir"

	test -d "$ml_tools_dir/$qemu" || {
		mkdir "$ml_tools_dir/$qemu.wip"
		trap qemu_trap 0 HUP INT TERM
		not_quiet echo Working on $qemu

		"$ml_madlib_dir/untar-helper.pl" "$qemu_ar" \
			"$ml_tools_dir/$qemu.wip"

		heavy_mv "$ml_tools_dir/$qemu.wip" "$ml_tools_dir/$qemu"
		trap - 0 HUP INT TERM
	}

	# extract the file to runtimes/&lt;runtime-name&gt; directory
	test -d "$ml_runtimes_dir" || mkdir "$ml_runtimes_dir"
	test ! -d "$ml_runtimes_dir/$runtime.wip" \
		|| die_with_premature_msg .wip $runtime "QEMU runtime '$runtime' creation ongoing."
	mkdir "$ml_runtimes_dir/$runtime.wip"
	trap runtime_trap 0 HUP INT TERM
	echo Extracting QEMU runtime $runtime
	# 'image_ar' variable is set in cache_check_fetch() function
	# This variable keeps inside the complete archive file name
	"$ml_madlib_dir/untar-helper.pl" \
		"$image_ar" "$ml_runtimes_dir/$runtime.wip"

	if ! test -x "$qemu_bin_dir"/$qemu
	then
		rm -rf "$qemu_bin_dir"/$qemu$ml_dotexe
		# Trust that there is just one...
		/bin/ln "$qemu_bin_dir"/qemu-system-* "$qemu_bin_dir"/$qemu$ml_dotexe || :
		test -x "$qemu_bin_dir"/$qemu || die "Cannot find $qemu binary"
	fi

	trap running_qemu_trap 0 HUP INT TERM
	heavy_mv "$ml_runtimes_dir/$runtime.wip" "$ml_runtimes_dir/$runtime"
	create_qemu_info_file
	cd "$ml_runtimes_dir/$runtime"
	streq "${QEMU_NOGRAPHIC:-}" 'yes' &amp;&amp; {
		testargs=-nographic
		# -nographic option does not work with -serial option
		args=`echo $args | sed 's/ -serial stdio\| -serial con://'`
	} || testargs=

	# XXX fix at better time.
	$extractonly &amp;&amp; { trap - 0; return; } || true

	# Check if ports needed for QEMU are free
	perl "$ml_madlib_dir/checkport.pl" $qemusshport $redirport2 $redirport3 || \
		{ warn "Cannot create new QEMU!";
		  die "Some of the ports ($qemusshport, $redirport2, $redirport3) needed for QEMU not available!"; }
	# start qemu
	echo "Starting QEMU for ssh setup ..."
	echo "This may take some time ..."

	env $qemulibpath "$qemu_bin_dir/$qemu" $testargs $args &gt;/dev/null 2&gt;&amp;1 &amp;
	qemuon=
	for _ in 1 2 3 4 5 6 7 8 9 10; do
		perl "$ml_madlib_dir/checkport.pl" $qemusshport || { qemuon=1; break; }
		sleep 1
	done
	case $qemuon in '') die "QEMU startup failed" ;; esac

	# Setup passwordless login towards the device if not setup yet
	gen_ssh_keys

	# takes a while to start up qemu
	# this is is an infinite loop if ssh fails
	while sleep 5; do
		ssh -p $qemusshport $sshopts developer@$qemuip \
		'/bin/mkdir -p .ssh; /bin/cat &gt;.ssh/authorized_keys2' 2&gt;/dev/null &lt; "$IDFILEPUB" &amp;&amp; break
	done

	echo "Connection to QEMU up, performing initial setup"
	configure_runtime $qemusshport "$sshopts" $qemuip

	trap - 0
	echo "QEMU runtime '$runtime' created!"
}

device_trap ()
{
	rv=$?
	trap '' 0 HUP INT TERM
	warn "Creating runtime '$runtime' with address '$address' failed"
	heavy_rmdir "$ml_runtimes_dir/$runtime"
	exit $rv
}

create_device_runtime ()
{
	case $address in
		'') die No IP address defined ;;
		*' '*) die "IP address '$address' contains spaces" ;;
	esac

	trap device_trap 0 HUP INT TERM
	# Setup passwordless login towards the device if not setup yet
	gen_ssh_keys
	ip=$address
	sshport=$defsshport
	ssh -p $sshport $initabletsshopts developer@$ip \
		'/bin/mkdir -p .ssh; /bin/cat &gt;.ssh/authorized_keys2' 2&gt;/dev/null &lt; "$IDFILEPUB" \
		|| die "ssh to developer@$ip failed - exit"

	configure_runtime $sshport "$initabletsshopts" $ip
	# Create the info file to runtimes/&lt;runtime-name&gt; directory
	test -d "$ml_runtimes_dir" || mkdir "$ml_runtimes_dir"
	test -d "$ml_runtimes_dir/$runtime" || mkdir "$ml_runtimes_dir/$runtime"
	{ echo "ip='$ip'"
	  echo "sshport='$sshport'"
	} &gt; "$ml_runtimes_dir/$runtime/information"
	trap - 0
	echo "Device runtime '$runtime' initialized!"
}

case $image in
	no-image)
	     streq "$address" '' &amp;&amp; die "The device runtime requires address to be defined"
	     create_device_runtime
	     ;;
	*)   streq "$address" '' || die "No address needed for QEMU runtime"
	     create_qemu_runtime
	     ;;
esac
touch "$ml_trigger"

# Local variables:
# mode: shell-script
# sh-basic-offset: 8
# tab-width: 8
# End:
# vi: set sw=8 ts=8
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
