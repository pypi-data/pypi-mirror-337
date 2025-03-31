from setuptools import setup, find_packages

setup(
    name='Y_lw',
    version='0.2.2',
    packages=find_packages(),
    description='A simple library that prints a greeting.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Y-ellow',
    author_email='im.yellow.dev@gmail.com',
    url='https://github.com/im-yellow/Y_ellow/',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
