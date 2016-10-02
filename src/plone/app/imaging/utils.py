# -*- coding: utf-8 -*-
from re import compile
from zope.component import queryUtility
from plone.registry.interfaces import IRegistry
from Products.CMFPlone.interfaces.controlpanel import IImagingSchema


QUALITY_DEFAULT = 88
pattern = compile(r'^(.*)\s+(\d+)\s*:\s*(\d+)$')


def getAllowedSizes():
    registry = queryUtility(IRegistry)
    if not registry:
        return None
    settings = registry.forInterface(IImagingSchema, prefix="plone", check=False)
    if not settings.allowed_sizes:
        return None
    sizes = {}
    for line in settings.allowed_sizes:
        line = line.strip()
        if line:
            name, width, height = pattern.match(line).groups()
            name = name.strip().replace(' ', '_')
            sizes[name] = int(width), int(height)
    return sizes


def getQuality():
    registry = queryUtility(IRegistry)
    if registry:
        settings = registry.forInterface(IImagingSchema, prefix="plone", check=False)
        return settings.quality or QUALITY_DEFAULT
    return QUALITY_DEFAULT
