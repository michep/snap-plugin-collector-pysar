from setuptools import setup

setup(name='snap-plugin-collector-pysar',
      version = '0.1',
      packages = ['snap_pysar'],
      install_requires = ['snap-plugin-lib-py>=1.0.10,<2'],
      url = "https://github.com/michep/snap-plugin-collector-pysar",
      author = "Mike Chepaykin",
      author_email="michep@mail.ru"
      )
