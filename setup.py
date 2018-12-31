from distutils.core import setup

setup(
    name='TTYles',
    version='0.1.0',
    author='buckle2000',
    # author_email='',
    packages=['ttyles'],
    # scripts=['bin/stowe-towels.py','bin/wash-towels.py'],
    # url='http://pypi.python.org/pypi/TTYles/',
    license='LICENSE',
    description='Easy to use terminal manipulation library with a Pythonic interface.',
    long_description=open('README.md').read(),
    install_requires=[
        "blessed>=1.15.0",
    ],
)
