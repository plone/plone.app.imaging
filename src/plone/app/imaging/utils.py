from zope.component import getUtility
from Products.CMFCore.interfaces import IPropertiesTool


def getAllowedSizes():
    ptool = getUtility(IPropertiesTool)
    sizes = {}
    for line in ptool.imaging_properties.getProperty('allowed_sizes'):
        line = line.strip()
        if line:
            name, dims = line.split(' ', 1)
            sizes[name.strip()] = tuple(map(int, dims.split(':', 1)))
    return sizes

