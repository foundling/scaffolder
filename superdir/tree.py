import os
import utils
import pdb

class Tree:

    def __init__(self, indent_size=None, output_dir=None, base_path=None):

        if os.path.exists(output_dir):
            raise IOError('The directory {} already exists'.format(self.output_dir))

        self.indent_size = indent_size
        self.output_dir = output_dir
        self.base_path = base_path
        self.data = None
        self.root = None

    def build_tree(self):
        ''' Derive parent/child hierarchy from current and previous lines' indentation relationship.  '''

        virtual_root = self._make_new_node(
            parent      = None,
            children    = [],
            value       = 'virtual_root',
            path        = self.base_path
        )
        root = self._make_new_node(
            parent      = virtual_root,
            children    = [],
            value       = self.output_dir, 
            path        = os.path.join(self.base_path, self.output_dir)
        )
        virtual_root['children'].append(root)

        parent_node = virtual_root
        prev_indent = -1
        for line in self.data:

            cur_indent = utils.get_indent(line, self.indent_size)
            filename = utils.get_dirname(line) if utils.is_dir(line) else utils.get_filename(line)


            ### Find Parent Node of this Line - Put this in a function ###

            # indent, so this is directory
            if cur_indent > prev_indent:
                parent_node = parent_node['children'][-1]

            # unindent, so this could be anything, but it's in some other part of the tree
            elif cur_indent < prev_indent:
                distance = prev_indent - cur_indent
                parent_node = self._find_ancestor(parent_node, distance)

            child = self._make_new_node(
                parent   = parent_node, 
                children = [] if utils.is_dir(line) else None,
                value    = filename,
                path     = os.path.join(parent_node['path'], filename)
            ) 

            parent_node['children'].append(child)
            prev_indent = cur_indent

        self.root = virtual_root

    def walk(self, callback):
        ''' Walk tree and call callback on each node. '''

        def _walk(tree):

            children = tree['children']

            for child in children:
                callback(child)

                if child['children'] is not None:
                    _walk(child)

        tree = self.root
        _walk(tree)

    def load_data(self, data):
        ''' Load the input data and clean it. '''

        self.data = utils.clean(data)

    def _make_new_node(self, parent=None, value=None, children=None, path=''):
        ''' create a new node. if children is Nonetype, node is treated as a leaf. '''
        return  dict(parent=parent, value=value, children=children, path=path)

    def _find_ancestor(self, start_node, parents_to_visit):
        ''' use indentation level relative to previous line to find ancestor.'''
        current_node = start_node

        while (parents_to_visit > 0):
            current_node = current_node['parent']
            parents_to_visit -= 1

        return current_node
