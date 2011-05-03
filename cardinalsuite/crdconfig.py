#!/usr/bin/env python

import ConfigParser, os


def parse_config(selected = None):
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
        user = useron

        [handset]
        host = 192.168.2.15
        user = meego
        
        [main]
        defaultdevice = usb
        """)
        open(cf,"w").write(cont)
        log.info("Creating default config file: " + cf)
    
    c.read([cf])
    if selected is None:
        selected = c.get("main", "defaultdevice")
    else:
        selected = str(selected)
        
            
    d['selected_device'] = selected
    
    host = c.get(selected,"host")
    d['host'] = host
    d['user'] = c.get(selected, 'user')
    all = set(c.sections())
    all.discard('main')
    all.discard(selected)    
    
    d['alldevices'] = [selected] + sorted(all)
    return d

