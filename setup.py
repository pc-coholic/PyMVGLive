try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='PyMVGLive',
    version='1.1.3',
    description='get live-data from mvg-live.de',
    author='pc-coholic',
    author_email='martin@pc-coholic.de',
    url='https://github.com/pc-coholic/PyMVGLive',
    packages=['MVGLive'],
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords='',
    license='?',
    install_requires=['requests'],
)
