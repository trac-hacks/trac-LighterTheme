from setuptools import find_packages, setup

version='0.3'

try:
    long_description = open("README.txt").read()
except:
    long_description = ''
try:
    long_description += open("CHANGES.txt").read()
except:
    pass

setup(name='trac-LighterTheme',
      version=version,
      description="A light, Bootstrap-inspired theme for Trac",
      long_description=long_description,
      author='Ethan Jucovy, Jacqueline Arasi',
      author_email='ejucovy@gmail.com',
      url='http://trac-hacks.org/wiki/LighterTheme',
      keywords='trac plugin',
      license="BSD",
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests*']),
      include_package_data=True,
      zip_safe=False,
      entry_points = """
      [trac.plugins]
      lightertheme = lightertheme
      """,
      )

