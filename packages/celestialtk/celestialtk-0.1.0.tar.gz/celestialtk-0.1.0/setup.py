from setuptools import setup, find_packages

setup(
    name='celestialtk',
    version='0.1.0',
    author='Alex Ricardo Castañeda Rodríguez',
    author_email='castaneda.systems@gmail.com',
    description='A Tkinter animation library for celestial-like floating points',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/ricardious',
    download_url='https://github.com/ricardious/celestialtk.git',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Multimedia :: Graphics'
    ],
    keywords='tkinter animation visualization',
    python_requires='>=3.6',
    install_requires=[],
)