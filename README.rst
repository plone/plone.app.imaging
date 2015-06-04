plone.app.imaging
=================

Introduction
------------

This package tries to factor out and re-use the image scaling code from
Archetypes_ into a separate package in order to make it user-configurable
and add support for storing the image data into ZODB blobs_.

  .. _Archetypes: http://plone.org/products/archetypes
  .. _blobs: http://plone.org/products/plone.app.blob


Warning
-------

Version 2.x is for Plone 5 only.


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

1. The ``tag`` method generates a complete image tag::

     <img tal:define="scales context/@@images"
          tal:replace="structure python: scales.tag('image',
                       width=1200, height=800, direction='down')"
          />

   While the first call requires the storage to load the image data
   and extract information for scaling, consecutive calls are cheap
   because the metadata is stored for each call signature.

   The ``direction`` keyword-argument can be used to specify the
   scaling direction. Additional parameters are rendered as element
   attributes (typically: "title" and "alt").

2. For tag generation using predefined scale names this would look like::

     <img tal:define="scales context/@@images"
          tal:replace="structure python: scales.tag('image', scale='mini')"
          />

   This would use the predefined scale size "mini" to determine the desired
   image dimensions, but still allow to pass in extra parameters.

3. The following traversal syntax is a short-cut for tag generation
   for predefined image scales::

     <img tal:replace="structure context/@@images/image/mini" />

4. The same syntax may be used for the original image::

     <img tal:replace="structure context/@@images/image" />

5. The ``scale`` method returns an image scale object useful for
   explicit tag generation::

     <img tal:define="scales context/@@images;
                      thumbnail python: scales.scale('image', width=64, height=64);"
          tal:condition="thumbnail"
          tal:attributes="src thumbnail/url;
                          width thumbnail/width;
                          height thumbnail/height" />

   This would create an up to 64 by 64 pixel scaled down version of the image
   stored in the "image" field.  It also allows for passing in addition
   parameters support by `plone.scale`_'s ``scaleImage`` function, e.g.
   ``direction`` or ``quality``.

   Note that the ``scale`` method loads the actual image data into
   memory on each invocation.

   .. _`plone.scale`: http://pypi.python.org/pypi/plone.scale

6. The image scale object also implements a ``tag`` method::

     <img tal:define="scales context/@@images;
                      scale python: scale.scale('image', width=1200, height=800)"
          tal:replace="structure scale/tag" />

   However, it's recommended to use the ``tag`` method of the image
   scales view directly because it avoids loading the image into memory.

Scaled image direction
~~~~~~~~~~~~~~~~~~~~~~

Three different scaling options are supported with the ``direction`` parameter.

* ``up`` scaling scales the smallest dimension up to the required size
  and crops the other dimension if needed.

* ``down`` scaling starts by scaling the largest dimension to the required
  size and crops the other dimension if needed.

* ``thumbnail`` scales to the requested dimensions without cropping. The
  resulting image may have a different size than requested. This option
  requires both width and height to be specified. `keep` is accepted as
  an alternative spelling for this option, but its use is deprecated.

Scaled image quality
~~~~~~~~~~~~~~~~~~~~

The quality of scaled images can be controlled through the "Imaging" control
panel.

This will only take effect for images that have not been scaled yet. To
re-scale existing images with an updated quality setting, you'l need to go in
the ZMI > ``portal_atct`` > "Image scales" tab, and click "recreate". This
may take a very long time!
