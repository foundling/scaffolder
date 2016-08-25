# -*- coding: utf-8 -*-

import os

import utils

def create_file(node):
    ''' Create a regular file if node has NoneType for children.  Otherwise, creates a directory. '''

    if os.path.exists(node['path']):
        print('Error, the directory {} already exists'.format(node['path']))
        sys.exit(1) 

    if node['children'] is None:
        open(node['path'], 'w').close()
    else:
        os.mkdir(node['path'])

def make_config_processor(config_path=None):
    ''' Takes relative name of config file in ~/home directory ''' 

    full_path = os.path.abspath( os.path.join(os.path.expanduser('~'), config_path) )

    try:
        with open(full_path) as config_file:
            hooks = dict([ map(str.strip, line.split('=')) for line in config_file  if line.strip() ])

    except IOError as E:
        print('Could not open config file.')
        print E

    def process_config_hooks(node):
        ''' on each node, if there's a match in the config settings, that file is created. '''

        filename = node['value'] 
        if filename in hooks:

            try:
                with open( hooks[filename], 'r' ) as src_file:

                    try:
                        with open( node['path'], 'w' ) as dst_file:
                            dst_file.write( src_file.read() ) 

                    except IOError as E:
                        print('Could not open destination file.')
                        print E

            except IOError as E:
                print('Could not open superdir hooks file.')
                print E


    return process_config_hooks