#!/usr/bin/env python

import os
import sys
import json
import logging

import mapzen.whosonfirst.utils
import mapzen.whosonfirst.machinetag

if __name__ == '__main__':

    import optparse

    opt_parser = optparse.OptionParser()

    opt_parser.add_option('-s', '--source', dest='source', action='store', default=None, help='Directory to read files from')
    opt_parser.add_option('-c', '--categories', dest='categories', action='store', default=None, help='...')

    opt_parser.add_option('-v', '--verbose', dest='verbose', action='store_true', default=False, help='Be chatty (default is false)')
    options, args = opt_parser.parse_args()

    if options.verbose:	
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)    

    categories = os.path.abspath(options.categories)
    source = os.path.abspath(options.source)

    authority = "sg"

    root = os.path.join(categories, authority)

    crawl = mapzen.whosonfirst.utils.crawl(source, inflate=True)

    for feature in crawl:

        props = feature['properties']
        
        stz = mapzen.whosonfirst.machinetag.sanitize()

        for cl in props.get('sg:classifiers', []):

            sg_type = cl.get('type', '')
            sg_category = cl.get('category', '')
            sg_subcategory = cl.get('subcategory', '')

            clean_type = stz.filter_namespace(sg_type)
            clean_category = stz.filter_predicate(sg_category)
            clean_subcategory = stz.filter_value(sg_subcategory)

            process = [
                [ 'namespace', 'simplegeo', 'sg' ],
                [ 'predicate', sg_type, clean_type ],
                [ 'value', sg_category, clean_category ],
            ]

            if clean_subcategory != "":
                
                process.extend([
                    [ 'namespace', sg_type, clean_type ],
                    [ 'predicate', sg_category, clean_category ],
                    [ 'value', sg_subcategory, clean_subcategory ]
                ])
    
            for spec in process:

                type, label, clean = spec

                parent = os.path.join(root, type)
                fname = "%s.json" % clean

                path = os.path.join(parent, fname)

                if os.path.exists(path):
                    continue

                data = {
                    'id': -1,
                    'label': label,
                    'name': clean
                }

                if not os.path.exists(parent):
                    os.makedirs(parent)

                fh = open(path, 'w')
                json.dump(data, fh, indent=2)

                print path
