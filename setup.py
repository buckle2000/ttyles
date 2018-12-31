import json
from distutils.core import setup

with open('Pipfile.lock') as f:
    install_requires = [k + v['version'] for k,v in json.load(f)['default'].items()]

setup(
    name='TTYles',
    version='0.1.1',
    author='buckle2000',
    # author_email='',
    packages=['ttyles'],
    # scripts=['bin/stowe-towels.py','bin/wash-towels.py'],
    url='https://github.com/buckle2000/ttyles/',
    license='LICENSE',
    description='Easy to use terminal manipulation library with a Pythonic interface.',
    long_description=open('README.md').read(),
    install_requires=install_requires,
)
