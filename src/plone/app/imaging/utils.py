from zope.component import queryUtility
from Products.CMFCore.interfaces import IPropertiesTool
from re import compile


pattern = compile(r'^(.*)\s+(\d+)\s*:\s*(\d+)(?:\s+(fill|fit))?$')


def getAllowedSizes():
    sizes_and_crop = getAllowedSizesAndCrops()
    sizes = {}
    for name in sizes_and_crop:
        width, height, crop = sizes_and_crop[name]
        sizes[name] = width, height
    return sizes

def getAllowedSizesAndCrops():
    ptool = queryUtility(IPropertiesTool)
    if ptool is None:
        return None
    props = getattr(ptool, 'imaging_properties', None)
    if props is None:
        return None
    sizes_and_crop = {}
    for line in props.getProperty('allowed_sizes'):
        line = line.strip()
        if line:
            name, width, height, fillfit = pattern.match(line).groups()
            crop = False
            if fillfit=="fill": crop = True
            name = name.strip().replace(' ', '_')
            sizes_and_crop[name] = int(width), int(height), crop

    return sizes_and_crop
    