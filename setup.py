from setuptools import setup

setup(name='snap-plugin-collector-pysar',
      version = '0.1',
      packages = ['snap_pysar'],
      install_requires = ['snap-plugin-lib-py>=1.0.10,<2'],
      url = "https://github.com/michep/python-sar",
      author = "Mike Chepaykin",
      author_email="michep@mail.ru",
      entry_points = {'console_scripts': ['snap-plugin-collector-pysar=snap_pysar.plugin:run']})
