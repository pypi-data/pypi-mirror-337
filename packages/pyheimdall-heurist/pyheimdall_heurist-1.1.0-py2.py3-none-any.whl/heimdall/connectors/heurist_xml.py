# -*- coding: utf-8 -*-
import heimdall
from heimdall.decorators import get_database
from heimdall.elements import Root, Item, Metadata
from xml.etree import ElementTree as etree
from xml.etree.ElementTree import Element
from urllib.parse import urlparse
from urllib.request import urlopen

"""
Provides connectors to Heurist-formatted XML files (HML).

This module defines an input connector to databases composed in full or in part of such XML files.

:copyright: The pyHeimdall contributors.
:licence: Afero GPL, see LICENSE for more details.
:SPDX-License-Identifier: AGPL-3.0-or-later
"""  # nopep8: E501


@get_database('heurist:xml')
def getDatabase(**options):
    r"""Imports a database from a Heurist XML (HML) file

    :param \**options: Keyword arguments, see below.
    :Keyword arguments:
        * **url** (:py:class:`str`) -- Local ou remote path of the XML file to import
        * **format** (:py:class:`str`, optional) Always ``heurist:xml``
        * **encoding** (:py:class:`str`, optional, default: ``utf-8``) -- ``url`` file encoding
    :return: HERA element tree
    :rtype: :py:class:`xml.etree.ElementTree.Element`

    Usage example: ::

      >>> import heimdall
      >>> tree = heimdall.getDatabase(format='heurist:xml', url='some/input.xml')
      >>> # ... do stuff ...

    .. CAUTION::
       For future compability, this function shouldn't be directly called; as shown in the usage example above, it should only be used through :py:class:`heimdall.getDatabase`.
    """  # nopep8: E501
    url = options['url']
    encoding = options.get('encoding', 'utf-8')
    if is_url(url):
        with urlopen(url) as response:
            content = response.read().decode(encoding)
        # can raise urllib.error.HTTPError (HTTP Error 404: Not Found, ...)
    else:
        with open(url, 'r') as f:
            content = f.read()
        # can raise OSError (file not found, ...)
    target = Builder()
    parser = etree.XMLParser(target=target)
    tree = etree.fromstring(content, parser)
    if options.get('update', True):
        heimdall.util.update_entities(tree)

        def by_id(node):
            return node.attrib['id'] == id_

        for eid, name in target.entity_names.items():
            id_ = eid
            e = heimdall.getEntity(tree, by_id)
            e.name = name
            for aid, name in target.attribute_names.items():
                id_ = aid
                a = heimdall.getAttribute(e, by_id)
                if a is not None:
                    a.name = name
        for pid, name in target.property_names.items():
            id_ = pid
            p = heimdall.getProperty(tree, by_id)
            p.name = name
    return tree


def is_url(path):
    schemes = ('http', 'https', 'file', )
    return urlparse(path).scheme in schemes


class Builder(object):

    def __init__(self):
        self.root = None
        self.ignore = False
        self.inside_metadata = False
        self.ignored_tags = set()
        self.update = None
        self.stack = list()
        self.entity_names = dict()
        self.attribute_names = dict()
        self.property_names = dict()

        self.CREATE = {
            f'hml': self._create_root,
            f'records': self._create_container,
            f'record': self._create_item,
            f'detail': self._create_metadata,
            f'id': self._create_metadata,
            f'type': self._update_item,
            f'title': self._create_metadata,
            }

    @property
    def current(self):
        try:
            return self.stack[-1]
        except IndexError:
            return None

    def start(self, tag, attrib):
        """Called for each opening ``tag`` and their attributes ``attrib``
        """
        tag = self._get_tag(tag)
        if self.inside_metadata:
            # case: we're in <detail> and there's XML in it
            attrs = ' ' if len(attrib) > 0 else ''
            attrs += ' '.join([f'{k}="{v}"' for k, v in attrib.items()])
            self._update_metadata(f'<{tag}{attrs}>')
            return
        if tag == f'detail':
            self.inside_metadata = True
        try:
            element = self.CREATE[tag](tag, attrib)
        except KeyError:
            self.ignored_tags.add(tag)
            self.ignore = True
            return
        if element is None:
            return
        if self.root is None:
            self.root = element
        else:
            self.current.append(element)
        self.stack.append(element)

    def end(self, tag):
        """Called for each closing ``tag``
        """
        tag = self._get_tag(tag)
        if tag == f'detail':
            self.inside_metadata = False
        if self.inside_metadata:
            self._update_metadata(f'</{tag}>')
            return
        if self.ignore:
            self.ignore = False
            return
        if self.update:
            self.update = None
            return
        if type(self.current) is Item:
            eid = self.current.attrib['eid']
            assert eid is not None
            for metadata in self.current.children:
                pid = metadata.attrib.get('pid', None)
                assert pid is not None
                metadata.attrib['aid'] = f'{eid}.{pid}'
            item = self.current
        element = self.stack.pop()

    def data(self, data):
        """Called for each element ``data`` (ie. text)
        """
        if self.inside_metadata:
            self._update_metadata(data)
            return
        if self.ignore:
            return
        if self.update:
            # update current item.eid
            (tag, attr, eid) = self.update
            assert type(self.current) is Item
            eid = eid if eid else data
            self.current.attrib[attr] = eid
            # memorize entity (presumably) human-readable name
            self.entity_names[eid] = data
            return
        if self.current is not None:
            if self.current.text is None:
                self.current.text = data
            else:
                self.current.text += data

    def close(self):
        """Called when all data has been parsed
        """
        # print(f"Ignored tags: {self.ignored_tags}")
        result = self.root
        self.root = None
        self.ignore = False
        self.update = None
        self.stack = list()
        return result

    def _get_tag(self, fulltag):
        # fulltag = "{xmlns}tag" ; we need this function because
        # Heurist can't fix its fucking namespace already
        parts = fulltag.split('}')
        tag = parts[-1]
        xmlns = parts[0][1:]
        return tag

    def _create_root(self, tag, attrib):
        return Root()

    def _create_container(self, tag, attrib):
        return Element('items')

    def _create_item(self, tag, attrib):
        return Item()

    def _create_metadata(self, tag, attrib):
        item = self.current
        if tag == f'id':
            return Metadata(pid='id')
        if tag == f'title':
            return Metadata(pid='title')
        # tag = 'detail'
        pid = attrib['conceptID']
        # memorize attribute and property (presumably) human-readable name
        eid = item.attrib['eid']
        aid = f'{eid}.{pid}'
        property_name = attrib.get('basename', None)
        attribute_name = attrib.get('name', None)
        self.property_names[pid] = property_name
        self.attribute_names[aid] = attribute_name
        return Metadata(pid=pid)

    def _update_item(self, tag, attrib):
        # <type>
        eid = attrib.get('conceptID', None)
        self.update = ('type', 'eid', eid)
        return None

    def _update_metadata(self, data):
        if self.current is not None:
            assert type(self.current) is Metadata
            if self.current.text is None:
                self.current.text = data
            else:
                self.current.text += data


__copyright__ = "Copyright the pyHeimdall contributors."
__license__ = 'AGPL-3.0-or-later'
__version__ = '1.1.0'
__all__ = ['getDatabase', '__version__']


if __name__ == '__main__':
    from os.path import join, dirname, basename, realpath
    base = join(dirname(realpath(__file__)), '..', '..', '..')
    url = join(base, 'tests', 'resources', 'heurist.xml')
    tree = heimdall.getDatabase(url=url, format='heurist:xml')
    heimdall.createDatabase(tree, url='dump.xml', format='hera:xml')
