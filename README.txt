plone.app.imaging
=================

Introduction
------------

This package tries to factor out and re-use the image scaling code from
Archetypes_ into a separate package in order to make it user-configurable
and add support for storing the image data into ZODB blobs_.

In addition it provides support for pluggable transformation chains (e.g.
for cropping).  Please see section `Image transforms`_ for details how to
use or define such transformations.

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


New-style image scales
----------------------

`plone.app.imaging` introduces new ways of using image scales in your
templates.  There are several variants you can pick from depending on how
much flexibility/convenience you need:

1. for full control you may do the tag generation explicitly::

     <img tal:define="image context/@@images/image;
                      thumbnail python: image.scale(width=64, height=64);"
          tal:condition="thumbnail"
          tal:attributes="src thumbnail/url;
                          width thumbnail/width;
                          height thumbnail/height" />

   This would create an up to 64 by 64 pixel scaled down version of the image
   stored in the "image" field.  It also allows for passing in addition
   parameters support by `plone.scale`_'s ``scaleImage`` function, e.g.
   ``direction`` or ``quality``.

   .. _`plone.scale`: http://pypi.python.org/pypi/plone.scale

2. for automatic tag generation with extra parameters you would use::

     <img tal:define="image context/@@images/image"
          tal:replace="structure python: image.scale(width=1200, height=800,
                       direction='down').tag()" />

3. for tag generation using predefined scale names this would look like::

     <img tal:define="image context/@@images/image"
          tal:replace="structure python: image.scale('mini').tag()" />

   This would use the predefined scale "mini" to determine the desired
   image dimensions, but still allow to pass in extra parameters.

4. a convenience short-cut for option 3 can be used::

     <img tal:replace="structure context/@@images/image/mini" />

5. and lastly, the short-cut can also be used to render the unscaled image::

     <img tal:replace="structure context/@@images/image" />


Image transforms
----------------

TODO this needs editing!

scaling is a transform, so ``img.scale(width=80,height=80)`` is equivalent to
``img.transform(name='scale',width=80,height=80)``

package shipped with another transform named `crop` that XXX describe what it does

     <img tal:define="img context/@@images/<imageFieldName>"
          tal:replace="structure python: img.crop(width=128,
                       height=128).tag()" />
   
transforms even can be combined dynamically. In the following example we
first crop an image and apply a (not yet existent) grayscale transform
afterwards::

     <img tal:define="img context/@@images/<imageFieldName>"
          tal:replace="structure python: img.crop(width=128,
                       height=128).grayscale().tag()" />



