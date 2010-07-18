from setuptools import setup, find_packages
from os.path import join

name = 'plone.app.imaging'
path = ['src'] + name.split('.') + ['version.txt']
version = open(join(*path)).read().strip()
readme = open("README.txt").read()
history = open(join('docs', 'HISTORY.txt')).read()

setup(name = name,
      version = version,
      description = 'User-configurable, blob-aware image scaling for Plone.',
      long_description = readme[readme.find('\n\n'):] + '\n' + history,
      classifiers=[
          "Environment :: Web Environment",
          "Framework :: Plone",
          "Framework :: Zope2",
          'Intended Audience :: Developers',
          'Intended Audience :: Other Audience',
          'Intended Audience :: System Administrators',
          "License :: OSI Approved :: GNU General Public License (GPL)",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
        ],
      keywords='images scaling zodb blob plone',
      author='Plone Foundation',
      author_email='plone-developers@lists.sourceforge.net',
      url='http://pypi.python.org/pypi/plone.app.imaging',
      license='GPL version 2',
      packages = find_packages('src'),
      package_dir = {'': 'src'},
      namespace_packages = ['plone', 'plone.app'],
      include_package_data = True,
      install_requires = [
        'setuptools',
        'plone.scale [storage]',
      ],
      extras_require = {'test': ['collective.testcaselayer', ]},
      platforms = 'Any',
      zip_safe = False,
      entry_points = '''
        [z3c.autoinclude.plugin]
        target = plone
      ''',
)
