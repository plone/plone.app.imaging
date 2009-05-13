from zope.component import getUtility
from Products.CMFCore.interfaces import IPropertiesTool


def getAllowedSizes():
    ptool = getUtility(IPropertiesTool)
    props = getattr(ptool, 'imaging_properties', None)
    if props is None:
        return None
    sizes = {}
    for line in props.getProperty('allowed_sizes'):
        line = line.strip()
        if line:
            name, dims = line.split(' ', 1)
            sizes[name.strip()] = tuple(map(int, dims.split(':', 1)))
    return sizes

