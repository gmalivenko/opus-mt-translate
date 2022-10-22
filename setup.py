from setuptools import setup, find_packages


def parse_requirements(filename):
    """ load requirements from a pip requirements file """
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]


reqs = parse_requirements('requirements.txt')


setup(name='opus-mt-translate',
      version='0.0.1',
      description='opus-mt-translate',
      author='Grigory Malivenko',
      author_email='',
      packages=find_packages(),
      install_requires=reqs,
      zip_safe=False,
      entry_points={
          'console_scripts': [
              'opus-mt-translate = opus_mt_translate.cli:main',
          ],
      },
)
