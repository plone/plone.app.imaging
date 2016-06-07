Changelog
=========

2.0.4 (2016-06-07)
------------------

Fixes:

- Fix tests to not scale ``gif`` images, which were converted to ``jpeg`` imaged until ``plone.scale`` version < 2.
  Use ``png`` images for testing instead, which works for all versions of plone.scale.
  [thet]


2.0.3 (2016-02-20)
------------------

Fixes:

- Fix test to not check for the concrete WebDAV content type header.
  Needed for Zope 4 compatibility.
  [thet]


2.0.2 (2016-01-08)
------------------

New:

- Added documentation for what the 'direction' parameter actually
  does.  [shadowmint]


2.0.1 (2015-11-26)
------------------

Fixes:

- Fixed incompatibilities with five.pt and chameleon (closes `#16`_).
  [rodfersou, maurits]

- Fixed 404 NotFound error when accessing image scales via webdav.
  [maurits]


2.0.0 (2015-05-11)
------------------

- Move control panel to Products.CMFPlone
  [vangheem]

- Remove unused import.
  [gforcada]

- re-adding imaging doctests.
  [tomgross]


1.1.2 (2014-10-23)
------------------

- portet tests to plone.app.testing
  [tomgross]


1.1.1 (2014-04-13)
------------------

- Disable csrf protection when scale is generated and traversed to.
  [vangheem]


1.1.0 (2014-02-23)
------------------

- Cache image scales using the plone.stableResource ruleset
  when they are accessed via UID-based URLs.
  [davisagli]

- Move propertysheet imaging_properties and the corresponding
  utilities to Products.CMFPlone.
  https://github.com/plone/plone.app.contenttypes/issues/82
  [pbauer]

- Generate Progressive JPEG.
  [kroman0]


1.0.9 (2013-06-13)
------------------

- Make getQuality always return an integer.


1.0.8 (2013-05-23)
------------------

- Make the quality of scaled images configurable through the configlet.
  https://dev.plone.org/ticket/13337
  [khink]


1.0.7 (2013-03-05)
------------------

* Avoid hard dependency on ATContentTypes.
  [davisagli]

1.0.6 (2012-04-15)
------------------

* Avoid loading an image scale object in order to generate a tag. It's
  expensive because it loads the image data into memory. The
  documentation has been updated to reflect that this is the most
  efficient usage of the API.

1.0.5 - 2011-04-03
------------------

* Fix test now `scale=None` does not raise exception.
  [elro]

1.0.4 - 2011-03-22
------------------

* Add a tag method to @@images to simplify tagging of full sized images.
  [elro]

* Make scale=None return the original image wrapped as an ImageScaling object.
  [elro]

1.0.3 - 2011-02-14
------------------

- Avoid breaking on startup if PIL is not present.
  [davisagli]

1.0.2 - 2011-02-10
------------------

- Add getAvailableSizes and getImageSize to the @@images view.
  [elro]

1.0.1 - 2011-01-03
------------------

- Protect the control panel with a custom permission,
  "Plone Site Setup: Imaging", instead of the generic "Manage portal".
  [davisagli]

1.0 - 2010-07-18
----------------

- Use the standard libraries doctest module.
  [hannosch]

- Update license to GPL version 2 only.
  [hannosch]

1.0b11 - 2010-07-01
-------------------

- Fix issue with creating scales based on Image objects that are storing their
  data as chained Pdata objects.
  [davisagli]

- Avoid using the deprecated five:implements directive.
  [hannosch]

1.0b10 - 2010-05-01
-------------------

- Use plone i18n domain instead of plone.app.imaging domain for the
  MessageFactory. This closes http://dev.plone.org/plone/ticket/10478
  [vincentfretin]

- Fix dependency on `plone.scale` to get requirements for the scale storage.
  [witsch]

- Fix logic bug in url traversal code for image scales.
  This fixes http://plone.org/products/plone.app.imaging/issues/1
  [ramonski, witsch]

- Add support for custom scales for "News Item" content.
  This refs http://dev.plone.org/plone/ticket/10250
  [pelle, witsch]

- Removed dependency declaration for the unused uuid distribution.
  [hannosch]

- Fix control panel definition so that its icon shows up again.
  [witsch]


1.0b9 - 2010-04-10
------------------

- Add new syntax options for generating image scales based on ideas
  borrowed from `plone.scale`, also improving caching and invalidation.
  [witsch]

- Provide sizes for `plone.namedfile` if it's installed.
  [davisagli]

- Restore possibility to define per-field image scale sizes.
  This refs http://dev.plone.org/plone/ticket/10159
  [huub_bouma, witsch]


1.0b8 - 2010-03-06
------------------

- Convert test setup to use `collective.testcaselayer`.
  [witsch]

- Add monkey-patch for `createScales` in order to fix recreation of scales.
  This refs http://dev.plone.org/plone/ticket/10186
  [witsch]


1.0b7 - 2009-12-03
------------------

- Swallow resizing exceptions if that flag is set on the image field.
  [matthewwilkes]

- Add test to make sure traversal to scales in path expressions still works.
  [davisagli, witsch]


1.0b6 - 2009-11-18
------------------

- Corrected ill-formed msgid that contained a double quote.
  [hannosch]


1.0b5 - 2009-11-15
------------------

- Allow white space within image scale definitions.
  This fixes http://dev.plone.org/plone/ticket/9207
  [amleczko]


1.0b4 - 2009-10-29
------------------

- Refactor default scale handler to make it more reusable for the
  blob-enabled version in `plone.app.blob`
  [witsch]


1.0b3 - 2009-08-26
------------------

- Fix compatibility issue with Plone 4.0.
  [witsch]

- Revert deferral of monkey-patching and traversal adapter registration
  to package installation time.
  [witsch]


1.0b2 - 2009-07-08
------------------

- Register traversal handler locally to avoid problems without the
  corresponding monkey patch in place.  Please see the second issue in
  http://plone.org/products/plone.app.blob/issues/19 for more info.
  [witsch]

- Replaced a getUtility with a queryUtility call in getAllowedSizes.
  [hannosch]


1.0b1 - 2009-05-14
------------------

- Add fallback for determining available image sizes to avoid breaking
  sites which haven't installed the package yet.
  [witsch]


1.0a2 - 2008-09-22
------------------

- Fix `getAvailableSizes` to not depend on `sizes` field-attribute.
  [witsch]


1.0a1 - 2008-08-12
------------------

- Initial version
  [witsch]

- Initial package structure.
  [zopeskel]

.. _`#16`: https://github.com/plone/plone.app.imaging/issues/16
