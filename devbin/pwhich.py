#!/usr/bin/env python



""" Scan for executable binary in several places """

import sys,os

def parse_desktop_file(fname):
    d = {}
    for l in open(fname):
        parts = l.split("=",1)
        if len (parts ) < 2:
            continue
        k,v= parts
        d[k] = v
    return d        
    

def pwhich(spat):
    # try real which
    
    matches = []
    wh = os.popen("which -a "+spat).readlines()
    matches.extend((a.strip(), '') for a in wh)
    
    # scan desktop files
    c = 'grep -ril "%s" /usr/share/applications' % spat    
    dfiles = os.popen(c).readlines()
    for f in dfiles:
        f = f.strip()
        if not f.endswith('.desktop'):
            continue
        
        d = parse_desktop_file(f)
        bin = d.get('Exec', "").strip()
        name = d.get("Name", "").strip()
        
        matches.append((bin, name))
        
    return matches

def main():
    pat = sys.argv[1]
    all = pwhich(pat)
    print "\n".join(a[0]+";" + a[1] for a in all)    
    
main()    
    
