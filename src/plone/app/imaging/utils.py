from zope.component import queryUtility
from Products.CMFCore.interfaces import IPropertiesTool


def getAllowedSizes():
    ptool = queryUtility(IPropertiesTool)
    if ptool is None:
        return None
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

