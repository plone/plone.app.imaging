from Products.CMFCore.interfaces import IPropertiesTool
from re import compile
from zope.component import queryUtility


QUALITY_DEFAULT = 88
pattern = compile(r'^(.*)\s+(\d+)\s*:\s*(\d+)(?:\s+(fill|fit))?$')


def getAllowedSizesAndStrategies():
    ptool = queryUtility(IPropertiesTool)
    if ptool is None:
        return None
    props = getattr(ptool, 'imaging_properties', None)
    if props is None:
        return None
    sizes_and_strategies = {}
    for line in props.getProperty('allowed_sizes'):
        line = line.strip()
        if line:
            name, width, height, fillfit = pattern.match(line).groups()
            crop = 'fit'
            if fillfit=='fill':
                crop = 'fill'
            name = name.strip().replace(' ', '_')
            sizes_and_strategies[name] = int(width), int(height), crop
    return sizes_and_strategies


def getAllowedSizes():
    sizes_and_strategies = getAllowedSizesAndStrategies()
    sizes = {}
    for name in sizes_and_strategies:
        width, height, crop = sizes_and_strategies[name]
        sizes[name] = width, height
    return sizes


def getScalingStrategies():
    sizes_and_strategies = getAllowedSizesAndStrategies()
    if sizes_and_strategies is None:
        return {}
    strategies = {}
    for name in sizes_and_strategies:
        width, height, crop = sizes_and_strategies[name]
        strategies[name] = crop
    return strategies


def getQuality():
    ptool = queryUtility(IPropertiesTool)
    if ptool:
        props = getattr(ptool, 'imaging_properties', None)
        if props:
            quality = props.getProperty('quality')
            if quality:
                return quality
    return QUALITY_DEFAULT
