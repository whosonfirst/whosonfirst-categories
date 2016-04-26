#!/usr/bin/env python

import os
import sys
import logging

import json

if __name__ == '__main__':

    whoami = sys.argv[0]
    whoami = os.path.abspath(whoami)

    bin = os.path.dirname(whoami)
    root = os.path.dirname(bin)

    categories = os.path.join(root, "categories")
    meta = os.path.join(root, "meta")

    out = []
    
    for root, dirs, files in os.walk(categories):

        for fname in files:
            
            path = os.path.join(categories, fname)
            fh = open(path, "r")
            
            data = json.load(fh)

            out.append({
                'id': data['id'],
                'name': data['name'],
                'label': data['label']
            })

    fh = sys.stdout
    json.dump(out, fh, indent=2)

    sys.exit(0)
