plone.app.imaging
=================

Introduction
------------

This package tries to factor out and re-use the image scaling code from
Archetypes_ into a separate package in order to make it user-configurable
and add support for storing the image data into ZODB blobs_.

  .. _Archetypes: http://plone.org/products/archetypes
  .. _blobs: http://plone.org/products/plone.app.blob


Installation
------------

The easiest way to use this package is when working with installations
based on `zc.buildout`_.  Here you can simply add the package to your "eggs"
and "zcml" options, run buildout and restart your `Plone`_ instance.

  .. _`zc.buildout`: http://pypi.python.org/pypi/zc.buildout/
  .. _`Plone`: http://www.plone.org/

Alternatively you can use the following configuration file to extend an
existing buildout::

  [buildout]
  extends = buildout.cfg

  [instance]
  eggs += plone.app.imaging
  zcml += plone.app.imaging

After that you should be able to "quick-install" the package via the
"Add-on products" section of `Plone`_'s configuration panel ("Site setup").
