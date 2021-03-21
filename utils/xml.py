""" Contains some code related to XML """
from lxml import etree


def pretty_xml(text, encoding='utf-8'):
    """ Add indent to the XML text """
    encoding     = encoding
    root = etree.fromstring(text)
    etree.indent(root)
    return etree.tostring(root).decode(encoding)

