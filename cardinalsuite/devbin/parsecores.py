#!/usr/bin/env python

import os,re

coredir = "/home/user/cardinal/cores"


cores = os.listdir(coredir)
for c in cores:
    mo = re.match('^core-(.+).\d+$')
    if not mo:
        continue
    proc = mo.group(1)
    pid = mo.group(2)
    






