# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

name = 'plone.app.imaging'
readme = open("README.rst").read()
history = open("CHANGES.rst").read()

setup(name = name,
      version='2.1.1',
      description = 'User-configurable, blob-aware image scaling for Plone.',
      long_description = readme[readme.find('\n\n'):] + '\n' + history,
      classifiers=[
          "Development Status :: 5 - Production/Stable",
          "Environment :: Web Environment",
          "Framework :: Plone",
          "Framework :: Plone :: 5.0",
          "Framework :: Plone :: 5.1",
          "Framework :: Plone :: 5.2",
          "Framework :: Zope2",
          "Framework :: Zope :: 4",
          'Intended Audience :: Developers',
          'Intended Audience :: Other Audience',
          'Intended Audience :: System Administrators',
          "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2.7",
          ],
      keywords='images scaling zodb blob plone',
      author='Plone Foundation',
      author_email='plone-developers@lists.sourceforge.net',
      url='https://github.com/plone/plone.app.imaging',
      license='GPL version 2',
      packages = find_packages('src'),
      package_dir = {'': 'src'},
      namespace_packages = ['plone', 'plone.app'],
      include_package_data = True,
      install_requires = [
          'setuptools',
          'plone.scale [storage]',
          'Products.Archetypes',
          'z3c.caching',
          'five.globalrequest'
      ],
      extras_require = {'test':
          ['plone.app.testing',
           'Products.ATContentTypes']},
      platforms = 'Any',
      zip_safe = False,
      entry_points = '''
        [z3c.autoinclude.plugin]
        target = plone
      ''',
      )
