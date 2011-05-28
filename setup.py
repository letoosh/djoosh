import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "djoosh",
    version = "0.1",
    author = "Alex Berezovskiy",
    author_email = "letoosh@gmail.com",
    description = ("A super simple Django-whoosh search engine "),
    license = "BSD",
    keywords = "django whoosh search models simple",
    url = "http://packages.python.org/djoosh",
    packages=['djoosh'],
    long_description=read('README'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)