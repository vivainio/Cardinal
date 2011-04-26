#!/usr/bin/env python

import ConfigParser, os


def parse_config():
    d = {}
    c = ConfigParser.ConfigParser()
    cf = os.path.expanduser('~/.cardinal.ini')
    if not os.path.isfile(cf):
        cont = textwrap.dedent("""\
        [usb]
        host = 192.168.2.15
        user = user
        
        [wlan_n900]
        host = 192.168.1.38
        user = user

        [handset]
        host = 192.168.2.15
        user = meego
        
        [main]
        defaultdevice = usb
        """)
        open(cf,"w").write(cont)
        log.info("Creating default config file: " + cf)
    
    c.read([cf])
    default = c.get("main", "defaultdevice")
    d['selected_device'] = default
    
    host = c.get(default,"host")
    d['host'] = host
    d['user'] = c.get(default, 'user')
    return d

