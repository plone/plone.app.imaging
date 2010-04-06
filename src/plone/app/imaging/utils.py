from zope.component import queryUtility
from Products.CMFCore.interfaces import IPropertiesTool
from re import compile


pattern = compile(r'^(.*)\s+(\d+)\s*:\s*(\d+)$')


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
            name, width, height = pattern.match(line).groups()
            name = name.strip().replace(' ', '_')
            sizes[name] = int(width), int(height)
    return sizes
