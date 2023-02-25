from io import open
from setuptools import setup, Extension

def read(fname, encoding='utf-8'):
    with open(fname, encoding=encoding) as f:
        return f.read()

setup(
    name='doepy',
    version="0.0.1",
    author='Tirthajyoti Sarkar',
    author_email='tirthajyoti@gmail.com',
    description='Design of experiments generator with simple CSV input/output options',
    url='https://github.com/tirthajyoti/doepy',
    download_url = 'https://github.com/tirthajyoti/doepy/archive/0.0.1.tar.gz',
    license='MIT License',
    long_description_content_type='text/markdown',
    long_description=read('Readme.md'),
    packages=['doepy'],
    install_requires=['pyDOE', 'numpy','pandas','diversipy'],
    keywords=[
        'DOE',
        'science',
        'physics',
        'engineering',
        'design of experiments',
        'experimental design',
        'optimization',
        'statistics',
        'python'
        ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Education',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Scientific/Engineering :: Physics',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities'
        ]
    )
